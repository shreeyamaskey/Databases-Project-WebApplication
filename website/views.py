from flask import Blueprint, render_template, request, flash, redirect, url_for
import os.path
import mariadb
from db_tunnel import DatabaseTunnel
import sys
from project.db_connector import DatabaseApp
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import InputRequired, Length


views = Blueprint('views', __name__)

DB_NAME = "sm08081_project"
DB_USER = "token_eded"
DB_PASSWORD = "3Q4P_QmUPT5aiiL8"


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/customer-checkout', methods=['GET', 'POST'])
def customer_checkout():

    class RentalForm(FlaskForm):
        customer_id = StringField('Customer ID')
        rented_date = DateField('Rented Date (yyyy-mm-dd)', format='%Y-%m-%d', validators=[InputRequired()])
        book_id = StringField('Book ID')
        return_date = DateField('Return Date (yyyy-mm-dd)', format='%Y-%m-%d', validators=[InputRequired()])
        been_returned = StringField('Y/N Choice', validators=[InputRequired(), Length(min=1, max=1)])
        checkout = SubmitField('Checkout')

    form = RentalForm()

    if form.validate_on_submit():
        # Retrieve form data
        customer_id = form.customer_id.data
        rented_date = form.rented_date.data
        book_id = form.book_id.data
        return_date = form.return_date.data
        been_returned = form.been_returned.data
        # fixing the date format
        rented_date = form.rented_date.data.strftime('%Y-%m-%d')
        return_date = form.return_date.data.strftime('%Y-%m-%d')

        with \
                DatabaseTunnel() as tunnel, \
                DatabaseApp(
                    dbHost='127.0.0.1', dbPort=tunnel.getForwardedPort(),
                    dbName=DB_NAME,
                    dbUser=DB_USER, dbPassword=DB_PASSWORD
                ) as app:

            try:
                app.insertRentals(customer_id, book_id, rented_date, return_date, been_returned)
                # redirect to the page where the invoice is printed
                app.insertInvoice(book_id, customer_id, rented_date)
                return redirect(url_for('views.print_invoice'))

            except mariadb.Error as err:
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
                print("SQL error when running database app!\n", file=sys.stderr)
                print(err, file=sys.stderr)
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)

    return render_template("customer.html", form=form)


@views.route('/customer-checkout1/<int:customer_id_param>', methods=['GET', 'POST'])
def customer_checkout1(customer_id_param):

    class RentalForm(FlaskForm):
        customer_id = StringField('Customer ID')
        rented_date = DateField('Rented Date (yyyy-mm-dd)', format='%Y-%m-%d', validators=[InputRequired()])
        book_id = StringField('Book ID')
        return_date = DateField('Return Date (yyyy-mm-dd)', format='%Y-%m-%d', validators=[InputRequired()])
        been_returned = StringField('Y/N Choice', validators=[InputRequired(), Length(min=1, max=1)])
        checkout = SubmitField('Checkout')

    form = RentalForm()

    # Pre-fill the customer_id field with the value from the route parameter
    form.customer_id.data = str(customer_id_param)

    if form.validate_on_submit():
        # Retrieve form data
        customer_id = form.customer_id.data
        rented_date = form.rented_date.data
        book_id = form.book_id.data
        return_date = form.return_date.data
        been_returned = form.been_returned.data
        # fixing the date format
        rented_date = form.rented_date.data.strftime('%Y-%m-%d')
        return_date = form.return_date.data.strftime('%Y-%m-%d')

        with \
                DatabaseTunnel() as tunnel, \
                DatabaseApp(
                    dbHost='127.0.0.1', dbPort=tunnel.getForwardedPort(),
                    dbName=DB_NAME,
                    dbUser=DB_USER, dbPassword=DB_PASSWORD
                ) as app:

            try:
                app.insertRentals(customer_id, book_id, rented_date, return_date, been_returned)
                # redirect to the page where the invoice is printed
                app.insertInvoice(book_id, customer_id, rented_date)
                return redirect(url_for('views.print_invoice'))

            except mariadb.Error as err:
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
                print("SQL error when running database app!\n", file=sys.stderr)
                print(err, file=sys.stderr)
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)

    return render_template("customer.html", form=form)


@views.route('/display-books')
def display_books():
    with \
            DatabaseTunnel() as tunnel, \
            DatabaseApp(
                dbHost='127.0.0.1', dbPort=tunnel.getForwardedPort(),
                dbName=DB_NAME,
                dbUser=DB_USER, dbPassword=DB_PASSWORD
            ) as app:

        try:
            results = app.queryAllBooks()
        except mariadb.Error as err:
            print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
            print("SQL error when running database app!\n", file=sys.stderr)
            print(err, file=sys.stderr)
            print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
    return render_template("display_books.html", results=results)


@views.route('/update-rental', methods=['GET', 'POST'])
def update_rental():
    class UpdateRental(FlaskForm):
        id = StringField('Rental ID')
        beenReturned = StringField('(Y/N)', validators=[InputRequired(), Length(min=1, max=1)])
        update = SubmitField('Update')

    form = UpdateRental()

    if form.validate_on_submit():
        # Retrieve form data
        id = form.id.data
        beenReturned = form.beenReturned.data

        with \
                DatabaseTunnel() as tunnel, \
                DatabaseApp(
                    dbHost='127.0.0.1', dbPort=tunnel.getForwardedPort(),
                    dbName=DB_NAME,
                    dbUser=DB_USER, dbPassword=DB_PASSWORD
                ) as app:

            try:
                app.updateRental(beenReturned, id)
                return redirect(url_for('views.update_rental'))

            except mariadb.Error as err:
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
                print("SQL error when running database app!\n", file=sys.stderr)
                print(err, file=sys.stderr)
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
    return render_template("update_rental.html", form=form)


@views.route('/display-rentals')
def display_rentals():
    with \
            DatabaseTunnel() as tunnel, \
            DatabaseApp(
                dbHost='127.0.0.1', dbPort=tunnel.getForwardedPort(),
                dbName=DB_NAME,
                dbUser=DB_USER, dbPassword=DB_PASSWORD
            ) as app:

        try:
            results = app.queryAllRentals()
        except mariadb.Error as err:
            print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
            print("SQL error when running database app!\n", file=sys.stderr)
            print(err, file=sys.stderr)
            print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
    return render_template("display_rentals.html", results=results)


@views.route('/add-customer', methods=['GET', 'POST'])
def add_customer():
    class CustomerForm(FlaskForm):
        name = StringField('Customer Name')
        email = StringField('Email')
        phone = StringField('Phone', validators=[InputRequired(), Length(min=1, max=10)])
        add = SubmitField('Add')

    form = CustomerForm()

    if form.validate_on_submit():
        # Retrieve form data
        name = form.name.data
        email = form.email.data
        phone = form.phone.data

        with \
                DatabaseTunnel() as tunnel, \
                DatabaseApp(
                    dbHost='127.0.0.1', dbPort=tunnel.getForwardedPort(),
                    dbName=DB_NAME,
                    dbUser=DB_USER, dbPassword=DB_PASSWORD
                ) as app:

            try:
                app.insertCustomer(name, email, phone)
                # I want to redirect to a page but fill in one of the fields
                # Query the database to get the customer ID
                customer_id = app.recentCustomer()
                return redirect(url_for('views.customer_checkout1', customer_id_param=customer_id[0]))

            except mariadb.Error as err:
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
                print("SQL error when running database app!\n", file=sys.stderr)
                print(err, file=sys.stderr)
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
    return render_template("add_customer.html", form=form)


@views.route('/print-invoice')
def print_invoice():
    with \
            DatabaseTunnel() as tunnel, \
            DatabaseApp(
                dbHost='127.0.0.1', dbPort=tunnel.getForwardedPort(),
                dbName=DB_NAME,
                dbUser=DB_USER, dbPassword=DB_PASSWORD
            ) as app:

        try:
            results = app.queryInvoice()
        except mariadb.Error as err:
            print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
            print("SQL error when running database app!\n", file=sys.stderr)
            print(err, file=sys.stderr)
            print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
    return render_template("print_invoice.html", results=results)


@views.route('/delete-book', methods=['GET', 'POST'])
def delete():
    class DeleteBook(FlaskForm):
        id = StringField('Book ID')
        delete = SubmitField('Delete')

    form = DeleteBook()

    if form.validate_on_submit():
        # Retrieve form data
        id = form.id.data

        with \
                DatabaseTunnel() as tunnel, \
                DatabaseApp(
                    dbHost='127.0.0.1', dbPort=tunnel.getForwardedPort(),
                    dbName=DB_NAME,
                    dbUser=DB_USER, dbPassword=DB_PASSWORD
                ) as app:

            try:
                app.deleteBook(id)
                return redirect(url_for('views.delete'))

            except mariadb.Error as err:
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
                print("SQL error when running database app!\n", file=sys.stderr)
                print(err, file=sys.stderr)
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
    return render_template("delete_book.html", form=form)


@views.route('/genre-report')
def genre_report():
    with \
            DatabaseTunnel() as tunnel, \
            DatabaseApp(
                dbHost='127.0.0.1', dbPort=tunnel.getForwardedPort(),
                dbName=DB_NAME,
                dbUser=DB_USER, dbPassword=DB_PASSWORD
            ) as app:

        try:
            results = app.genreReport()
        except mariadb.Error as err:
            print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
            print("SQL error when running database app!\n", file=sys.stderr)
            print(err, file=sys.stderr)
            print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
    return render_template("genre.html", results=results)

