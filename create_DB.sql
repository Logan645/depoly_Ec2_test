create database week6_DB;
use week6_DB;
create table member(
	id bigint not null auto_increment,
    name varchar(255) not null,
    account varchar(255) not null UNIQUE,
    password varchar(255) not null,
    CONSTRAINT unique_account primary key(id, account));

create index member_name on member(name);

create table message( 
    ID bigint not null primary key auto_increment,
    user_ID bigint not null,
    message varchar(255) not null,
    FOREIGN KEY (user_ID) REFERENCES member(id)
    );