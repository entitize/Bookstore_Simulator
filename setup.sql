DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS authors;

CREATE TABLE authors (
    auth_id      INT           AUTO_INCREMENT,
    first_name   VARCHAR(25)   NOT NULL,
    last_name    VARCHAR(25)   NOT NULL,
    country      VARCHAR(35)   NOT NULL,
    PRIMARY KEY (auth_id)
);

CREATE TABLE customers (
    cust_id        VARCHAR(10),
    first_name     VARCHAR(25)     NOT NULL,
    last_name      VARCHAR(25)     NOT NULL,
    num_purchases  INT             NOT NULL,
    total_spent    NUMERIC(7, 2)   NOT NULL,
    PRIMARY KEY (cust_id),
    CHECK (num_purchases >= 0),
    CHECK (total_spent >= 0)
);

-- curr_price is in USD
CREATE TABLE books (
    book_id        INT             AUTO_INCREMENT,
    title          VARCHAR(45)     NOT NULL,
    auth_id        INT             NOT NULL,
    genre          VARCHAR(15)     NOT NULL,
    curr_price     NUMERIC(4, 2)   NOT NULL,
    PRIMARY KEY (book_id),
    FOREIGN KEY (auth_id) REFERENCES authors(auth_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (curr_price > 0)
);

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
    CHECK (rating IN (1, 2, 3, 4, 5))
);

CREATE TABLE purchases (
    purchase_id      INT             AUTO_INCREMENT,
    book_id          INT             NOT NULL,
    cust_id          VARCHAR(10)     NOT NULL,
    purchase_ts      TIMESTAMP       NOT NULL,
    purchase_price   NUMERIC(4, 2)   NOT NULL,
    PRIMARY KEY (purchase_id),
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (purchase_price > 0)
);

CREATE INDEX idx_book_rating
ON ratings (book_id, rating);