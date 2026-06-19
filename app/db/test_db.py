import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="legalconnect",
        user="postgres",
        password="surabhi"
    )
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print(e)