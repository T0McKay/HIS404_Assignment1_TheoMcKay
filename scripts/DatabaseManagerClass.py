import sqlite3


class DatabaseManager:
    #will act as static class but using static methods and class attributes - will also throw error if tries to instatiate

    #Connects to database, or creates if it does not exist
    conn = sqlite3.connect("database.db")
    #close connection when not needed using conn.close()

    cursor = conn.cursor

    conn.commit()

    conn.close()

    