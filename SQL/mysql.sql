create database challenge_me;

use challenge_me;

create table players(name varchar(15), hp int, power int, defense int);
create table accounts(username varchar(20), pswd varchar(20));

insert into players values('Adam', 60, 25, 10);
insert into players values('Bela', 50, 15, 7);
insert into players values('Lajos', 46, 21, 4);
insert into players values('Laci', 74, 27, 11);

insert into accounts values('gladiator2000', 'asdasd');
insert into accounts values('valaki01', '12345');
insert into accounts values('n3mtudom', 'asd123');

select * from players;
select * from accounts;




