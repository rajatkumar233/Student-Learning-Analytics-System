import psycopg2
import json

def get_connection():
        return psycopg2.connect(
                dbname='analystmind',
                user='postgres',
                password=1234,
                host='localhost',
                port=5432
        )

def load_students_details():
        conn = get_connection()
        cursor = conn.cursor()
        with open(r"F:\Youtube\ANALYST MIND Project 1\ Student Learning Analytics System Project\StudentDetails.json") as f:
                data = json.load(f)
                for row in data:
                        cursor.execute("""INSERT INTO student_details (id,name,contact_number,email_id,school_id,grade)
                                    values(%s,%s,%s,%s,%s,%s) on conflict (id) do nothing""",
                                    (
                                        row.get('id'),
                                        row.get('name'),
                                        row.get('contact_number'),
                                        row.get('email_id'),
                                        row.get('school_id'),
                                        row.get('grade')
                                    )
                        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Data loaded successfully into students table")
