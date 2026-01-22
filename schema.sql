DROP DATABASE IF EXISTS electives;
CREATE DATABASE electives;
USE electives;

-- Clean up old objects if present
DROP TRIGGER IF EXISTS CGPA_check;
DROP TRIGGER IF EXISTS DOB_check;
DROP TRIGGER IF EXISTS update_elective;
DROP PROCEDURE IF EXISTS interest_matcher_project;
DROP PROCEDURE IF EXISTS interest_matcher_elective;
DROP PROCEDURE IF EXISTS pastproject_matcher_project;
DROP PROCEDURE IF EXISTS pastproject_matcher_elective;

DROP TABLE IF EXISTS Works_On;
DROP TABLE IF EXISTS Project_Guide;
DROP TABLE IF EXISTS Company_Locations;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS Elective;
DROP TABLE IF EXISTS Job;
DROP TABLE IF EXISTS Company;
DROP TABLE IF EXISTS Belongs_To;
DROP TABLE IF EXISTS Taught_By;
DROP TABLE IF EXISTS Teacher;
DROP TABLE IF EXISTS Student;

-- STUDENT TABLE
CREATE TABLE Student(
  SRN varchar(20)  NOT NULL,
  Student_Name varchar(50) NOT NULL,
  CGPA decimal(3,2) DEFAULT NULL,
  DOB date DEFAULT NULL,
  Graduated_year YEAR DEFAULT NULL,
  PRIMARY KEY(SRN)
);

-- TEACHER TABLE
CREATE TABLE Teacher(
  Teacher_ID varchar(10)  NOT NULL,
  Teacher_Name varchar(50) NOT NULL,
  PRIMARY KEY(Teacher_ID)
);

-- ELECTIVE TABLE (FULLTEXT on Syllabus)
CREATE TABLE Elective(
  Course_ID varchar(20) NOT NULL,
  Course_Name varchar(100) NOT NULL,
  Syllabus TEXT DEFAULT NULL,
  Avg_Grade varchar(10) DEFAULT NULL,
  Difficulty varchar(20) DEFAULT NULL,
  Class_Size varchar(10) DEFAULT NULL,
  Elective_Number int DEFAULT NULL,
  Elective_Description varchar(255) DEFAULT NULL,
  Semester int DEFAULT NULL,
  PRIMARY KEY(Course_ID),
  FULLTEXT KEY (Syllabus)
);

-- BELONGS_TO TABLE
CREATE TABLE Belongs_To(
  SRN varchar(20) NOT NULL,
  Course_ID varchar(20) NOT NULL,
  feedback varchar(1000),
  grade INT,
  PRIMARY KEY(SRN,Course_ID),
  FOREIGN KEY(SRN) REFERENCES Student(SRN),
  FOREIGN KEY(Course_ID) REFERENCES Elective(Course_ID)
);

-- TAUGHT_BY TABLE (associate teachers with electives)
CREATE TABLE Taught_By(
  SRN varchar(20),
  Course_ID varchar(20),
  Teacher_ID varchar(20),
  PRIMARY KEY(SRN,Course_ID,Teacher_ID),
  FOREIGN KEY(SRN) REFERENCES Student(SRN),
  FOREIGN KEY(Course_ID) REFERENCES Elective(Course_ID),
  FOREIGN KEY(Teacher_ID) REFERENCES Teacher(Teacher_ID)
);

-- COMPANY, LOCATIONS, JOBS
CREATE TABLE Company(
  Company_ID varchar(20),
  Company_Name varchar(100),
  PRIMARY KEY(Company_ID)
);

CREATE TABLE Company_Locations(
  Company_ID varchar(20),
  Company_Location varchar(255),
  PRIMARY KEY(Company_ID, Company_Location),
  FOREIGN KEY(Company_ID) REFERENCES Company(Company_ID)
);

CREATE TABLE Job(
  Job_ID varchar(20),
  Job_Name varchar(100),
  Job_description varchar(255),
  Parent_Company varchar(20),
  PRIMARY KEY(Job_ID,Parent_Company),
  FOREIGN KEY(Parent_Company) REFERENCES Company(Company_ID)
);

-- WORKS_ON TABLE
CREATE TABLE Works_On(
  SRN varchar(20),
  Company_ID varchar(20),
  Job_ID varchar(20),
  PRIMARY KEY(SRN,Company_ID,Job_ID),
  FOREIGN KEY(SRN) REFERENCES Student(SRN),
  FOREIGN KEY(Company_ID) REFERENCES Company(Company_ID),
  FOREIGN KEY(Job_ID) REFERENCES Job(Job_ID)
);

-- PROJECTS and PROJECT_GUIDE
CREATE TABLE Projects(
  Project_name varchar(200),
  Project_Year YEAR,
  PRIMARY KEY(Project_name),
  FULLTEXT KEY (Project_name)
);


CREATE TABLE Project_Guide(
  Student_SRN varchar(20),
  Project_name varchar(200),
  Teacher_ID varchar(20),
  PRIMARY KEY(Student_SRN,Project_name,Teacher_ID),
  FOREIGN KEY(Student_SRN) REFERENCES Student(SRN),
  FOREIGN KEY(Project_name) REFERENCES Projects(Project_name),
  FOREIGN KEY(Teacher_ID) REFERENCES Teacher(Teacher_ID)
);