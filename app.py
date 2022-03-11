"""
This is a template you may start with for your Final Project application.
You may choose to modify it, or you may start with the example function
stubs (most of which are incomplete). An example is also posted
from Lecture 19 on Canvas.

For full credit, remove any irrelevant comments, which are included in the
template to help you get started. Replace this program overview with a
brief overview of your application as well (including your name/partners name).

Some sections are provided as recommended program breakdowns, but are optional
to keep, and you will probably want to extend them based on your application's
features.
"""
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. Set to False when done testing.
DEBUG = True
ADMIN_PASSWORD = "admin"
conn = None

# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='root',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',
        #   password='adminpw',
          database='cs121_final_project'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def example_query():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            # do stuff with row data
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def get_purchases(all, user_id=""):
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    if all:
        sql = 'SELECT * FROM purchases'
    else:
        sql = 'SELECT * FROM purchases WHERE cust_id = \'%s\';' % (user_id)
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        print("Purchases:")
        for row in rows:
            # row is something like (1, 1, 'kai4567890', datetime.datetime(2020, 1, 1, 0, 0), Decimal('10.23'))
            # pretty print this row
            # purchase_id,book_id,cust_id,timestamp,purchase_price
            row_display = f"purchase_id: {row[0]}, book_id: {row[1]}, cust_id: {row[2]}, timestamp: {row[3]}, purchase_price: {row[4]}"
            print(row_display)
        if not rows:
            print("No purchases found")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def add_author(first_name, last_name, country):
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'INSERT INTO authors VALUES (NULL, \'%s\', \'%s\', \'%s\');' % (first_name, last_name, country)
    try:
        cursor.execute(sql)
        conn.commit()
        sql = 'SELECT LAST_INSERT_ID();'
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            return row[0]
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def add_book(title, auth_id, genre, curr_price):
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'INSERT INTO books VALUES (NULL, \'%s\', \'%s\', \'%s\', %d);' % (title, auth_id, genre, curr_price)
    try:
        cursor.execute(sql)
        conn.commit()
        sql = 'SELECT LAST_INSERT_ID();'
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            return row[0]
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def update_book_price(book_id, new_price):
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'UPDATE books SET curr_price = %d WHERE book_id = %d' % (new_price, book_id)
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def exists(table, column, value, is_num):
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    if is_num:
        sql = f'SELECT * FROM {table} WHERE {column} = {value};'
    else:
        sql = f'SELECT * FROM {table} WHERE {column} = \'{value}\';'
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def exists_2_col(table, column, column2, value, value2, is_num, is_num2):
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    if not is_num:
        value = f'\'{value}\''
    if not is_num2:
        value2 = f'\'{value2}\''
    sql = f'SELECT * FROM {table} WHERE {column} = {value} AND {column2} = {value2};'
    print(sql)
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def get_book_price(book_id):
    cursor = conn.cursor()
    sql = 'SELECT curr_price FROM books WHERE book_id = %d;' % (book_id)
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        book_price = row[0]
        print("Retrieved book price: ", book_price)
        return row[0]
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def register_user():
    cust_id = input("Enter username: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    num_purchases = 0
    total_spent = 0
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'INSERT INTO customers VALUES (\'%s\', \'%s\', \'%s\', %d, %d);' % (cust_id, first_name, last_name, num_purchases, total_spent)
    print("Executed sql: ", sql)
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(f"Registered User: {cust_id}")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def purchase_book(user_id, book_id, book_price):
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    # purchases: purchase_id,book_id,cust_id,timestamp,purchase_price
    sql = 'INSERT INTO purchases VALUES (NULL, %d, \'%s\', NOW(), %d);' % (book_id, user_id, book_price)
    try:
        cursor.execute(sql)
        conn.commit()
        print(f"Purchased Book: {book_id}")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def view_book_info(book_id):
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'SELECT * FROM books WHERE book_id = %d;' % (book_id)
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        # Output is like: 2,Harry Potter: Chamber of Secrets,2,Fiction,12.34
        # print(row)
        print(f"Book ID: {row[0]}, Title: {row[1]}, Author ID: {row[2]}, Genre: {row[3]}, Price: {row[4]}")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def make_review(user_id, book_id, rating):
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'INSERT INTO ratings VALUES (NULL, \'%s\', %d, %d);' % (user_id, book_id, rating)
    try:
        cursor.execute(sql)
        sql = 'SELECT LAST_INSERT_ID();'
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            return row[0]
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('What would you like to do? ')
    print('  (TODO: provide command-line options)')
    print('  (a) - admin login')
    print('  (c) - client options')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'a':
        admin_login()
    elif ans == 'c':
        show_client_options()


# You may choose to support admin vs. client features in the same program, or
# separate the two as different client and admin Python programs using the same
# database.
def show_admin_options():
    """
    Displays options specific for admins, such as adding new data <x>,
    modifying <x> based on a given id, removing <x>, etc.
    """
    print('What would you like to do? ')
    print('  (v) - view all purchases')
    print('  (a) - add author')
    print('  (b) - add book')
    print('  (u) - update book price!')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'v':
        get_all = input('Do you want all purchases y/n: ').lower()
        if get_all == 'y':
            get_purchases(True)
        else:
            user_id = input('What is the user id: ').lower()
            get_purchases(False, user_id=user_id)
    elif ans == 'a':
        first_name = input('What is the author first name: ')
        last_name = input('What is the author last name: ')
        country = input('What is the author country: ')
        auth_id = add_author(first_name, last_name, country)
        print(f"new author id: {auth_id}")
    elif ans == 'b':
        title = input('What is the book title: ')
        auth_id = int(input('What is the author id: '))
        if not exists('authors', 'auth_id', auth_id, True):
            print("Author doesn't exist, add author information")
            first_name = input('What is the author first name: ')
            last_name = input('What is the author last name: ')
            country = input('What is the author country: ')
            auth_id = add_author(first_name, last_name, country)
            print(f"new author id: {auth_id}")
        genre = input('What is the genre: ')
        curr_price = float(input('What is the price: '))
        book_id = add_book(title, auth_id, genre, curr_price)
        print(f"new book id: {book_id}")
    elif ans == 'u':
        book_id = int(input('What is the book id: '))
        new_price = float(input('What is the price: '))
        update_book_price(book_id, new_price)
    

def show_client_options():
    """
    Displays options specific for clients, such as purchasing a book or
    making a review
    """
    # Ask the user for their user id
    user_id = input("What is your user id: ").lower()
    if exists('customers', 'cust_id', user_id, False):
        print(f"Welcome back {user_id}")
    else:
        print("User not found, please register")
        register_user()  
    print('What would you like to do? ')
    print('  (p) - make a purchase')
    print('  (r) - make a review')
    print('  (v) - view purchases')
    print('  (b) - see book information')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'p':
        book_id = int(input('Please enter the book id: '))
        if exists('books', 'book_id', book_id, True):
            book_price = get_book_price(book_id)
            purchase_book(user_id, book_id, book_price)
        else:
            print("Book does not exist :(")
    elif ans == 'r':
        book_id = int(input('Please enter the book id: '))
        rating = int(input('What is the rating (1 - 5): '))
        if exists_2_col('purchases', 'cust_id', 'book_id', user_id, book_id, False, True): # check user purchased book
            if exists_2_col('ratings', 'cust_id', 'book_id', user_id, book_id, False, True):# check if already rated
                print("You have already rated this book")
            rating_id = make_review(user_id, book_id, rating)
            print(f"new rating id: {rating_id}")
        else:
            print("You haven't purchased this book so you can't rate it")
    elif ans == 'v':
        get_purchases(True, user_id)
    elif ans == 'b':
        book_id = input('Please enter the book id: ').lower()
        view_book_info(book_id)

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()

def admin_login():
    """
    Quits the program, printing a good bye message to the user.
    """
    ans = input('Type in the admin password: ').lower()
    if ans == ADMIN_PASSWORD:
        print("Successfully logged in as admin")
        show_admin_options()
    else:
        print("Incorrect Password Try Again")
        admin_login()


def main():
    """
    Main function for starting things up.
    """
    show_options()


if __name__ == '__main__':
    # This conn is a global object that other functinos can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()
