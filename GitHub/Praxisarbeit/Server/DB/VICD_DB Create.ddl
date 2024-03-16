CREATE TABLE Film (
  film_id  int(10) NOT NULL AUTO_INCREMENT, 
  Filmname varchar(255) NOT NULL UNIQUE, 
  `Date`   date, 
  Regie    varchar(255), 
  PRIMARY KEY (film_id));
CREATE TABLE Kritik (
  kritik_id    int(10) NOT NULL AUTO_INCREMENT, 
  Kritik       varchar(255), 
  Sterne       int(10), 
  Filmfilm_id  int(10) NOT NULL, 
  Usersuser_id int(10) NOT NULL, 
  PRIMARY KEY (kritik_id));
CREATE TABLE Users (
  user_id      int(10) NOT NULL AUTO_INCREMENT, 
  Name         varchar(255) NOT NULL, 
  Nachname     varchar(255) NOT NULL, 
  Benutzername varchar(255) NOT NULL UNIQUE, 
  Password     varchar(255) NOT NULL, 
  PRIMARY KEY (user_id));
ALTER TABLE Kritik ADD CONSTRAINT FKKritik56655 FOREIGN KEY (Usersuser_id) REFERENCES Users (user_id);
ALTER TABLE Kritik ADD CONSTRAINT FKKritik37843 FOREIGN KEY (Filmfilm_id) REFERENCES Film (film_id);

