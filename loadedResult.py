import psycopg2
import json
import gspread
import pandas as pd

def generate_and_push_report():
    conn = psycopg2.connect(
        dbname = 'Project',
        user = 'postgres',
        password = 'password',
        host = 'localhost',
        port = 5432
    )

    Schoolwise_report = """SELECT  fr.school_id,fr.school_name,fr.no_of_students as registred_users, 
        count(distinct(ci.id)) as cmf_submitted, 
        count(DISTINCT case when ci.status ='Processed' THEN ci.id end) as cmf_sucessful,
        ROUND(cast(AVG(cm.wpm)as numeric),2) AS avg_wpm,
        ROUND(cast(AVG(cm.wcpm)as numeric),2) AS avg_wcpm,
        ROUND(cast(AVG(cm.pronunciation)as numeric),2) AS avg_pronunciation,
        ROUND(cast(AVG(cm.fluency)as numeric),2) AS avg_fluency
        FROM student_detail as sd 
        LEFT JOIN performance_input as ci
        ON sd.id = ci.child_id
        LEFT JOIN perform_matrices as cm
        ON cm.input_Id = ci.id
        LEFT JOIN form_responces as fr
        ON fr.school_id = sd.school_id
        GROUP BY 1,2,3;
    ;"""
    grade_wise_report = """SELECT
        s.grade,
        COUNT(DISTINCT i.child_Id) AS registered_users,
        COUNT(DISTINCT i.id) AS cmf_submitted,
        COUNT(DISTINCT CASE 
            WHEN i.status = 'Processed' THEN i.id 
        END) AS cmf_successful,
        AVG(m.wpm) AS avg_wpm,
        AVG(m.wcpm) AS avg_wcpm,
        AVG(m.pronunciation) AS avg_pronunciation,
        AVG(m.fluency) AS avg_fluency
        FROM student_detail s
        LEFT JOIN performance_input i
        ON s.id = i.child_id
        LEFT JOIN perform_matrices m
        ON i.id = m.input_id
        LEFT JOIN form_responces as fr
        ON fr.school_id = s.school_id
        GROUP BY s.grade
        ORDER BY s.grade;"""
    
    df_school = pd.read_sql_query(
        Schoolwise_report,
        conn
    )
    df_grade = pd.read_sql_query(
        grade_wise_report,
        conn
    )

    conn.close()
    
    output_file = "loadedResult.xlsx"
    with pd.ExcelWriter(output_file,engine="openpyxl")as writer:
        df_school.to_excel(writer,sheet_name="school",index=False)
        df_grade.to_excel(writer,sheet_name="grade",index=False)
    
    #print(f"report saved successfully: {output_file}")
    print("report saved successfully:")


generate_and_push_report()




import psycopg2
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials 
import pandas as pd

def genrate_and_push_report():
        conn = psycopg2.connect(
                dbname='analystmind',
                user='postgres',
                password=1234,
                host='localhost',
                port=5432
        )
        
        Schoolwise_report = """SELECT  fr.school_id,fr.school_name,fr.no_of_students as registred_users, 
        count(distinct(ci.attempt_id)) as cmf_submitted, 
        count(DISTINCT case when ci.status ='Processed' THEN ci.attempt_id end) as cmf_sucessful,
        ROUND(cast(AVG(cm.wpm)as numeric),2) AS avg_wpm,
        ROUND(cast(AVG(cm.wcpm)as numeric),2) AS avg_wcpm,
        ROUND(cast(AVG(cm.pronunciation)as numeric),2) AS avg_pronunciation,
        ROUND(cast(AVG(cm.fluency)as numeric),2) AS avg_fluency
        FROM student_details as sd 
        LEFT JOIN performance_input as ci
        ON sd.id = ci.child_id
        LEFT JOIN performance_metrics as cm
        ON cm.input_Id = ci.attempt_id
        LEFT JOIN form_responces as fr
        ON fr.school_id = sd.school_id
        GROUP BY 1,2,3;"""
        grade_wise_report = """
        SELECT
        s.grade,
        COUNT(DISTINCT i.child_Id) AS registered_users,
        COUNT(DISTINCT i.attempt_id) AS cmf_submitted,

        COUNT(DISTINCT CASE 
            WHEN i.status = 'Processed' THEN i.attempt_id 
        END) AS cmf_successful,

        AVG(m.wpm) AS avg_wpm,
        AVG(m.wcpm) AS avg_wcpm,
        AVG(m.pronunciation) AS avg_pronunciation,
        AVG(m.fluency) AS avg_fluency
        FROM student_details s
        LEFT JOIN performance_input i
        ON s.id = i.child_id
        LEFT JOIN performance_metrics m
        ON i.attempt_id = m.input_id
        LEFT JOIN form_responces as fr
        ON fr.school_id = s.school_id
        GROUP BY s.grade
        ORDER BY s.grade;"""

        df_school_wise_report = pd.read_sql_query(Schoolwise_report,conn)
        df_grade_wise_report = pd.read_sql_query(grade_wise_report,conn)
        conn.close()

        #converting to string
        df_school_wise_report = df_school_wise_report.astype(str)
        df_grade_wise_report = df_grade_wise_report.astype(str)

        #googel sheet setup
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(r"F:\Youtube\ANALYST MIND Project 1\ Student Learning Analytics System Project\gcp-tutorial-youtube-4390926df4a7.json", scope)
        client = gspread.authorize(creds)
        #open the googel sheet and select worksheet
        ws = client.open_by_key("1w3JI1lDyAOKIF4fam2feqDGIbbLugOE0RpVOK6itYnk").worksheet("School_wise_report")
        ws.clear()
        #update the worksheet with new data
        ws.update([df_school_wise_report.columns.values.tolist()] + df_school_wise_report.values.tolist())
        print("School wise report updated successfully in google sheet")
        #update the gradewise report
        ws_grade = client.open_by_key("1w3JI1lDyAOKIF4fam2feqDGIbbLugOE0RpVOK6itYnk").worksheet("gradewise_report")
        ws_grade.clear()
        ws_grade.update([df_grade_wise_report.columns.values.tolist()] + df_grade_wise_report.values.tolist())
        print("Grade wise report updated successfully in google sheet") 


genrate_and_push_report()
