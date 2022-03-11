DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS authors;

CREATE TABLE authors (
    auth_id      CHAR(10),
    first_name   VARCHAR(25)   NOT NULL,
    last_name    VARCHAR(25)   NOT NULL,
    country      VARCHAR(35)   NOT NULL,
    PRIMARY KEY (auth_id)
);

CREATE TABLE customers (
    cust_id        CHAR(10),
    first_name     VARCHAR(25)     NOT NULL,
    last_name      VARCHAR(25)     NOT NULL,
    num_purchases  INT             NOT NULL,
    total_spent    NUMERIC(5, 2)   NOT NULL,
    PRIMARY KEY (cust_id),
    CHECK (num_purchases >= 0),
    CHECK (total_spent >= 0)
);

CREATE TABLE books (
    book_id        CHAR(10),
    title          VARCHAR(45)     NOT NULL,
    auth_id        CHAR(10)        NOT NULL,
    genre          VARCHAR(15)     NOT NULL,
    curr_price     NUMERIC(2, 2)   NOT NULL,
    PRIMARY KEY (book_id),
    FOREIGN KEY (auth_id) REFERENCES authors(auth_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (curr_price > 0)
);

CREATE TABLE ratings (
    rating_id      INT             AUTO_INCREMENT,
    cust_id        CHAR(10)        NOT NULL,
    book_id        CHAR(10)        NOT NULL,
    rating         INT             NOT NULL,
    PRIMARY KEY (rating_id),
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (rating IN (1, 2, 3, 4, 5))
);

-- specific details about a given track on a playlist
-- contains the track's unique uri code, the name of the track, the
-- artist who made the track's uri code and the track's album's uri code
-- and the playlist this track is on's uri code, the duration of the track,
-- the url at which the track can be previewed, the songs popularity rating,
-- (a numerical value) and the timestamp of when
-- the track was added to the playlist, and who added the song to the
-- playlist (name of the user)
-- all of the fields except the preview url and added by can't be null
-- this table depends on artist, album, and playlist
CREATE TABLE track (
    track_uri       VARCHAR(100),
    track_name      VARCHAR(250)    NOT NULL,
    artist_uri      VARCHAR(100)    NOT NULL,
    album_uri       VARCHAR(100)    NOT NULL,
    playlist_uri    VARCHAR(100)    NOT NULL,
    duration_ms     VARCHAR(10)     NOT NULL,
    preview_url     VARCHAR(300),
    popularity      VARCHAR(10)     NOT NULL,
    added_at        TIMESTAMP       NOT NULL,
    added_by        VARCHAR(50),
    PRIMARY KEY (track_uri),
    FOREIGN KEY (artist_uri) REFERENCES artist(artist_uri) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (album_uri) REFERENCES album(album_uri) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (playlist_uri) REFERENCES playlist(playlist_uri) 
    ON DELETE CASCADE ON UPDATE CASCADE
);