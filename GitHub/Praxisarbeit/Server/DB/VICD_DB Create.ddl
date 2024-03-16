CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    rating INT NOT NULL,
    comment TEXT NOT NULL,
    added_by VARCHAR(100) NOT NULL,
    FOREIGN KEY (added_by) REFERENCES users(username)
);
