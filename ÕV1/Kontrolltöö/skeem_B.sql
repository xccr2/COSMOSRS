CREATE TABLE isikud (id INT PRIMARY KEY, nimi VARCHAR(80) NOT NULL, sool CHAR(32), rasi CHAR(64));
CREATE TABLE kataloog (id INT PRIMARY KEY, pealkiri VARCHAR(100) NOT NULL, vastutaja VARCHAR(80) NOT NULL);
CREATE TABLE syndmused (
  isik_id INT NOT NULL, kirje_id INT NOT NULL, algus DATE NOT NULL, lopp DATE,
  PRIMARY KEY (isik_id, kirje_id, algus),
  FOREIGN KEY (isik_id) REFERENCES isikud(id),
  FOREIGN KEY (kirje_id) REFERENCES kataloog(id)
);
INSERT INTO isikud (id,nimi) VALUES (1,'Anna'), (2,'Märt'), (3,'Eva'), (4,'Rasmus');
INSERT INTO kataloog VALUES (1,'Põhjarada','Riin'), (2,'Linnuaed','Toomas'), (3,'Öine meri','Ene');
