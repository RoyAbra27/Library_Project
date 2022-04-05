from app.main import app, initDB


if __name__ == '__main__':
    initDB()
    app.run(debug=True, port=8888)
