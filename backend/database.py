import sqlite3


conn = sqlite3.connect(
    "extractions.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS extractions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        document_type TEXT,

        result TEXT
    )
    '''
)

conn.commit()


def save_extraction(
    filename,
    document_type,
    result
):

    cursor.execute(
        '''
        INSERT INTO extractions
        (filename, document_type, result)

        VALUES (?, ?, ?)
        ''',
        (
            filename,
            document_type,
            str(result)
        )
    )

    conn.commit()


def get_extractions():

    cursor.execute(
        "SELECT * FROM extractions"
    )

    return cursor.fetchall()