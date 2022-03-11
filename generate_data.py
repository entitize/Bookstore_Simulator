import pandas as pd
import numpy as np

# Books(book_id, title, auth_id, genre, curr_price)
# Authors(auth_id, first_name, last_name, country)
# Purchases(purchase_id, book_id, cust_id, timestamp, purchase_price)
# Ratings(rating_id, cust_id, book_id, rating)
# Customers(cust_id, first_name, last_name, num_purchases, total_spent)

# Create new dataframe

def generate_books_df():
    df = pd.DataFrame(columns=['book_id', 'title', 'auth_id', 'genre', 'curr_price'])
    data = []
    data.append({'book_id': 1, 'title': 'Harry Potter: Philosopher\'s Stone', 'auth_id': 2, 'genre': 'Fiction', 'curr_price': 10.23})
    data.append({'book_id': 2, 'title': 'Harry Potter: Chamber of Secrets', 'auth_id': 2, 'genre': 'Fiction', 'curr_price': 12.34})
    data.append({'book_id': 3, 'title': 'The Hobbit', 'auth_id': 3, 'genre': 'Novel', 'curr_price': 23.45})
    data.append({'book_id': 4, 'title': 'The Lord of the Rings', 'auth_id': 1, 'genre': 'Fiction', 'curr_price': 34.56})
    data.append({'book_id': 5, 'title': 'The Da Vinci Code', 'auth_id': 1, 'genre': 'Mystery', 'curr_price': 45.67})
    df = pd.DataFrame(data, columns=['book_id', 'title', 'auth_id', 'genre', 'curr_price'])
    df.to_csv('data/books.csv', index=False)
    print("Saved to data/books.csv")

def generate_authors_df():
    df = pd.DataFrame(columns=['auth_id', 'first_name', 'last_name', 'country'])
    data = []
    data.append({'auth_id': 1, 'first_name': 'JRR', 'last_name': 'Tolkein', 'country': 'USA'})
    data.append({'auth_id': 2, 'first_name': 'JK', 'last_name': 'Rowling', 'country': 'USA'})
    data.append({'auth_id': 3, 'first_name': 'Dan', 'last_name': 'Brown', 'country': 'USA'})
    df = pd.DataFrame(data, columns=['auth_id', 'first_name', 'last_name', 'country'])
    df.to_csv('data/authors.csv', index=False)
    print("Saved to data/authors.csv")

def generate_purchase_df():
    df = pd.DataFrame(columns=['purchase_id', 'book_id', 'cust_id', 'timestamp', 'purchase_price'])
    data = []
    data.append({'purchase_id': 1, 'book_id': 1, 'cust_id': 'kai4567890', 'timestamp': '2020-01-01', 'purchase_price': 10.23})
    data.append({'purchase_id': 2, 'book_id': 2, 'cust_id': 'kai4567890', 'timestamp': '2020-01-02', 'purchase_price': 12.34})
    data.append({'purchase_id': 3, 'book_id': 3, 'cust_id': 'kai4567890', 'timestamp': '2020-01-03', 'purchase_price': 23.45})
    data.append({'purchase_id': 4, 'book_id': 4, 'cust_id': 'kai4567890', 'timestamp': '2020-01-04', 'purchase_price': 34.56})
    data.append({'purchase_id': 5, 'book_id': 5, 'cust_id': 'kai4567890', 'timestamp': '2020-01-05', 'purchase_price': 45.67})
    df = pd.DataFrame(data, columns=['purchase_id', 'book_id', 'cust_id', 'timestamp', 'purchase_price'])
    df.to_csv('data/purchases.csv', index=False)
    print("Saved to data/purchases.csv")

def generate_ratings_df():
    df = pd.DataFrame(columns=['rating_id', 'cust_id', 'book_id', 'rating'])
    data = []
    data.append({'rating_id': 1, 'cust_id': 'kai4567890', 'book_id': 1, 'rating': 3})
    df = pd.DataFrame(data, columns=['rating_id', 'cust_id', 'book_id', 'rating'])
    df.to_csv('data/ratings.csv', index=False)
    print("Saved to data/ratings.csv")

def generate_customers_df():
    df = pd.DataFrame(columns=['cust_id', 'first_name', 'last_name', 'num_purchases', 'total_spent'])
    data = []
    data.append({'cust_id': 'kai4567890', 'first_name': 'Kai', 'last_name': 'Nakamura', 'num_purchases': 5, 'total_spent': 123.45})
    df = pd.DataFrame(data, columns=['cust_id', 'first_name', 'last_name', 'num_purchases', 'total_spent'])
    df.to_csv('data/customers.csv', index=False)
    print("Saved to data/customers.csv")

# %%
if __name__ == '__main__':
    print("Generating datasets...")
    generate_books_df()
    generate_authors_df()
    generate_purchase_df()
    generate_ratings_df()
    generate_customers_df()
    print("Done")