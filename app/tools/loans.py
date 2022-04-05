import sqlite3
from flask import request, render_template
from datetime import date, timedelta, datetime


con = sqlite3.connect('library.db', check_same_thread=False)
cur = con.cursor()


class Loans():

    def displayLoans(self):
        cur.execute("SELECT *  FROM Loans")
        loansTable = cur.fetchall()
        return render_template("loans/displayloans.html", loansTable=loansTable)

    def loanABook(self):
        if request.method == "POST":
            customerName = request.form.get('customerName')
            bookName = request.form.get('bookName')
            loanDate = date.today()
            cur.execute(
                f'''SELECT BookID FROM books WHERE Name='{bookName}' ORDER BY BookID DESC LIMIT 1 ''')
            try:
                tempBookID = list(cur.fetchall())
                resBookID = (tempBookID[0])
                finalBooklID = (resBookID[0])
            except:
                failMSG = 'Book not registered in the Library!'
                return render_template('loans/loanBook.html', failMSG=failMSG)
            cur.execute(
                f'''SELECT CustID FROM Customers WHERE Name='{customerName}' ORDER BY CustID DESC LIMIT 1 ''')
            try:
                tempCustID = list(cur.fetchall())
                resCustID = (tempCustID[0])
                finalCustID = (resCustID[0])
            except:
                failMSG = 'Customer not registered in the Library!'
                return render_template('loans/loanBook.html', failMSG=failMSG)
            cur.execute(
                f''' SELECT bookID FROM books
                     where Available= "YES" and BookID={finalBooklID}''')
            validator = cur.fetchall()
            if len(validator) == 0:
                failMSG = 'Book unavailable!'
                return render_template('loans/loanBook.html', failMSG=failMSG)
            else:
                SuccessMSG = 'Books loaned successfuly!'
                cur.execute(
                    f'''INSERT INTO loans (CustID, BookID) SELECT Customers.CustID, Books.BookID FROM Customers, Books WHERE Customers.Name="{customerName}" and Books.Name="{bookName}"''')
                cur.execute(
                    f'''UPDATE Loans SET loanDate='{loanDate}' where BookID={finalBooklID}''')
                cur.execute(
                    f'''UPDATE Books SET Available='NO' where BookID={finalBooklID}''')
                cur.execute(
                    f'''UPDATE Loans SET Status='Loaned' where BookID={finalBooklID} and ReturnDate is null ''')
                con.commit()
                return render_template('loans/loanBook.html', SuccessMSG=SuccessMSG)
        else:
            return render_template('loans/loanBook.html')

    def returnBook(self):
        if request.method == "POST":
            customerName = request.form.get('customerName')
            bookName = request.form.get('bookName')
            returnDate = date.today()
            cur.execute(
                f'''SELECT loans.custID FROM Loans
            inner join Customers on loans.CustID=Customers.CustID
            where Customers.Name= '{customerName}'
            ORDER BY loans.custID DESC LIMIT 1
            ''')
            try:  # validate that customer loaned a book
                tempCustID = list(cur.fetchall())
                resCustID = (tempCustID[0])
                finalCustID = (resCustID[0])
            except:
                failMSG = 'This Customer did not loan a book!'
                return render_template('loans/returnBook.html', failMSG=failMSG)
            cur.execute(
                f'''SELECT loans.BookID FROM Loans
            inner join Books on loans.BookID=Books.BookID
            where Books.Name= '{bookName}'
            ORDER BY loans.BookID DESC LIMIT 1
            ''')
            try:  # validate that selected book is loaned
                tempBookID = list(cur.fetchall())
                resBookID = (tempBookID[0])
                finalBookID = (resBookID[0])
            except:
                failMSG = 'This book is not loaned at this moment!'
                return render_template('loans/returnBook.html', failMSG=failMSG)
            cur.execute(
                f'''SELECT loans.BookID FROM Loans
            inner join Books on loans.BookID=Books.BookID
            inner join Customers on loans.CustID=Customers.CustID
            where Books.Name= '{bookName}' and Customers.Name= '{customerName}'
            ORDER BY loans.BookID DESC LIMIT 1''')
            try:  # validate that selected book is loaned
                tempBookID = list(cur.fetchall())
                resBookID = (tempBookID[0])
                finalBookID = (resBookID[0])
            except:
                failMSG = 'This book is not loaned by this customer!'
                return render_template('loans/returnBook.html', failMSG=failMSG)
            SuccessMSG = 'Books returned successfuly!'
            cur.execute(
                f'''UPDATE Books SET Available='YES' where BookID={finalBookID} ''')
            cur.execute(
                f'''UPDATE Loans SET ReturnDate='{returnDate}' where BookID={finalBookID} AND CustID={finalCustID}''')
            cur.execute(
                f'''UPDATE Loans SET Status='Returned' where BookID={finalBookID}''')
            con.commit()
            return render_template('loans/returnBook.html', SuccessMSG=SuccessMSG)
        else:
            return render_template('loans/returnBook.html')

    def lateloans(self):
        SQL = '''SELECT Loans.CustID,Loans.BookID, Loans.LoanDate, Books.Type FROM Loans
        INNER JOIN Books on Loans.BookID=Books.BookID
        WHERE Loans.Status = 'Loaned'
        '''
        cur.execute(SQL)
        lateTable = cur.fetchall()
        lateList = []
        for singleDate in lateTable:
            loanDate = singleDate[2]
            bookType = singleDate[3]
            today = date.today()
            finaldate = datetime.strptime(loanDate, '%Y-%m-%d')
            msgDict = {'msgType1': 'Loan is late by ' +
                       str(finaldate.date()+timedelta(days=10) - today),
                       'msgType2': 'Loan is late by ' +
                       str(finaldate.date()+timedelta(days=5) - today),
                       'msgType3': 'Loan is late by ' +
                       str(finaldate.date()+timedelta(days=2) - today)}

            if bookType == 1:
                if finaldate.date()+timedelta(days=10) <= today:
                    lateList.append(singleDate)
                    continue
            elif bookType == 2:
                if finaldate.date()+timedelta(days=5) <= today:
                    lateList.append(singleDate)
                    continue
            elif bookType == 3:
                if finaldate.date()+timedelta(days=2) <= today:
                    lateList.append(singleDate)
                    continue
            else:
                msg = 'There are no late loans!'
                return render_template('loans/displayLateLoans.html', msg=msg)
            msgDict = {'msgType1': 'Loan is late by' +
                       str(finaldate.date()+timedelta(days=10) - today),
                       'msgType2': 'Loan is late by' +
                       str(finaldate.date()+timedelta(days=5) - today),
                       'msgType3': 'Loan is late by' +
                       str(finaldate.date()+timedelta(days=2) - today)}
        try:
            return render_template('loans/displayLateLoans.html', lateList=lateList, msgDict=msgDict)
        except:
            msg = 'There are no late loans!'
            return render_template('loans/displayLateLoans.html', msg=msg)
