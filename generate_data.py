import pandas as pd
import numpy as np

# Books(book_id, title, auth_id, genre, curr_price)
# Authors(auth_id, first_name, last_name, country)
# Purchases(purchase_id, book_id, cust_id, timestamp, purchase_price)
# Ratings(rating_id, cust_id, book_id, rating)
# Customers(cust_id, first_name, last_name, num_purchases, total_spent)

# Create new dataframe
df = pd.DataFrame(columns=['book_id', 'title', 'auth_id', 'genre', 'curr_price'])

# Insert random data
data = []
data.append({'book_id': 1, 'title': 'Death of Giant Goose', 'auth_id': 1, 'genre': 'Fiction', 'curr_price': 10})
data.append({'book_id': 2, 'title': 'Death of Giant Goose', 'auth_id': 1, 'genre': 'Fiction', 'curr_price': 10})
df.to_csv('data/books.csv', index=False)