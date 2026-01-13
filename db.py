import pymysql

def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="animeotaku",
        database="web_py",
        cursorclass=pymysql.cursors.DictCursor
    )
