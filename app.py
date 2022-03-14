"""
An application to simulate a book store
"""
import sys
import mysql.connector
import mysql.connector.errorcode as errorcode

DEBUG = False

# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------


def get_conn_admin():
    """"
    Returns a connected MySQL connector instance with admin permissions, 
    if connection is successful. If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='appadmin',
            password='admin',
            port='3306',
            database='cs121_final_project'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)


def get_conn_client():
    """"
    Returns a connected MySQL connector instance with client permissions, 
    if connection is successful. If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='appclient',
            password='client',
            port='3306',
            database='cs121_final_project'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
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


def authenticate(username, password):
    """
    Authenticates a user with the given username and password.
    Returns True if successful, False otherwise.
    """
    cursor = conn.cursor()
    sql = 'SELECT authenticate(\'%s\', \'%s\');' % (username, password)
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        auth = row[0]
        if auth == 1:
            return True
        return False
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')


def get_purchases_ratings(all, user_id=""):
    """"
    Returns the row of purchases and ratings for the given user_id.
    """
    cursor = conn.cursor()
    if all:
        sql = 'SELECT cust_id, book_id, purchase_ts, purchase_price, rating FROM purchases NATURAL LEFT JOIN ratings ORDER BY purchase_ts DESC;'
    else:
        sql = 'SELECT cust_id, book_id, purchase_ts, purchase_price, rating FROM purchases NATURAL LEFT JOIN ratings WHERE cust_id = \'%s\' ORDER BY purchase_ts DESC;' % (user_id)
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("Purchases and ratings:")
        for row in rows:
            row_display = f"cust_id: {row[0]}, book_id: {row[1]}, timestamp: {row[2]}, purchase_price: {row[3]}, rating: {row[4]}"
            print(row_display)
        if not rows:
            print("No purchases found")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def view_personal_information(user_id):
    """
    Get the customers information
    """
    cursor = conn.cursor()
    sql = "SELECT * FROM customers WHERE cust_id = \'%s\';" % (user_id)
    try:
        cursor.execute(sql)
        info = cursor.fetchall()[0]
        print(f"User ID: {info[0]}, First Name: {info[1]}, Last Name: {info[2]}, Num Purchases: {info[3]}, Total Spent: {info[4]}")
        
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def add_author(first_name, last_name, country):
    """
    Adds an author to the database.
    """
    cursor = conn.cursor()
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
    """
    Adds a book to the database.
    """
    cursor = conn.cursor()
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
    """
    Updates the price of a book for the given book_id.
    """
    cursor = conn.cursor()
    sql = 'UPDATE books SET curr_price = %d WHERE book_id = %d' % (new_price, book_id)
    try:
        cursor.execute(sql)
        conn.commit()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')


def update_customer_info(user_id, first_name, last_name, password):
    """
    Helper function for updating customer info
    """
    cursor = conn.cursor()
    sql = 'UPDATE customers SET first_name = \'%s\', last_name = \'%s\' WHERE cust_id = \'%s\'' % (first_name, last_name, user_id)
    sql2 = 'CALL sp_change_password(\'%s\', \'%s\');' % (user_id, password)
    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        conn.commit()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')


def exists(table, column, value, is_num):
    """
    Helper function for checking if a value exists in a table.
    """
    cursor = conn.cursor()
    if is_num:
        sql = 'SELECT * FROM %s WHERE %s = %d;' % (table, column, value)
    else:
        sql = 'SELECT * FROM %s WHERE %s = \'%s\';' % (table, column, value)
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
    """"
    Helper function for checking if a value exists in a table.
    """
    cursor = conn.cursor()
    if not is_num:
        value = f'\'{value}\''
    if not is_num2:
        value2 = f'\'{value2}\''
    sql = f'SELECT * FROM {table} WHERE {column} = {value} AND {column2} = {value2};'
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
    """"
    Returns the price of the book with the given book_id.
    """
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
    """
    Registers a new user
    """
    cust_id = input("Enter username: ")
    if exists('customers', 'cust_id', cust_id, False) or cust_id == "admin":
        print("Username already exists. Please choose different username")
        register_user()
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    password = input("Enter account password: ")
    num_purchases = 0
    total_spent = 0
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'INSERT INTO customers VALUES (\'%s\', \'%s\', \'%s\', %d, %d);' % (cust_id, first_name, last_name, num_purchases, total_spent)
    sql2 = 'CALL sp_add_user(\'%s\', \'%s\');' % (cust_id, password)
    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        conn.commit()
        print(f"Registered User: {cust_id}")
        return cust_id
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')


def purchase_book(user_id, book_id, book_price):
    """
    Purchases a book for the given user_id
    re"""
    cursor = conn.cursor()
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


def view_books_info():
    """"
    Prints out all books in the database
    """
    cursor = conn.cursor()
    sql = 'SELECT * FROM books ORDER BY genre;'
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(f"Book ID: {row[0]}, Title: {row[1]}, Author ID: {row[2]}, Genre: {row[3]}, Price: {row[4]}")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')


def make_review(user_id, book_id, rating):
    """
    Make a review for a book by a user with a rating.
    """
    cursor = conn.cursor()
    sql = 'INSERT INTO ratings VALUES (NULL, \'%s\', %d, %d);' % (user_id, book_id, rating)
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


def show_purchase_dow_stats():
    """
    Displays the number of purchases per day of the week.
    """
    cursor = conn.cursor()
    sql = 'SELECT day_of_week(DATE(purchase_ts)) as day_of_week, COUNT(*) as num_purchases FROM purchases GROUP BY day_of_week;'
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("Purchase Statistics:")
        for row in rows:
            row_display = f"day_of_week: {row[0]}, num_purchases: {row[1]}"
            print(row_display)
        if not rows:
            print("No purchases found")
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
    Displays options users can choose in the application, 
    they can login as a client or an admin
    """
    print('What would you like to do? ')
    print('  (a) - admin login')
    print('  (c) - client login')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'a':
        admin_login()
    elif ans == 'c':
        client_login()


def display_20_highest_rated_books():
    """
    Displays the 20 highest rated books in the database.
    """
    cursor = conn.cursor()
    sql = "SELECT * FROM books NATURAL JOIN (SELECT AVG(rating) as avg_rating, book_id FROM ratings GROUP BY book_id ORDER BY avg_rating LIMIT 20 ) top_20_rated;"
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            # Example output: (1, "Harry Potter: Philosopher's Stone", 2, 'Fiction', Decimal('10.23'), Decimal('3.0000'))
            print(f"Book ID: {row[0]}, Title: {row[1]}, Author ID: {row[2]}, Genre: {row[3]}, Price: {row[4]}, Average Rating: {row[5]}")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')


def display_20_most_popular_books():
    """
    Displays the 20 most popular books in the database.
    """
    cursor = conn.cursor()
    sql = "SELECT book_id, COUNT(*) as `times_purchased`, title, genre FROM purchases NATURAL JOIN books GROUP BY book_id ORDER BY COUNT(*) LIMIT 20;"
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            # Example output: (2, 1, 'Harry Potter: Chamber of Secrets', 'Fiction')
            print(f"Book ID: {row[0]}, Times Purchased: {row[1]}, Title: {row[2]}, Genre: {row[3]}")
            # print(row)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

# You may choose to support admin vs. client features in the same program, or
# separate the two as different client and admin Python programs using the same
# database.
def show_admin_options():
    """
    Displays options specific for admins, such as adding new books or authors,
    updating prices, and viewing purchase/rating information
    """
    print('What would you like to do? ')
    print('  (v) - view all purchases and ratings')
    print('  (s) - view purchase day of week stats')
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
            get_purchases_ratings(True)
        else:
            user_id = input('What is the user id: ').lower()
            get_purchases_ratings(False, user_id=user_id)
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
    elif ans == 's':
        show_purchase_dow_stats()
    show_admin_options()


def show_client_options(user_id):
    """
    Displays options specific for clients, such as purchasing a book or
    making a review
    """
    print('What would you like to do? ')
    print('  (p) - make a purchase')
    print('  (r) - make a review')
    print('  (v) - view purchases and rating')
    print('  (b) - see books information')
    print('  (h) - top 20 highest rated books')
    print('  (m) - top 20 most popular books')
    print('  (u) - update personal information')
    print('  (a) - view personal information')
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
        if exists_2_col('purchases', 'cust_id', 'book_id', user_id, book_id, False, True):  # check user purchased book
            if exists_2_col('ratings', 'cust_id', 'book_id', user_id, book_id, False, True):  # check if already rated
                print("You have already rated this book")
            else:
                rating_id = make_review(user_id, book_id, rating)
                print(f"new rating id: {rating_id}")
        else:
            print("You haven't purchased this book so you can't rate it")
    elif ans == 'v':
        get_purchases_ratings(False, user_id)
    elif ans == 'b':
        view_books_info()
    elif ans == 'h':
        display_20_highest_rated_books()
    elif ans == 'm':
        display_20_most_popular_books()
    elif ans == 'u':
        first_name = input("Please enter your new first name: ")
        last_name = input("Please enter your new last name: ")
        new_password = input("Please enter your new password: ")
        update_customer_info(user_id, first_name, last_name, new_password)
    elif ans == 'a':
        view_personal_information(user_id)
    show_client_options(user_id)


def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def admin_login():
    """
    Checks the admin login information
    """
    # the admin password is admin
    password = input('Type in the admin password: ')
    if authenticate("admin", password):
        print("Successfully logged in as admin")
        conn = get_conn_admin()
        show_admin_options()
    else:
        print("Incorrect Password Try Again")
        admin_login()


def client_login():
    """
    Checks if the client is registered, else lets them register an id
    """
    user_id = input("What is your user id: ").lower()

    if exists('customers', 'cust_id', user_id, False):
        # print(f"Welcome back {user_id}")
        password = input("What is your password: ")
        if authenticate(user_id, password):
            print("Successfully logged in")
            conn = get_conn_client()
            show_client_options(user_id)
        else:
            print("Incorrect Password Try Again")
            client_login()
    else:
        print("User not found, please register")
        user_id = register_user()
    show_client_options(user_id)


def main():
    """
    Main function for starting things up.
    """
    show_options()


if __name__ == '__main__':
    conn = get_conn_admin()
    main()
