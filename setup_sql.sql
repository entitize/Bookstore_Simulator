-- CREATE SCHEMA `cs121_final_project`;
DROP FUNCTION IF EXISTS day_of_week;
DROP PROCEDURE IF EXISTS sp_update_customer_purchase_info;
USE cs121_final_project;
source setup.sql;
source load-data.sql;
source setup-routines.sql;
source setup-passwords.sql;
source grant-permissions.sql