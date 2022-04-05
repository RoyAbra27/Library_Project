import sqlite3
from flask import request, render_template
con = sqlite3.connect('library.db', check_same_thread=False)
cur = con.cursor()


class Book():
    def addBook(self):
        if request.method == 'POST':
            bookName = request.form.get('bookName')
            bookAuthor = request.form.get('bookAuthor')
            bookYear = request.form.get('bookYear')
            bookLoanType = request.form.get('bookLoanType')
            cur.execute(
                f"INSERT INTO Books (BookID,Name,Author,YearPublished,Type,Available) VALUES (NULL,'{bookName}','{bookAuthor}',{int(bookYear)},{int(bookLoanType)},'YES')")
            con.commit()
            msg = 'Book added successfully!'
            return render_template('/books/addBook.html', msg=msg)
        else:
            return render_template('/books/addBook.html')

    def displayBooks(self):
        if request.method == 'POST':  # display all books if nothing selected/search my books table
            bookInputName = request.form.get('bookInputName')
            if bookInputName == '':
                cur.execute('SELECT *  FROM Books')
                booksTable = cur.fetchall()
                return render_template("/books/displayBooks.html", booksTable=booksTable)
            else:
                cur.execute(
                    f"SELECT * FROM Books where Name='{bookInputName}'")
                booksTable = cur.fetchall()
                return render_template('/books/displayBooks.html', booksTable=booksTable)
        else:  # go first, load my page
            cur.execute('SELECT *  FROM Books')
            booksTable = cur.fetchall()
            return render_template('/books/displayBooks.html', booksTable=booksTable)

    def findBookByName(self):
        if request.method == 'POST':
            bookInputName = request.form.get('bookInputName')
            cur.execute(
                f"SELECT * FROM Books where Name='{bookInputName}'")
            booksTable = cur.fetchall()
            return render_template('/books/findBook.html', booksTable=booksTable)
        else:
            booksTable = cur.fetchall()
            return render_template('/books/findBook.html', booksTable=booksTable)

    def removeBook(self):
        if request.method == 'POST':
            bookInputName = request.form.get('bookInputName')
            cur.execute(
                f"SELECT Name FROM Books WHERE Name='{bookInputName}' ")
            Validator = cur.fetchall()
            if Validator:
                cur.execute(
                    f"DELETE FROM Books where Name='{bookInputName}'")
                con.commit()
                msg = 'Book removed successfully'
                return render_template('/books/removeBook.html', msg=msg)
            else:
                msg = 'Book not registered'
                return render_template('/books/removeBook.html', msg=msg)
        else:
            return render_template('/books/removeBook.html')
