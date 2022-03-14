DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS authors;

-- represents the authors that have written the different books in the 
-- bookstore, has author id (is auto incremented by the table), the author's
-- first name, the author's last name, and the country the author is from
-- all of which except country can't be NULL
CREATE TABLE authors (
    auth_id      INT           AUTO_INCREMENT,
    first_name   VARCHAR(25)   NOT NULL,
    last_name    VARCHAR(25)   NOT NULL,
    country      VARCHAR(35),
    PRIMARY KEY (auth_id)
);

-- represents the customers that shop at the store
-- has customer id (is set by the customer), the customer's
-- first name, the customer's last name, the number of purchases the
-- customer has made (can't be negative) and the 
-- total amount they have spent in USD (can't be negative)
-- all of which can't be NULL
CREATE TABLE customers (
    cust_id        VARCHAR(10),
    first_name     VARCHAR(25)     NOT NULL,
    last_name      VARCHAR(25)     NOT NULL,
    num_purchases  INT             NOT NULL,
    total_spent    NUMERIC(10, 2)   NOT NULL,
    PRIMARY KEY (cust_id),
    CHECK (num_purchases >= 0),
    CHECK (total_spent >= 0)
);

-- represents the books available for purchase at the store
-- has book id (is auto incremented by the table), the book's
-- title, the id of the author of the book, the book's genre
-- and the current price of the book in USD (can't be negative)
-- the current price can be updated
-- all of which can't be NULL
-- A book can only be written by one author
CREATE TABLE books (
    book_id        INT             AUTO_INCREMENT,
    title          VARCHAR(45)     NOT NULL,
    auth_id        INT             NOT NULL,
    genre          VARCHAR(15)     NOT NULL,
    curr_price     NUMERIC(10, 2)   NOT NULL,
    PRIMARY KEY (book_id),
    FOREIGN KEY (auth_id) REFERENCES authors(auth_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (curr_price > 0)
);

-- Represents the raings made by customers
-- rating_id is auto incremented by the table
-- cust_id is the customer id of the customer that made the rating
-- book_id is the book id of the book that was rated
-- rating is the rating given by the customer on a scale from 1 - 5
-- a customer can't make multiple ratings on the same book
CREATE TABLE ratings (
    rating_id      INT             AUTO_INCREMENT,
    cust_id        VARCHAR(10)     NOT NULL,
    book_id        INT             NOT NULL,
    rating         INT             NOT NULL,
    PRIMARY KEY (rating_id),
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (rating IN (1, 2, 3, 4, 5)),
    UNIQUE(book_id, cust_id)
);

-- Represents the purchases made by customers
-- purchase_id is auto incremented by the table
-- book_id is the id of the book purchased
-- cust_id is the id of the customer who purchased the book
-- purchase_ts is the timestamp the purchase was made
-- purchase_price is the price of the book in USD (must be non negative)
-- All of the fields can't be null
-- only one book can be purchased at a time
CREATE TABLE purchases (
    purchase_id      INT             AUTO_INCREMENT,
    book_id          INT             NOT NULL,
    cust_id          VARCHAR(10)     NOT NULL,
    purchase_ts      TIMESTAMP       NOT NULL,
    purchase_price   NUMERIC(10, 2)   NOT NULL,
    PRIMARY KEY (purchase_id),
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (purchase_price > 0)
);

-- index on the time of purchase
CREATE INDEX idx_purchase_time
ON purchases (purchase_ts);

-- index on the book genre
CREATE INDEX idx_book_genre
ON books (genre);