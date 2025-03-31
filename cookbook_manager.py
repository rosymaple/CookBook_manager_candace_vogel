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

        # Need to create a borrowed books table to store data 
        sql_create_borrowed_books_table = """
        CREATE TABLE IF NOT EXISTS borrowed_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cookbook_id INTEGER NOT NULL,
            borrower_name TEXT NOT NULL,
            date_borrowed DATE NOT NULL,
            return_date DATE,
            FOREIGN KEY (cookbook_id) REFERENCES cookbooks (id)
        );
        """
        # Need to create a table to store the tags we will associate with books
        sql_create_tags_table = """
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """

        # Need to create a table to store cookbook tags and link them to two other tables
        # This will be our many-to-many relationship table. 
        sql_create_cookbook_tags_table = """
        CREATE TABLE IF NOT EXISTS cookbook_tags (
            cookbook_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (cookbook_id, tag_id),
            FOREIGN KEY (cookbook_id) REFERENCES cookbooks (id),
            FOREIGN KEY (tag_id) REFERENCES tags (id)
        );
        """


        # Calling the constructor for the cursor object to create a new cursor
        # (that lets us work with the database)
        cursor = conn.cursor()
        cursor.execute(sql_create_cookbooks_table)
        cursor.execute(sql_create_borrowed_books_table)
        cursor.execute(sql_create_cookbook_tags_table)
        cursor.execute(sql_create_tags_table)
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
        print(f"Error adding to collection: {e}")
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

# insert data into borrowed_cookbooks table
def track_cookbooks(conn, cookbook_id, borrower_name, date_borrowed, return_date=None):
    """ Track which friend borrowed your cookbook and when """

    sql = '''INSERT INTO borrowed_books(cookbook_id, borrower_name, date_borrowed, return_date)
    VALUES(?,?,?,?)'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (cookbook_id, borrower_name, date_borrowed, return_date))
        conn.commit()
        print(f"{borrower_name} is currently borrowing cookbook ID: {cookbook_id}. ")
    except Error as e:
        print(f"Error occured: {e}")

def add_tags(conn, cookbook_id, tags):
    """This is the function to add tags to cookbooks (gluten-free, organic, etc)"""
    try:
        cursor = conn.cursor()
        tag_ids = []

        for tag in tags:
            # inserting tag in tags table using cursor.execute
            cursor.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
            cursor.execute("SELECT id FROM tags WHERE name = ?", (tag,))
            tag_id = cursor.fetchone()
            if tag_id:
                tag_ids.append(tag_id[0])

        # inserting data into cookbook_tags table
        # this is our many-to-many relationship table
        for tag_id in tag_ids:
            cursor.execute("INSERT OR IGNORE INTO cookbook_tags (cookbook_id, tag_id) VALUES (?, ?)", (cookbook_id, tag_id))

        conn.commit()
        print(f"Successfully added tags to cookbook ID: {cookbook_id}.")
        return True
    except Error as e:
        print(f"Error adding recipe tags: {e}")
        return False


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

        # Example usage of track_borrowed_cookbook
        track_cookbooks(conn, 2, 'Candace', '2025-03-31', None)

        # Example usage of add_recipe_tags
        add_tags(conn, 1, ['gluten-free', 'organic', 'moth-food'])

        # Close the database connection
        print("\nDatabase connection closed")
        conn.close()
    else:
        print("Error! The universe is not aligned for database connections right now.")

# Code to call the main function
if __name__ == '__main__':
    main()
