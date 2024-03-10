import sqlite3

def create_db(cleaned_data):
    conn = sqlite3.connect('cleaned_result.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tweet_table (
        Tweet_Cleaned TEXT,
        Tweet_Unclean TEXT
    )
    ''')

    conn.commit()
    conn.close()

    conn = sqlite3.connect('cleaned_result.db')
    cursor = conn.cursor()

    cursor.executemany('''
    INSERT INTO tweet_table (Tweet_Cleaned, Tweet_Unclean) VALUES (?, ?)
    ''', cleaned_data)

    conn.commit()
    conn.close()

