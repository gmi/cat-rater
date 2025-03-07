from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')

def mysql_connection(func): # wrapper :3 to make db connections easier
    def wrapper(*args, **kwargs):
        try:
            mydb = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                port=DB_PORT,
            )
            mycursor = mydb.cursor()
            func(mycursor)
            mycursor.close()
        except:
            print("database opperation failed")
            
    return wrapper