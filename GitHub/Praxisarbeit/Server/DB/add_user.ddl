CREATE USER 'nginx'@'localhost' IDENTIFIED BY 'AdminMariaDB$1';
GRANT ALL PRIVILEGES ON movie_legends_db.* TO 'nginx'@'localhost';
FLUSH PRIVILEGES;
