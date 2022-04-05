from flask import Flask, render_template
import sqlite3
from .tools.customers import Customers
from .tools.books import Book
from .tools.loans import Loans
from . import appTools as appTools
# Create DB and create a cursor:
app = Flask(__name__)
con = sqlite3.connect('library.db', check_same_thread=False)
cur = con.cursor()

customers = Customers()
books = Book()
loans = Loans()

# Create table in the DB:


def initDB():
    try:

        cur.execute('''CREATE TABLE Customers (
        CustID INTEGER PRIMARY KEY,
        Name varchar(255) NOT NULL,
        age int,
        City varchar(255)
    );''')
        cur.execute('''CREATE TABLE Books (
        BookID INTEGER PRIMARY KEY,
        Name varchar(255) NOT NULL,
        Author varchar(255),
        YearPublished int,
        Type int,
        Available varchar(3)
    );''')
        cur.execute('''CREATE TABLE Loans (
        CustID int NOT NULL ,
        BookID int NOT NULL,
        LoanDate date,
        ReturnDate date,
        Status varchar(10)
        FOREIGN KEY (CustID) REFERENCES Customers(CustID)
        FOREIGN KEY (BookID) REFERENCES Books(BookID)
    );''')
        con.commit()
    except:
        print("DB already exist")
        con.commit()
        return

# Homepage:


@app.route('/home/DBtest')
def testDB():
    return appTools.testDB()


@app.route('/home/DBreset')
def resetDB():
    return appTools.resetDB()


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# Customer pages:


@app.route('/customers')
def customersMain():
    return render_template('customers/customersMain.html')


@app.route('/customers/displaycustomers', methods=['GET', 'POST'])
def displayCustomers():
    return customers.displayCustomers()


@app.route('/customers/addcustomer', methods=['GET', 'POST'])
def addCustomer():
    return customers.addCustomer()


@app.route('/customers/removecustomer', methods=['GET', 'POST'])
def removeCustomer():
    return customers.removeCustomer()

# Book pages:


@app.route('/books')
def booksMain():
    return render_template('books/booksMain.html')


@app.route('/books/displaybooks', methods=['GET', 'POST'])
def displayBooks():
    return books.displayBooks()


@app.route('/books/addbook', methods=['GET', 'POST'])
def addBook():
    return books.addBook()


@app.route('/books/removebook', methods=['GET', 'POST'])
def removeBook():
    return books.removeBook()

# Loan pages:


@app.route('/loans')
def loansMain():
    return render_template('loans/loansMain.html')


@app.route('/loans/displayloans')
def displayLoans():
    return loans.displayLoans()


@app.route('/loans/loanbook', methods=['GET', 'POST'])
def loanBook():
    return loans.loanABook()


@app.route('/loans/returnbook', methods=['GET', 'POST'])
def returnBook():
    return loans.returnBook()


@app.route('/loans/lateloans', methods=['GET', 'POST'])
def lateloans():
    return loans.lateloans()


if __name__ == '__main__':
    initDB()
    app.run(debug=True, port=8888)
