-- create database and user
create database options_data;
create user options_user with encrypted password 'optimal';
grant all privileges on database options_data to options_user;

