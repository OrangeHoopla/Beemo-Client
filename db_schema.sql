CREATE TABLE users (
    sub varchar(255)  NOT NULL,
    username varchar(255),
    PRIMARY KEY (sub)
); 

CREATE TABLE hives (
	name varchar(255),
	id varchar(255) NOT NULL,
	sub varchar(255),
	PRIMARY KEY(id),
	FOREIGN KEY(sub) REFERENCES users(sub)

);

CREATE TABLE temp (
	recorded TIMESTAMP,
	temp int,
	id varchar(255) NOT NULL,
	sub varchar(255),
	FOREIGN KEY(id) REFERENCES hives(id),
	FOREIGN KEY(sub) REFERENCES users(sub)

);

CREATE TABLE weight (
	recorded TIMESTAMP,
	weight DECIMAL(5,2),
	id varchar(255) NOT NULL,
	sub varchar(255),
	FOREIGN KEY(id) REFERENCES hives(id),
	FOREIGN KEY(sub) REFERENCES users(sub)

);

CREATE TABLE humidity (
	recorded TIMESTAMP,
	humidity smallint,
	id varchar(255) NOT NULL,
	sub varchar(255),
	FOREIGN KEY(id) REFERENCES hives(id),
	FOREIGN KEY(sub) REFERENCES users(sub)

);

CREATE TABLE log (
recorded TIMESTAMP,
note nvarchar(3000),
sub varchar(255) NOT NULL,
FOREIGN KEY(sub) REFERENCES users(sub)
);

CREATE TABLE signalstrength (
	strength smallint,
	id varchar(255) NOT NULL,
	sub varchar(255),
	FOREIGN KEY(id) REFERENCES hives(id),
	FOREIGN KEY(sub) REFERENCES users(sub)
);

CREATE TABLE battery (
	recorded TIMESTAMP,
	charge smallint,
	id varchar(255) NOT NULL,
	sub varchar(255),
	FOREIGN KEY(id) REFERENCES hives(id),
	FOREIGN KEY(sub) REFERENCES users(sub)
);

CREATE TABLE hiveinfo (
note nvarchar(3000),
id varchar(255) NOT NULL,
beetype varchar(255),
location varchar(255),
hivetype varchar(255),
temperment varchar(255),
FOREIGN KEY(id) REFERENCES hives(id)
)

SELECT * FROM Users
SELECT * FROM Hives
SELECT * FROM temp

#phony data
INSERT INTO users (sub,username) 
VALUES ('87b9886b-a4ff-4eb5-9049-d2eb43234599','quade'); 

INSERT INTO hives (name,sub,id)
VALUES ('beehive1','24f213a1-64f4-4d1b-b397-e4ef6774c444','abc123');

#YYYY-MM-DD HH:MI:SS
INSERT INTO temp (recorded,temp,id,sub) 
VALUES ('2021-12-25 15:40:03',85,"abc123","4f9124ef-3f13-4460-8ca8-9054c439d1c2"); 
DELETE FROM hives WHERE sub="87b9886b-a4ff-4eb5-9049-d2eb43234599" AND NOT id="abc123"; --- due to temp 