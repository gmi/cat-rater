from dotenv import load_dotenv
import os
import mysql.connector
import mysql.connector.cursor
import random
from datetime import datetime

load_dotenv()

DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

directory = 'static/cats'

def get_all_cat_pics(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_paths.append(file)
    return file_paths

def mysql_connection(db_iscreated=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                if db_iscreated:
                    mydb = mysql.connector.connect(
                        host=DB_HOST,
                        user=DB_USER,
                        password=DB_PASS,
                        port=DB_PORT,
                        database=DB_NAME
                    )
                else:
                    mydb = mysql.connector.connect(
                        host=DB_HOST,
                        user=DB_USER,
                        password=DB_PASS,
                        port=DB_PORT,
                    )
                cursor = mydb.cursor()
                func(cursor, *args, **kwargs)
                mydb.commit()  # commit any changes made during the operation
                cursor.close()
            except Exception as e:
                print("database operation failed:", e)
                
        return wrapper
    return decorator

def mysql_connection_with_return(db_iscreated=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                if db_iscreated:
                    mydb = mysql.connector.connect(
                        host=DB_HOST,
                        user=DB_USER,
                        password=DB_PASS,
                        port=DB_PORT,
                        database=DB_NAME
                    )
                else:
                    mydb = mysql.connector.connect(
                        host=DB_HOST,
                        user=DB_USER,
                        password=DB_PASS,
                        port=DB_PORT,
                    )
                cursor = mydb.cursor()
                result = func(cursor, *args, **kwargs)
                mydb.commit()  # commit any changes made during the operation
                cursor.close()
                return result
            except Exception as e:
                print("database operation failed:", e)
                return None
                
        return wrapper
    return decorator


@mysql_connection(db_iscreated=False)
def create_database(cursor):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    create_tables()

@mysql_connection()
def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cat_ratings (
            ID INT NOT NULL UNIQUE,
            PicRoute VARCHAR(255) NOT NULL,
            Rating INT NOT NULL,
            PRIMARY KEY (ID)
        ) 
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vote_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ip_address VARCHAR(45) NOT NULL,
            cat_id INT NOT NULL,
            vote_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX (ip_address, cat_id)
        )
    ''')
    paths = get_all_cat_pics(directory)
    data = [(i, path, 0) for i, path in enumerate(paths)]
    
    query = "INSERT INTO cat_ratings (ID, PicRoute, Rating) VALUES (%s, %s, %s)"
    cursor.executemany(query, data)


@mysql_connection()
def insert_cat(cursor, ID, PicRoute, Rating):
    cursor.execute(f'''
        INSERT INTO cat_ratings (ID, PicRoute, Rating)
        VALUES({ID}, '{PicRoute}', {Rating})
    ''')
    
'''# this was used for testing :3
@mysql_connection()
def select_all(cursor):
    cursor.execute("SELECT * FROM cat_ratings")
    results = cursor.fetchall()
    for row in results:
        print(row)
'''

@mysql_connection_with_return()
def get_row_count(cursor):
    cursor.execute("SELECT COUNT(*) FROM cat_ratings")
    num_rows = cursor.fetchone()[0]
    return num_rows

@mysql_connection_with_return()
def get_random_cat(cursor):
    num_rows = get_row_count()
    if num_rows > 0:
        num = random.randint(0, num_rows - 1)
        cursor.execute(f"SELECT * FROM cat_ratings WHERE ID={num}")
        cat = cursor.fetchone()
        return cat
    
@mysql_connection()
def increment_rating(cursor, ID):
    cursor.execute(f"UPDATE cat_ratings SET Rating = Rating + 1 WHERE ID = {ID}")

@mysql_connection_with_return()
def get_random_cat(cursor):
    cursor.execute("SELECT * FROM cat_ratings ORDER BY RAND() LIMIT 1")
    return cursor.fetchone()

@mysql_connection()
def increment_rating(cursor, ID):
    cursor.execute("UPDATE cat_ratings SET Rating = Rating + 1 WHERE ID = %s", (ID,))

@mysql_connection_with_return()
def get_cat_by_id(cursor, cat_id):
    cursor.execute("SELECT * FROM cat_ratings WHERE ID = %s", (cat_id,))
    return cursor.fetchone()

@mysql_connection_with_return()
def log_vote(cursor, ip_address, cat_id):
    cursor.execute('''
        INSERT INTO vote_logs (ip_address, cat_id)
        VALUES (%s, %s)
    ''', (ip_address, cat_id))

@mysql_connection_with_return()
def get_last_vote_time(cursor, ip_address):
    cursor.execute('''
        SELECT UNIX_TIMESTAMP(MAX(vote_time)) 
        FROM vote_logs 
        WHERE ip_address = %s
    ''', (ip_address,))
    result = cursor.fetchone()[0]
    return result or 0

@mysql_connection_with_return()
def get_last_cat_vote_time(cursor, ip_address, cat_id):
    cursor.execute('''
        SELECT UNIX_TIMESTAMP(MAX(vote_time)) 
        FROM vote_logs 
        WHERE ip_address = %s AND cat_id = %s
    ''', (ip_address, cat_id))
    result = cursor.fetchone()[0]
    return result or 0

@mysql_connection_with_return()
def get_top_100_cats_by_rating(cursor):
    cursor.execute('''
        SELECT * FROM cat_ratings
        ORDER BY Rating DESC
        LIMIT 100
    ''')
    return cursor.fetchall()