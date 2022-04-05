from datetime import date, timedelta, datetime
from flask import Flask, render_template
import sqlite3
con = sqlite3.connect('library.db', check_same_thread=False)
cur = con.cursor()


def testDB():

    for index in range(1, 4):
        cur.execute(
            f"INSERT INTO Customers (custID,Name,Age,City) VALUES (NULL,'cust{index}',18+{int(index)},'city{index}')")
        cur.execute(
            f"INSERT INTO Books (BookID,Name,Author,YearPublished,Type,Available) VALUES (NULL,'book{index}','Author{index}',{int(index)}+2000,{index},'NO')")
        cur.execute(
            f"INSERT INTO Loans (BookID,CustID,Status) VALUES ({index},4-{int(index)},'Loaned')")
        cur.execute(
            '''UPDATE Loans SET loanDate='2022-03-01' WHERE BookID=1 ''')
        cur.execute(
            '''UPDATE Loans SET loanDate='2022-03-01' WHERE BookID=2 ''')
        cur.execute(
            '''UPDATE Loans SET loanDate='2022-03-01' WHERE BookID=3 ''')
    cur.execute(
        f"INSERT INTO Books (BookID,Name,Author,YearPublished,Type,Available) VALUES (NULL,'book4','Author4',2004,1,'YES')")
    con.commit()
    msg = '''Customers, Books and Loans have been added to the DB!
    There is 1 available book that you can try to loan by yourself!'''
    return render_template('index.html', msg=msg)


def resetDB():
    cur.execute('DELETE FROM Loans')
    cur.execute('DELETE FROM Books')
    cur.execute('DELETE FROM Customers')
    con.commit()
    msg = '''All data has been reset!'''
    return render_template('index.html', msg=msg)
