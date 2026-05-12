import mysql.connector


# ================= Database Connection =================
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="devKUMAR@1234",
        database="srms_db"
    )


# ================= Create Database =================
def create_database():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="devKUMAR@1234"
    )

    cur = con.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS srms_db")

    con.commit()
    con.close()


# ================= Create Course Table =================
def create_course():
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
            cid INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            duration VARCHAR(50),
            charges DECIMAL(10,2),
            description TEXT
        )
    """)

    con.commit()
    con.close()


# ================= Create Student Table =================
def create_student():
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS student(
            roll VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            gender VARCHAR(20),
            dob VARCHAR(50),
            contact VARCHAR(20),
            admission VARCHAR(50),
            course VARCHAR(100),
            state VARCHAR(100),
            city VARCHAR(100),
            pin VARCHAR(20),
            address TEXT
        )
    """)

    con.commit()
    con.close()


# ================= Create Result Table =================
def create_result():
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS result(
            rid INT PRIMARY KEY AUTO_INCREMENT,
            roll VARCHAR(10),
            name VARCHAR(100),
            course VARCHAR(100),
            marks_ob DECIMAL(10,2),
            full_marks DECIMAL(10,2),
            percent DECIMAL(10,2)
        )
    """)

    con.commit()
    con.close()


# ================= Create Teacher Table =================
def create_teacher():
    con = connect_db()
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS teacher")
    cur.execute("""
        CREATE TABLE teacher(
            tid      INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name     VARCHAR(100) NOT NULL,
            contact  VARCHAR(20),
            email    VARCHAR(100) NOT NULL UNIQUE,
            question VARCHAR(200),
            answer   VARCHAR(100),
            password VARCHAR(100) NOT NULL
        )
    """)

    con.commit()
    con.close()


# ================= Run All =================
create_database()
create_course()
create_student()
create_result()
create_teacher()

print("Database and Tables Created Successfully")