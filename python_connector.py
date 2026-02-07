# python_connector.py
# Updated connector with semester-aware queries.

import mysql.connector
from mysql.connector import errorcode
import os

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="electives",
        autocommit=False
    )

def get_cursor(conn):
    return conn.cursor(buffered=True, dictionary=True)

# ---------------------------
# Basic helper functions
# ---------------------------

def get_elective_semester(course_id):
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        cur.execute("SELECT Semester FROM Elective WHERE Course_ID = %s", (course_id,))
        row = cur.fetchone()
        return row['Semester'] if row else None
    finally:
        cur.close()
        conn.close()

def retrieve_electives(semester=None):
    """
    If semester is provided (int), returns electives for that semester.
    Otherwise returns all electives.
    Returns list of dicts with Course_ID, Course_Name, Syllabus, Semester, Class_Size, Difficulty
    """
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        if semester:
            cur.execute("""
                SELECT Course_ID, Course_Name, Syllabus, Semester, Class_Size, Difficulty
                FROM Elective
                WHERE Semester = %s
            """, (semester,))
        else:
            cur.execute("""
                SELECT Course_ID, Course_Name, Syllabus, Semester, Class_Size, Difficulty
                FROM Elective
            """)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

# ---------------------------
# Alumni insert helpers
# ---------------------------

def insert_alumni_details(srn, student_name, dob, graduated_year):
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        sql = """
        INSERT INTO Student (SRN, Student_Name, DOB, Graduated_year)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE Student_Name=VALUES(Student_Name), DOB=VALUES(DOB), Graduated_year=VALUES(Graduated_year)
        """
        cur.execute(sql, (srn, student_name, dob, graduated_year))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def insert_alumni_elective_details(srn, elective_name, feedback, grade):
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        cur.execute("SELECT Course_ID FROM Elective WHERE Course_Name = %s", (elective_name,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Elective not found")
        course_id = row['Course_ID']
        cur.execute("""
            INSERT INTO Belongs_To (SRN, Course_ID, feedback, grade)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE feedback=VALUES(feedback), grade=VALUES(grade)
        """, (srn, course_id, feedback, grade))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def insert_alumni_project_details(srn, project_name, teacher_name, project_year=None):
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        # ensure project exists
        if project_year:
            cur.execute("INSERT IGNORE INTO Projects (Project_name, Project_Year) VALUES (%s, %s)",
                        (project_name, project_year))
        else:
            cur.execute("INSERT IGNORE INTO Projects (Project_name) VALUES (%s)", (project_name,))

        # find teacher id
        cur.execute("SELECT Teacher_ID FROM Teacher WHERE Teacher_Name = %s", (teacher_name,))
        t = cur.fetchone()
        if not t:
            raise ValueError("Teacher not found")
        teacher_id = t['Teacher_ID']

        cur.execute("""
            INSERT IGNORE INTO Project_Guide (Student_SRN, Project_name, Teacher_ID)
            VALUES (%s, %s, %s)
        """, (srn, project_name, teacher_id))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def insert_alumni_job_details(srn, company_name, job_name):
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        cur.execute("SELECT Company_ID FROM Company WHERE Company_Name = %s", (company_name,))
        c = cur.fetchone()
        if not c:
            raise ValueError("Company not found")
        company_id = c['Company_ID']
        cur.execute("SELECT Job_ID FROM Job WHERE Job_Name = %s AND Parent_Company = %s", (job_name, company_id))
        j = cur.fetchone()
        if not j:
            raise ValueError("Job not found for that company")
        job_id = j['Job_ID']
        cur.execute("""
            INSERT IGNORE INTO Works_On (SRN, Company_ID, Job_ID)
            VALUES (%s, %s, %s)
        """, (srn, company_id, job_id))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

# ---------------------------
# Student scoring: semester-aware retrievals
# ---------------------------

def retrieve_top_projects_by_interest(interest, limit=5):
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        try:
            cur.callproc("interest_matcher_project", (interest,))
            results = []
            for res in cur.stored_results():
                results.extend(res.fetchall())
            return results[:limit]
        except Exception:
            cur.execute("""
                SELECT Project_name, Project_Year,
                       MATCH(Project_name) AGAINST (%s IN NATURAL LANGUAGE MODE) AS score
                FROM Projects
                WHERE MATCH(Project_name) AGAINST (%s IN NATURAL LANGUAGE MODE)
                ORDER BY score DESC LIMIT %s
            """, (interest, interest, limit))
            return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def retrieve_top_electives_by_interest(interest, semester, limit=5):
    """
    Uses fulltext match on Syllabus but only returns electives from 'semester'
    """
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        cur.execute("""
            SELECT Course_ID, Course_Name,
                   MATCH(Syllabus) AGAINST (%s IN NATURAL LANGUAGE MODE) AS score
            FROM Elective
            WHERE MATCH(Syllabus) AGAINST (%s IN NATURAL LANGUAGE MODE)
              AND Semester = %s
            ORDER BY score DESC
            LIMIT %s
        """, (interest, interest, semester, limit))
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def retrieve_top_projects_by_pastproject(pastproject, limit=5):
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        try:
            cur.callproc("pastproject_matcher_project", (pastproject,))
            results = []
            for res in cur.stored_results():
                results.extend(res.fetchall())
            return results[:limit]
        except Exception:
            cur.execute("""
                SELECT Project_name, Project_Year,
                       MATCH(Project_name) AGAINST (%s IN NATURAL LANGUAGE MODE) AS score
                FROM Projects
                WHERE MATCH(Project_name) AGAINST (%s IN NATURAL LANGUAGE MODE)
                ORDER BY score DESC LIMIT %s
            """, (pastproject, pastproject, limit))
            return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def retrieve_top_electives_by_pastproject(pastproject, semester, limit=5):
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        cur.execute("""
            SELECT Course_ID, Course_Name,
                   MATCH(Syllabus) AGAINST (%s IN NATURAL LANGUAGE MODE) AS score
            FROM Elective
            WHERE MATCH(Syllabus) AGAINST (%s IN NATURAL LANGUAGE MODE)
              AND Semester = %s
            ORDER BY score DESC
            LIMIT %s
        """, (pastproject, pastproject, semester, limit))
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def electives_by_teacher(teacher_name, semester=None):
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        cur.execute("SELECT Teacher_ID FROM Teacher WHERE Teacher_Name = %s", (teacher_name,))
        t = cur.fetchone()
        if not t:
            return []
        teacher_id = t['Teacher_ID']
        if semester:
            cur.execute("""
                SELECT e.Course_ID, e.Course_Name
                FROM Elective e
                JOIN Taught_By tb ON e.Course_ID = tb.Course_ID
                WHERE tb.Teacher_ID = %s AND e.Semester = %s
            """, (teacher_id, semester))
        else:
            cur.execute("""
                SELECT e.Course_ID, e.Course_Name
                FROM Elective e
                JOIN Taught_By tb ON e.Course_ID = tb.Course_ID
                WHERE tb.Teacher_ID = %s
            """, (teacher_id,))
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def electives_based_on_jobs(company_name, job_name, semester=None):
    """
    Returns electives (Course_ID, Course_Name, alumni_count) that alumni who worked in (company,job) belonged to.
    Filter by semester if provided.
    """
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        cur.execute("SELECT Company_ID FROM Company WHERE Company_Name = %s", (company_name,))
        c = cur.fetchone()
        if not c:
            return []
        company_id = c['Company_ID']
        cur.execute("SELECT Job_ID FROM Job WHERE Job_Name = %s AND Parent_Company = %s", (job_name, company_id))
        j = cur.fetchone()
        if not j:
            return []
        job_id = j['Job_ID']
        if semester:
            cur.execute("""
                SELECT e.Course_ID, e.Course_Name, COUNT(*) AS alumni_count
                FROM Elective e
                JOIN Belongs_To b ON e.Course_ID = b.Course_ID
                WHERE b.SRN IN (
                  SELECT w.SRN FROM Works_On w
                  WHERE w.Company_ID = %s AND w.Job_ID = %s
                ) AND e.Semester = %s
                GROUP BY e.Course_ID, e.Course_Name
                ORDER BY alumni_count DESC LIMIT 10
            """, (company_id, job_id, semester))
        else:
            cur.execute("""
                SELECT e.Course_ID, e.Course_Name, COUNT(*) AS alumni_count
                FROM Elective e
                JOIN Belongs_To b ON e.Course_ID = b.Course_ID
                WHERE b.SRN IN (
                  SELECT w.SRN FROM Works_On w
                  WHERE w.Company_ID = %s AND w.Job_ID = %s
                )
                GROUP BY e.Course_ID, e.Course_Name
                ORDER BY alumni_count DESC LIMIT 10
            """, (company_id, job_id))
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def electives_by_difficulty(difficulty_level, semester=None):
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        if semester:
            cur.execute("SELECT Course_ID, Course_Name FROM Elective WHERE Difficulty = %s AND Semester = %s",
                        (difficulty_level, semester))
        else:
            cur.execute("SELECT Course_ID, Course_Name FROM Elective WHERE Difficulty = %s", (difficulty_level,))
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def electives_by_class_size_range(min_size, max_size, semester=None):
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        if semester:
            cur.execute("""
                SELECT Course_ID, Course_Name
                FROM Elective
                WHERE CAST(Class_Size AS SIGNED) BETWEEN %s AND %s
                  AND Semester = %s
            """, (min_size, max_size, semester))
        else:
            cur.execute("""
                SELECT Course_ID, Course_Name
                FROM Elective
                WHERE CAST(Class_Size AS SIGNED) BETWEEN %s AND %s
            """, (min_size, max_size))
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

# ---------------------------
# Utility: fetch teacher list, company list, job list
# ---------------------------

def all_teacher_names():
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        cur.execute("SELECT Teacher_Name FROM Teacher ORDER BY Teacher_Name")
        return [r['Teacher_Name'] for r in cur.fetchall()]
    finally:
        cur.close()
        conn.close()

def all_company_names():
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        cur.execute("SELECT Company_Name FROM Company ORDER BY Company_Name")
        return [r['Company_Name'] for r in cur.fetchall()]
    finally:
        cur.close()
        conn.close()

def job_names_for_company(company_name):
    conn = get_connection()
    cur = get_cursor(conn)
    try:
        cur.execute("SELECT Company_ID FROM Company WHERE Company_Name = %s", (company_name,))
        c = cur.fetchone()
        if not c:
            return []
        cur.execute("SELECT Job_Name FROM Job WHERE Parent_Company = %s", (c['Company_ID'],))
        return [r['Job_Name'] for r in cur.fetchall()]
    finally:
        cur.close()
        conn.close()