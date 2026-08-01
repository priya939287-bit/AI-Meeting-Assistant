import sqlite3


def create_database():

    connection = sqlite3.connect("meetings.db")

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meetings(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        transcript TEXT,

        summary TEXT,

        action_items TEXT

    )
    """)

    connection.commit()

    connection.close()


def save_meeting(transcript, summary, action_items):

    connection = sqlite3.connect("meetings.db")

    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO meetings
    (transcript, summary, action_items)

    VALUES (?, ?, ?)
    """, (transcript, summary, action_items))

    connection.commit()

    connection.close()


def get_all_meetings():

    connection = sqlite3.connect("meetings.db")

    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM meetings
    ORDER BY id DESC
    """)

    meetings = cursor.fetchall()

    connection.close()

    return meetings


def search_meetings(keyword):

    connection = sqlite3.connect("meetings.db")

    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM meetings
    WHERE transcript LIKE ?
    OR summary LIKE ?
    ORDER BY id DESC
    """, ('%' + keyword + '%', '%' + keyword + '%'))

    meetings = cursor.fetchall()

    connection.close()

    return meetings


def delete_all_meetings():

    connection = sqlite3.connect("meetings.db")

    cursor = connection.cursor()

    cursor.execute("DELETE FROM meetings")

    connection.commit()

    connection.close()


create_database() 