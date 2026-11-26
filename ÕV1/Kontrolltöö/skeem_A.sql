CREATE TABLE isikud (id INT PRIMARY KEY, nimi VARCHAR(80) NOT NULL, sool CHAR(32), rasi CHAR(64));
CREATE TABLE kataloog (id INT PRIMARY KEY, pealkiri VARCHAR(100) NOT NULL, vastutaja VARCHAR(80) NOT NULL);
CREATE TABLE syndmused (
  isik_id INT NOT NULL, kirje_id INT NOT NULL, algus DATE NOT NULL, lopp DATE,
  PRIMARY KEY (isik_id, kirje_id, algus),
  FOREIGN KEY (isik_id) REFERENCES isikud(id),
  FOREIGN KEY (kirje_id) REFERENCES kataloog(id)
);
INSERT INTO isikud (id,nimi) VALUES (1,'Mari'), (2,'Karl'), (3,'Liis'), (4,'Oskar');
INSERT INTO kataloog VALUES (1,'Andmebaasid','Tiiu'), (2,'Võrgud','Arvo'), (3,'Linux','Kadi');
