 create database mtuci_db;

\c mtuci_db 
 
 create table kafedra (id serial primary key, nazvanie_k varchar not null, dekanat varchar not null);
 create table student_group(id serial primary key, kafedra_n integer not null references kafedra(id), name_group varchar not null);
 create table student(id serial primary key, full_name varchar not null, passport varchar(10) not null, group_numb integer not null references student_group(id));

 insert into kafedra (nazvanie_k, dekanat) values ('МКиИТ', 'ИТ');
 insert into kafedra (nazvanie_k, dekanat) values ('Информатика', 'ИТ');

 insert into student_group(name_group, kafedra_n) values ('БВТ2201', '3');
 insert into student_group(name_group, kafedra_n) values ('БВТ2202', '3');
 insert into student_group(name_group, kafedra_n) values ('БИН2201', '4');
 insert into student_group(name_group, kafedra_n) values ('БИН2202', '4');


 insert into student(full_name, passport, group_numb) values ('Крюков Александр', '3818188888', '1');
 insert into student(full_name, passport, group_numb) values ('Николай Круподеров', '1234567891', '1');
 insert into student(full_name, passport, group_numb) values ('Таджитдинова Карина', '2345678531', '1');
 insert into student(full_name, passport, group_numb) values ('Щербакова Милена', '3452678546', '1');
 insert into student(full_name, passport, group_numb) values ('Тесленко Валерий', '5432789567', '1');
 insert into student(full_name, passport, group_numb) values ('Лесовой Роман', '6527845944', '2');
 insert into student(full_name, passport, group_numb) values ('Безгачева Анастасия', '1122334455', '2');
 insert into student(full_name, passport, group_numb) values ('Гладкий Андрей', '5425685313', '2');
 insert into student(full_name, passport, group_numb) values ('Аблязов Илья', '5785314686', '2');
 insert into student(full_name, passport, group_numb) values ('Титова Маргарита', '9764256863', '2');
 insert into student(full_name, passport, group_numb) values ('Арчаков Кирилл', '6748193748', '3');
 insert into student(full_name, passport, group_numb) values ('Заздравных Валерия', '9476573819', '3');
 insert into student(full_name, passport, group_numb) values ('Леновская Полина, '7859204760', '3');
 insert into student(full_name, passport, group_numb) values ('Григоренко Денис', '9684756239', '3');
 insert into student(full_name, passport, group_numb) values ('Пастухова Валерия', '1237896543','3');
 insert into student(full_name, passport, group_numb) values ('Миловский Никита', '9870685947', '4');
 insert into student(full_name, passport, group_numb) values ('Кукушкин Сергей', '6784560237', '4');
 insert into student(full_name, passport, group_numb) values ('Кесслер Алексей', '2345643217', '4');
 insert into student(full_name, passport, group_numb) values ('Попов Александр', '7865489456', '4');
 insert into student(full_name, passport, group_numb) values ('Малиновская Мария', '2345378906', '4');