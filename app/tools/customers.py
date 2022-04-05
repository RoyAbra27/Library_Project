import sqlite3
from flask import request, render_template
con = sqlite3.connect('library.db', check_same_thread=False)
cur = con.cursor()


class Customers():
    def addCustomer(self):
        if request.method == 'POST':
            custName = request.form.get('custName')
            custAge = request.form.get('custAge')
            custCity = request.form.get('custCity')
            cur.execute(
                f"INSERT INTO Customers (custID,Name,Age,City) VALUES (NULL,'{custName}',{int(custAge)},'{custCity}')")
            con.commit()
            msg = 'Customer added successfully!'
            return render_template('/customers/addCustomer.html', msg=msg)
        else:
            return render_template('/customers/addCustomer.html')

    def displayCustomers(self):
        if request.method == 'POST':
            customerInputName = request.form.get('customerInputName')
            if customerInputName == '':
                cur.execute("SELECT *  FROM Customers")
                customerTable = cur.fetchall()
                return render_template("/customers/displayCustomers.html", customerTable=customerTable)
            else:
                cur.execute(
                    f"SELECT * FROM Customers where Name='{customerInputName}'")
                customerTable = cur.fetchall()
                return render_template('/customers/displayCustomers.html', customerTable=customerTable)
        else:
            cur.execute("SELECT * FROM Customers")
            customerTable = cur.fetchall()
            return render_template('/customers/displayCustomers.html', customerTable=customerTable)

    def findCustomerByName(self):
        if request.method == 'POST':
            customerInputName = request.form.get('customerInputName')
            cur.execute(
                f"SELECT * FROM Customers where Name='{customerInputName}'")
            customerTable = cur.fetchall()
            return render_template('/customers/findCustomer.html', customerTable=customerTable)
        else:
            customerTable = cur.fetchall()
            return render_template('/customers/findCustomer.html', customerTable=customerTable)

    def removeCustomer(self):
        if request.method == 'POST':
            customerInputName = request.form.get('customerInputName')
            cur.execute(
                f"SELECT Name FROM Customers WHERE Name='{customerInputName}' ")
            Validator = cur.fetchall()
            if Validator:
                cur.execute(
                    f"DELETE FROM Customers where Name='{customerInputName}'")
                con.commit()
                msg = 'Customer removed successfully'
                return render_template('/customers/removeCustomer.html', msg=msg)
            else:
                msg = 'Customer not registered'
                return render_template('/customers/removeCustomer.html', msg=msg)
        else:
            return render_template('/customers/removeCustomer.html')
