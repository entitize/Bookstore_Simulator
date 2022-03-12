-- Seeing all of the top 20 highest rated.
SELECT * FROM books NATURAL JOIN (
    SELECT AVG(rating) as avg_rating, book_id FROM ratings
    GROUP BY book_id
    ORDER BY avg_rating
    LIMIT 20
) top_20_rated;
-- Seeing the 20 most popular books.
SELECT book_id, COUNT(*) as `times_purchased`, title, genre
FROM purchases NATURAL JOIN books
GROUP BY book_id
ORDER BY COUNT(*)
LIMIT 20;
-- Seeing all of their purchases and ratings of 
-- those purchases if they rated them.
SELECT cust_id, book_id, purchase_ts, purchase_price, rating 
FROM purchases NATURAL LEFT JOIN ratings
WHERE cust_id = 'kai4567890';
-- Seeing how many purchases are made on each day of the week
SELECT day_of_week(DATE(purchase_ts)) as day_of_week, COUNT(*) as num_purchases
FROM purchases GROUP BY day_of_week;