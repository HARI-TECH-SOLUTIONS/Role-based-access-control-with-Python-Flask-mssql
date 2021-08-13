create database login_system


select * from items

select * from Users


create table items(
ID int identity(1,1) primary key,
userId int not null,
item varchar(200) not null,
role varchar(10) not null)


create table Users(
Id int identity(1,1) primary key,
FName varchar(20) not null,
LName varchar(20) not null,
UName varchar(20) not null,
Email varchar(40) not null,
Password varchar(max) null,
role varchar(10) not null)

insert into Users
values('admin', 'admin', 'admin', 'admin@gmail.com', 'e10adc3949ba59abbe56e057f20f883e', 'admin')


insert into Users
values('root', 'root', 'root', 'root@gmail.com', 'e10adc3949ba59abbe56e057f20f883e', 'root')


UPDATE Users
SET UName = 'ROOT'
WHERE Id = '2';


insert into items (userId, item)
values (@id, 'task101');

