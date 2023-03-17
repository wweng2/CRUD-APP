
/*Create the users table with the user_name, id, and poitns column */
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_name TEXT NOT NULL,
    id INT NOT NULL,
    points INT NOT NULL
);
