CREATE DATABASE IF NOT EXISTS timetable_db3;
USE timetable_db3;

CREATE TABLE IF NOT EXISTS subjects (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50),
  teacher VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS timetable (
  id INT AUTO_INCREMENT PRIMARY KEY,
  class_name VARCHAR(10),
  day VARCHAR(20),
  period1 VARCHAR(100),
  period2 VARCHAR(100),
  period3 VARCHAR(100),
  period4 VARCHAR(100),
  break_time VARCHAR(20),
  period5 VARCHAR(100),
  period6 VARCHAR(100),
  period7 VARCHAR(100),
  period8 VARCHAR(100)
);

TRUNCATE TABLE subjects;

INSERT INTO subjects (name, teacher) VALUES
('English', 'Mr. Sharma'),
('Maths', 'Ms. Gupta'),
('Science', 'Mr. Verma'),
('Social Studies', 'Mrs. Mehta'),
('Hindi', 'Ms. Rani'),
('Computer', 'Mr. Raj'),
('Sanskrit', 'Ms. Kaur'),
('Physical Education', 'Mr. singh')


