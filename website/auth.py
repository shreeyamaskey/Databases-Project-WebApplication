from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)


@auth.route('/customer-checkout')
def customer_checkout():
    return render_template("customer.html")

# make a function or class to call for the db connection
# then do the sql function needed
