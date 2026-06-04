import psycopg2
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials 

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



        
def load_performance_input():
        conn = get_connection()
        curr = conn.cursor()

        with open(r"F:\Youtube\ANALYST MIND Project 1\ Student Learning Analytics System Project\PerformanceInput.json") as f:
            data = json.load(f)

            for row in data:
                curr.execute("""INSERT INTO performance_input (attempt_id,child_id,school_id,submitted_at,status)
                            values(%s,%s,%s,%s,%s) on conflict (attempt_id) do nothing""",
                            (
                                row.get('id'),
                                row.get('child_id'),
                                row.get('school_id'),
                                row.get('submitted_at'),
                                row.get('status')
                            )
                )
        conn.commit()
        curr.close()
        conn.close()
        print("Data loaded successfully into performance_input table")
    

def load_performance_metrics():
    conn = get_connection()
    curr = conn.cursor()
    with open(r"F:\Youtube\ANALYST MIND Project 1\ Student Learning Analytics System Project\PerformanceMetrics.json") as f:
        data = json.load(f)
        for row in data:
              curr.execute("""INSERT INTO performance_metrics (metric_id,input_id,processed_date,wpm,wcpm,pronunciation,fluency,noise)
                           values(%s,%s,%s,%s,%s,%s,%s,%s) on conflict (metric_id) do nothing""",
                           (
                                row.get('id'),
                                row.get('input_id'),
                                row.get('processed_date'),
                                row.get('wpm'),
                                row.get('wcpm'),
                                row.get('pronunciation'),
                                row.get('fluency'),
                                row.get('noise')
                                )
                                )
    conn.commit()
    curr.close()
    conn.close()
    print("Data loaded successfully into performance_metrics table")


def load_from_response():
    conn = get_connection()
    curr = conn.cursor()
    gc = gspread.service_account(filename=r"F:\Youtube\ANALYST MIND Project 1\ Student Learning Analytics System Project\gcp-tutorial-youtube-4390926df4a7.json")
    sh = gc.open_by_key('18v6ozMouLO6IDrc8Jc76DfQ4P2AZz0kbUqqB0Stg3CY')
    worksheet = sh.worksheet('FormResponse')

    data = worksheet.get_all_records()
    for row in data:
        curr.execute("""INSERT INTO form_responces (form_submission_date,school_id,school_name,city,state,contact_number,email_id,no_of_students)
                    values(%s,%s,%s,%s,%s,%s,%s,%s) on conflict (school_id) do nothing""",
                    (
                        row.get('form_submission_date'),
                        row.get('school_id'),
                        row.get('school_name'),
                        row.get('city'),
                        row.get('state'),
                        row.get('contact_number'),
                        row.get('email_id'),
                        row.get('no_of_students')
                    )
        )
    conn.commit()
    curr.close()
    conn.close()
    print("Data loaded successfully from google sheet into form_responces table")

load_from_response()
