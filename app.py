import os
import psycopg2
from flask import Flask

app = Flask(__name__)

# Fetch the connection string securely from Render's environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")


@app.route("/")
def index():
    return "Hello World from Elysha in CSPB 3308"


@app.route("/db-test")
def db_test():
    conn = None
    cur = None
    try:
        # Open connection
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Run a quick test query
        cur.execute("SELECT NOW();")
        db_time = cur.fetchone()

        return f"Database connected successfully! Server time: {db_time[0]}"

    except Exception as e:
        if conn is not None:
            conn.rollback()
        return f"Database error: {e}"

    finally:
        # Crucial (Part 7): Always close connections when finished!
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()