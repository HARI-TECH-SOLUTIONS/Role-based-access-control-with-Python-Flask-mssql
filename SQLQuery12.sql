

ALTER TABLE items
ADD role varchar(10);


INSERT INTO dbo.items(role)
VALUES (user);

ALTER TABLE items
DROP COLUMN role;


ALTER TABLE items
ADD constraint (user)



INSERT INTO items(role)
VALUES('user');