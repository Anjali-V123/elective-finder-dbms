# elective-finder-dbms


# Elective Finder – DBMS Project

This project is a **Database Management Systems (DBMS)** course project that helps students choose suitable electives based on interests, past projects, alumni outcomes, and preferences.

The system uses:  
- **MySQL** for database storage  
- **Python** for backend logic  
- **Streamlit** for the frontend interface  

> Note: This was developed as a **team project** as part of a DBMS course.

---

## Features

### Alumni Module
- Enter alumni details (SRN, name, graduation year)  
- Provide elective feedback and grades  
- Add projects worked on with mentors  
- Add companies and job roles  

### Student Module
- Semester-wise elective selection  
- Select interests (up to 3)  
- Add past projects  
- Choose dream companies and job roles  
- Set preferences (difficulty, class size, teacher)  
- Generate **top 3 elective recommendations** using a weighted scoring system  
- View results with charts and tables  

---

## Recommendation Logic (Overview)

Electives are scored based on:  
- Interests (higher weight)  
- Past projects  
- Alumni job outcomes  
- Preferred teacher  
- Difficulty level  
- Class size preference  

The electives with the highest scores are recommended.

---

## Project Structure

app.py # Streamlit frontend
python_connector.py # MySQL database connector
schema.sql # Database schema (DDL)
data.sql # Sample data (DML)
README.md


## How to Run

1. Set up MySQL and run:
sql
SOURCE schema.sql;
SOURCE data.sql;

Update database credentials in python_connector.py if needed.

Run the app:
  streamlit run app.py


Tech Stack

1)MySQL
2)Python
3)Streamlit
4)mysql-connector-python
5)Pandas, Matplotlib
