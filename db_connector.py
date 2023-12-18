import mariadb
from db_tunnel import DatabaseTunnel
from datetime import datetime

DB_NAME = "sm08081_project"
DB_USER = "token_eded"
DB_PASSWORD = "3Q4P_QmUPT5aiiL8"

QUERY_DISPLAY_BOOKS = """
# SELECT *
# FROM Book
SELECT Book.id, Book.name, Book.publishedOn, Book.seriesName, Genre.name, Author.name, Author.birthYear
FROM Book
    LEFT JOIN Author ON Book.authorId = Author.id
    LEFT JOIN hasGenre ON Book.id = hasGenre.bookId
    LEFT JOIN Genre ON hasGenre.genreId = Genre.id
"""

QUERY_INSERT_RENTAL = """
INSERT INTO rentedBy (customerId, bookId, rentedDate, returnDate, beenReturned)
VALUES (%s, %s, %s, %s, %s)
"""

QUERY_INSERT_INVOICE = """
INSERT INTO Invoice (bookId, customerId, date, price)
VALUES (%s, %s, %s, %s)
"""

QUERY_INSERT_CUSTOMER = """
INSERT INTO Customer (name, email, phone)
VALUES (%s, %s, %s)
"""

QUERY_DISPLAY_INVOICE = """
SELECT Book.name, Customer.name, Invoice.date, Invoice.price
FROM Invoice
    INNER JOIN Book ON Invoice.bookId = Book.id
    INNER JOIN Customer ON Invoice.customerId = Customer.id
WHERE Invoice.id = (
    SELECT MAX(id)
    FROM Invoice
)
"""

QUERY_DISPLAY_RENTAL = """
SELECT rentedBy.id, Book.id, Book.name, Customer.id, Customer.name, rentedBy.rentedDate, rentedBy.returnDate, rentedBy.beenReturned
FROM rentedBy
    INNER JOIN Book On rentedBy.bookId = Book.id
    INNER JOIN Customer On rentedBy.customerId = Customer.id
"""

QUERY_UPDATE_RENTAL = """
UPDATE rentedBy
SET beenReturned = %s
WHERE id = %s
"""

QUERY_DELETE_BOOK = """
DELETE FROM Book
WHERE id = %s
"""

QUERY_GENRE_REPORT = """
SELECT Genre.name, COUNT(hasGenre.bookId)
FROM Genre
    INNER JOIN hasGenre ON Genre.id = hasGenre.genreId
    INNER JOIN Book ON hasGenre.bookId = Book.id
GROUP BY Genre.id
"""

class DatabaseApp:
    '''A simple Python application that interfaces with a database.'''

    def __init__(self, dbHost, dbPort, dbName, dbUser, dbPassword):
        self.dbHost, self.dbPort = dbHost, dbPort
        self.dbName = dbName
        self.dbUser, self.dbPassword = dbUser, dbPassword

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()

    def connect(self):
        self.connection = mariadb.connect(
                host=self.dbHost, port=self.dbPort, database=self.dbName,
                user=self.dbUser, password=self.dbPassword,
                autocommit=True,
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def queryAllBooks(self):
        self.cursor.execute(QUERY_DISPLAY_BOOKS)

        results = [(id, name, publishedOn, seriesName, genre, author, authorBirthYear) for (id, name, publishedOn, seriesName, genre, author, authorBirthYear) in self.cursor]
        return results

    def insertRentals(self, customerId, bookId, rentedDate, returnDate, beenReturned):
        self.cursor.execute(QUERY_INSERT_RENTAL, (customerId, bookId, rentedDate, returnDate, beenReturned))

    def insertInvoice(self, bookId, customerId, date):
        # to get the price of book
        self.cursor.execute("SELECT rentalCost FROM Book WHERE id = %s", (bookId,))
        price = self.cursor.fetchone()
        price = float(price[0])
        self.cursor.execute(QUERY_INSERT_INVOICE, (bookId, customerId, date, price))

    def queryInvoice(self):
        self.cursor.execute(QUERY_DISPLAY_INVOICE)
        results = [[bookName, customerName, date, price] for (bookName, customerName, date, price) in self.cursor]
        self.cursor.execute("SELECT returnDate FROM rentedBy WHERE id = (SELECT MAX(id) FROM rentedBy)")
        return_date = self.cursor.fetchone()
        return_date = return_date[0].strftime('%Y-%m-%d')
        results[0].append(return_date)
        return results

    def queryAllRentals(self):
        self.cursor.execute(QUERY_DISPLAY_RENTAL)
        results = [(id, bookId, name, customerId, custname, rentedDate, returnDate, beenReturned) for (id, bookId, name, customerId, custname, rentedDate, returnDate, beenReturned) in self.cursor]
        return results

    def insertCustomer(self, name, phone, email):
        self.cursor.execute(QUERY_INSERT_CUSTOMER, (name, phone, email))

    def recentCustomer(self):
        self.cursor.execute("SELECT MAX(id) FROM Customer")
        customer_id = self.cursor.fetchone()
        print(customer_id)
        return customer_id

    def updateRental(self, beenReturned, id):
        self.cursor.execute(QUERY_UPDATE_RENTAL, (beenReturned, id))

    def deleteBook(self, id):
        self.cursor.execute(QUERY_DELETE_BOOK, (id,))

    def genreReport(self):
        self.cursor.execute(QUERY_GENRE_REPORT)
        results = [(name, count) for (name, count) in self.cursor]
        return results
