-- Get purchase ratings
SELECT cust_id, book_id, purchase_ts, purchase_price, rating FROM purchases NATURAL LEFT JOIN ratings ORDER BY purchase_ts DESC;

-- Add author
INSERT INTO authors VALUES (NULL, "Kai", "Nakamura", "USA");

-- Add book
INSERT INTO books VALUES (NULL, 'Random Title', 1, 'Random Genre', 12.34);

-- update_book_price
UPDATE books SET curr_price = 15.00 WHERE book_id = 1;

-- Get book price
SELECT curr_price FROM books WHERE book_id = 1;

-- Register User
INSERT INTO customers VALUES ('neha', 'Neha', 'Dalia', 0, 0);

-- Purchase Book
INSERT INTO purchases VALUES (1, 'neha', 12.34);

-- view_books_info
SELECT * FROM books ORDER BY genre;

-- Make Review
INSERT INTO ratings VALUES ('neha', 1, 5);

-- Show purchase day of week stats
SELECT day_of_week(DATE(purchase_ts)) as day_of_week, COUNT(*) as num_purchases FROM purchases GROUP BY day_of_week

-- Seeing all of the top 20 highest rated books
-- equivalent to an RA expression
SELECT * FROM books NATURAL JOIN (
    SELECT AVG(rating) as avg_rating, book_id FROM ratings
    GROUP BY book_id
    ORDER BY avg_rating
    LIMIT 20
) top_20_rated;
-- Seeing the 20 most popular books
-- equivalent to an RA expression
SELECT book_id, COUNT(*) as `times_purchased`, title, genre
FROM purchases NATURAL JOIN books
GROUP BY book_id
ORDER BY COUNT(*)
LIMIT 20;
-- Seeing all of their purchases and ratings of 
-- those purchases if they rated them
SELECT cust_id, book_id, purchase_ts, purchase_price, rating 
FROM purchases NATURAL LEFT JOIN ratings
WHERE cust_id = 'kai4567890';
-- Seeing how many purchases are made on each day of the week
SELECT day_of_week(DATE(purchase_ts)) as day_of_week, COUNT(*) as num_purchases
FROM purchases GROUP BY day_of_week;