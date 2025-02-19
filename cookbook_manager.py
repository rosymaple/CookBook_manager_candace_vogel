# Use the SQLite database
import sqlite3
from sqlite3 import Error

# Function to create a connection to the database

def create_connection(): 
    """Create a database connection"""
    conn = None
    try: 
        conn = sqlite3.connect('hipster_cookbooks.db');
        print(f"Successfully connected to SQLite {sqlite3.version}")
        return conn    
    except Error as e:
            print(f"Error establishing connection" )

# Function to create a table for storing the cookbooks
def create_table(conn):
    """Create a table structure"""
    try: 
        sql_create_cookbooks_table = """
        CREATE TABLE IF NOT EXISTS cookbooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year_published INTEGER,
            aesthetic_rating INTEGER,
            instagram_worthy BOOLEAN,
            cover_color TEXT
        );
        """
        # Calling the constructor for the cursor object to create a new cursor
        # (that lets us work with the database)
        cursor = conn.cursor()
        cursor.execute(sql_create_cookbooks_table)
        print("Successfully created a database structure")
    except Error as e:
        print(f"Error creating table: {e}")

# Function will insert a new cookbook record into the database table
def insert_cookbook(conn, cookbook):
    """Add a new cookbook to your shelf"""
    sql = '''INSERT INTO cookbooks(title, author, year_published, aesthetic_rating, 
    instagram_worthy, cover_color)
    VALUES(?,?,?,?,?,?)'''

    # Use the connection to the database to insert the new record
    try:
        # Create a new cursor (this is like a pointer that lets us traverse the database)
        cursor = conn.cursor()
        cursor.execute(sql, cookbook)
        # Commit the changes
        conn.commit()
        print(f"Successfully curated cookbook with the id: {cursor.lastrowid}")
        return cursor.lastrowid
    except Error as e:
        print(f"Error addinf to collection: {e}")
        return None

# Function to retrieve the cookbooks from the database
def get_all_cookbooks(conn):
    """Browse your entire collection of cookbooks"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cookbooks")
        books = cursor.fetchall()

        # Iterate through the list of books and display the info for each cookbook
        for book in books:
            print(f"ID: {book[0]}")
            print(f"Title: {book[1]}")
            print(f"Author: {book[2]}")
            print(f"Published: {book[3]}")
            print(f"Aesthetic Rating: {'✨' * book[4]}")
            print(f"Instagram Worthy: {'📸 Yes' if book[5] else 'Not aesthetic enough'}")
            print(f"Cover Color: {book[6]}")
            print("---")
        return books
    except Error as e:
        print(f"Error retrieving collection: {e}")
        return []

# Main function is called when the program executes
# It directs the show
def main():
    # Establish connection to our cookbook database
    conn = create_connection()

    # Test if the connection is viable
    if conn is not None:
        # Create our table
        create_table(conn)

        # Insert some carefully curated sample cookbooks
        cookbooks = [
            ('Foraged & Found: A Guide to Pretending You Know About Mushrooms',
            'Oak Wavelength', 2023, 5, True, 'Forest Green'),
            ('Small Batch: 50 Recipes You Will Never Actually Make',
            'Sage Moonbeam', 2022, 4, True, 'Raw Linen'),
            ('The Artistic Toast: Advanced Avocado Techniques',
            'River Wildflower', 2023, 5, True, 'Recycled Brown'),
            ('Fermented Everything', 
            'Jim Kombucha', 2021, 3, True, 'Denim'),
            ('The Deconstructed Sandwich: Making Simple Things Complicated',
            'Juniper Vinegar-Smith', 2023, 5, True, 'Beige')
        ]

        # Display our list of books
        print("\n Curating your cookbook collection . . .")
        # Insert cookbooks into the database
        for cookbook in cookbooks:
            insert_cookbook(conn, cookbook)

        # Get the cookbooks from the database
        print("\nYour carefully curated collection:")
        get_all_cookbooks(conn)

        # Close the database connection
        print("\nDatabase connection closed")
    else:
        print("Error! The universe is not aligned for database connections right now.")

# Code to call the main function
if __name__ == '__main__':
    main()
