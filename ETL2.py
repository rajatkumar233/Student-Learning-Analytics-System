import psycopg2
import json
import gspread
import pandas as pd


def get_connection2():
    return psycopg2.connect(
            dbname = 'Project',
            user = 'postgres',
            password = 'password',
            host = 'localhost',
            port = 5432
    )


#get_connection2()


def load_student_details():
        conn = get_connection2()
        cursor = conn.cursor()
        with open(r"C:\Users\rajat\OneDrive\Desktop\Project\ETL_Pipeline\Dataset\Student Learning Analytics System Project-20260524T152332Z-3-001\ Student Learning Analytics System Project\StudentDetails.json") as p:
                data = json.load(p)
                for row in data:
                        cursor.execute("""Insert into student_detail (id,name,contact_number,email_id,school_id,grade)
                                       values(%s,%s,%s,%s,%s,%s) on conflict (id)do nothing""",
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

#load_student_details()


def load_performance_input():
    conn = get_connection2()
    curr = conn.cursor()

    with open(r"C:\Users\rajat\OneDrive\Desktop\Project\ETL_Pipeline\Dataset\Student Learning Analytics System Project-20260524T152332Z-3-001\ Student Learning Analytics System Project\PerformanceInput.json")as f :
        data = json.load(f)

        for row in data:
            curr.execute(
                """insert into performance_input(id,child_id,school_id,submitted_at,status)
                values(%s,%s,%s,%s,%s)on conflict (id) do nothing""",
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
    print("data loaded successfully into performance_input table")
            
#load_performance_input()


def load_performance_matrix():
    conn = get_connection2()
    curr = conn.cursor()

    with open(r"C:\Users\rajat\OneDrive\Desktop\Project\ETL_Pipeline\Dataset\Student Learning Analytics System Project-20260524T152332Z-3-001\ Student Learning Analytics System Project\PerformanceMetrics.json")as f :
        data = json.load(f)

        for row in data:
            curr.execute(
                """insert into perform_matrices(id,input_id,processed_date,wpm,wcpm,pronunciation,fluency,noise)
                values(%s,%s,%s,%s,%s,%s,%s,%s)on conflict (id) do nothing""",
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
    print("data loaded successfully into performance_matirx table")
            
#load_performance_matrix()


def load_form_responses():
    conn = get_connection2()
    cursor = conn.cursor()

    path = r"C:\Users\rajat\OneDrive\Desktop\Project\ETL_Pipeline\Dataset\Student Learning Analytics System Project-20260524T152332Z-3-001\ Student Learning Analytics System Project\Analyst_Mind_Project 1.xlsx"

    df = pd.read_excel(path,sheet_name='FormResponse')
    inserted = 0

    for _,row in df.iterrows():
        cursor.execute("""INSERT INTO form_responces
            (
                form_submission_date,
                school_id,
                school_name,
                city,
                state,
                contact_number,
                email_id,
                no_of_students
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (school_id) DO NOTHING
            """,
            (
                row["form_submission_date"],
                row["school_id"],
                row["school_name"],
                row["city"],
                row["state"],
                str(row["contact_number"]),
                row["email_id"],
                int(row["no_of_students"])
                
            ))
        inserted += cursor.rowcount
        print("Rows in Excel:", len(df))
        print("Rows inserted:", inserted)
            
        conn.commit()
        cursor.close()
        conn.close()

        print("formresponse data load successfully")


load_form_responses()
#path = r"C:\Users\rajat\OneDrive\Desktop\Project\ETL_Pipeline\Dataset\Student Learning Analytics System Project-20260524T152332Z-3-001\ Student Learning Analytics System Project\Analyst_Mind_Project 1.xlsx"

#df = pd.read_excel(path,sheet_name='FormResponse')

#print(df.shape)
#print(df["school_id"].nunique())
#print(df["school_id"].head(10))
#print(df["school_id"].unique())

#for sid in df["school_id"]:
# print(sid)
