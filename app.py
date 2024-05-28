from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection parameters
DB_HOST = os.getenv('DB_HOST', 'ep-spring-waterfall-a5qs90lq.us-east-2.aws.neon.tech')
DB_NAME = os.getenv('DB_NAME', 'HEDB')
DB_USER = os.getenv('DB_USER', 'houseessentialsinfo')
DB_PASS = os.getenv('DB_PASS', 'fVa4yGH1PlFb')
DB_PORT = os.getenv('DB_PORT', '5432')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn

@app.route('/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM all_orders')  # Replace 'your_table' with your table name
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Format data as a list of dictionaries
    colnames = [desc[0] for desc in cur.description]
    data = [dict(zip(colnames, row)) for row in rows]

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
