CREATE TABLE account (
 username  VARCHAR(20)    PRIMARY KEY,
 pw_hash   CHAR(32)       NOT NULL
);

UPDATE account SET pw_hash = md5('admin')
WHERE username = 'admin';