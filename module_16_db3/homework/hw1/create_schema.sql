PRAGMA foreign_keys = ON;

CREATE TABLE director(
    dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dir_first_name VARCHAR(50) NOT NULL,
    dir_last_name VARCHAR(50) NOT NULL
);

CREATE TABLE movie(
    mov_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_title VARCHAR(50) NOT NULL
);

CREATE TABLE actors(
    act_id INTEGER PRIMARY KEY AUTOINCREMENT,
    act_first_name VARCHAR(50) NOT NULL,
    act_last_name VARCHAR(50) NOT NULL,
    act_gender VARCHAR(1) NOT NULL
);

CREATE TABLE movie_direction(
    dir_id INTEGER NOT NULL REFERENCES director (dir_id) ON DELETE CASCADE,
    mov_id INTEGER NOT NULL,
    FOREIGN KEY (mov_id) REFERENCES movie (mov_id) ON DELETE CASCADE
);

CREATE TABLE oscar_awarded(
    award_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_id INTEGER NOT NULL REFERENCES movie (mov_id) ON DELETE CASCADE
);

CREATE TABLE movie_cast(
    act_id INTEGER NOT NULL REFERENCES actors (act_id) ON DELETE CASCADE,
    mov_id INTEGER NOT NULL REFERENCES movie (mov_id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL
)
