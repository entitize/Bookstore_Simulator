DROP TRIGGER IF EXISTS trg_purchases_insert;
DROP TRIGGER IF EXISTS trg_purchases_update;
DROP TRIGGER IF EXISTS trg_purchases_delete;
DROP FUNCTION IF EXISTS day_of_week;
DROP PROCEDURE IF EXISTS sp_update_customer_purchase_info;

-- DROP FUNCTION IF EXISTS day_of_week;
-- DROP PROCEDURE IF EXISTS sp_update_customer_purchase_info;
-- Given: Set the "end of statement" character to ! so we don't confuse MySQL
DELIMITER !
-- Given a date value, returns its day of week
CREATE FUNCTION day_of_week (d DATE) RETURNS VARCHAR(10) DETERMINISTIC
BEGIN
-- DAYOFWEEK returns 7 for Saturday, 1 for Sunday and so on
IF DAYOFWEEK(d) = 1
   THEN RETURN 'Sunday';
ELSEIF DAYOFWEEK(d) = 2
   THEN RETURN 'Monday';
ELSEIF DAYOFWEEK(d) = 3
   THEN RETURN 'Tuesday';
ELSEIF DAYOFWEEK(d) = 4
   THEN RETURN 'Wednesday';
ELSEIF DAYOFWEEK(d) = 5
   THEN RETURN 'Thursday';
ELSEIF DAYOFWEEK(d) = 6
   THEN RETURN 'Saturday';
ELSE RETURN 'Saturday';
END IF;
END !
DELIMITER ;

DELIMITER !

-- A procedure to execute when inserting/deleting a new purchase
CREATE PROCEDURE sp_update_customer_purchase_info(
    new_cust_id          CHAR(10),
    num_purchase_change  INT,
    new_purchase_price   NUMERIC(10, 2)
)
BEGIN 
    INSERT INTO customers
        -- customer not already in view; add row (can update information about name later)
        VALUES (new_cust_id, 'temp first name', 'temp last name', num_purchase_change, new_purchase_price)
    ON DUPLICATE KEY UPDATE 
        -- customer already in view; update existing row
        num_purchases = num_purchases + num_purchase_change,
        total_spent = total_spent + new_purchase_price;
END !

-- Handles new rows added to purchase table, updates customer info accordingly
CREATE TRIGGER trg_purchases_insert AFTER INSERT
       ON purchases FOR EACH ROW
BEGIN
    CALL sp_update_customer_purchase_info(NEW.cust_id, 1, NEW.purchase_price);
END !
DELIMITER ;

DELIMITER !
-- Handles rows deleted from purchase table, updates customer info accordingly
CREATE TRIGGER trg_purchases_delete AFTER DELETE
       ON purchases FOR EACH ROW
BEGIN
    CALL sp_update_customer_purchase_info(OLD.cust_id, -1, -1 * OLD.purchase_price);
END !
DELIMITER ;

DELIMITER !
-- Handles rows updated in the purchase table, updates customer info accordingly
CREATE TRIGGER trg_purchases_update AFTER UPDATE
       ON purchases FOR EACH ROW
BEGIN
    -- deletes old data
    CALL sp_update_customer_purchase_info(OLD.cust_id, -1, -1 * OLD.purchase_price);
    -- adds new data
    CALL sp_update_customer_purchase_info(NEW.cust_id, 1, NEW.purchase_price);
END !
DELIMITER ;