import os

import psycopg2
from flask import Flask

app = Flask(__name__)

# Fetch the connection string securely from Render's environment variables.
DATABASE_URL = os.environ.get("DATABASE_URL")

# Fix for Render URL scheme compatibility.
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")


@app.route("/")
def index():
    return "Hello World from Elysha in CSPB 3308"


@app.route("/db_test")
def db_test():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("SELECT NOW();")
        db_time = cur.fetchone()

        return f"Database connected successfully! Server time: {db_time[0]}"

    except Exception as e:
        if conn is not None:
            conn.rollback()

        return f"Database error: {e}", 500

    finally:
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()


@app.route("/db_create")
def db_create():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        sql = """
        CREATE TABLE IF NOT EXISTS Basketball(
            First varchar(255),
            Last varchar(255),
            City varchar(255),
            Name varchar(255),
            Number int
        );
        """

        cur.execute(sql)
        conn.commit()

        return "Basketball Table Created"

    except Exception as e:
        if conn is not None:
            conn.rollback()

        return f"Database error: {e}", 500

    finally:
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()


@app.route("/db_insert")
def db_insert():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        sql = """
        INSERT INTO Basketball (First, Last, City, Name, Number)
        VALUES
        ('Jayson', 'Tatum', 'Boston', 'Celtics', 0),
        ('Stephen', 'Curry', 'San Francisco', 'Warriors', 30),
        ('Nikola', 'Jokic', 'Denver', 'Nuggets', 15),
        ('Kawhi', 'Leonard', 'Los Angeles', 'Clippers', 2),
        ('Elysha', 'Smith', 'CU Boulder', 'CSPB 3308', 3308);
        """

        cur.execute(sql)
        conn.commit()

        return "Basketball Table Populated"

    except Exception as e:
        if conn is not None:
            conn.rollback()

        return f"Database error: {e}", 500

    finally:
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()


@app.route("/db_select")
def db_select():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("SELECT * FROM Basketball;")
        records = cur.fetchall()

        html = "<table border='1'>"
        html += (
            "<tr>"
            "<th>First</th>"
            "<th>Last</th>"
            "<th>City</th>"
            "<th>Name</th>"
            "<th>Number</th>"
            "</tr>"
        )

        for row in records:
            html += "<tr>"

            for value in row:
                html += f"<td>{value}</td>"

            html += "</tr>"

        html += "</table>"

        return html

    except Exception as e:
        if conn is not None:
            conn.rollback()

        return f"Database error: {e}", 500

    finally:
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()


@app.route("/db_drop")
def db_drop():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS Basketball;")
        conn.commit()

        return "Basketball Table Dropped"

    except Exception as e:
        if conn is not None:
            conn.rollback()

        return f"Database error: {e}", 500

    finally:
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()