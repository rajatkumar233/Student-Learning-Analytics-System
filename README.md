# Student Learning Analytics System

A simple data pipeline project that helps schools track and understand how their students are performing in reading and learning activities. It collects student data from different places, puts it all in one database, and creates useful performance reports.

## What This Project Does

In simple words, this project does the following things:

1. **Reads student data** from JSON files (student details, test attempts, and scores)
2. **Pulls school information** from a Google Form (through Google Sheets)
3. **Saves everything** into a PostgreSQL database in a clean and organized way
4. **Creates two reports**:
   - School-wise Report â€” shows how each school is doing overall
   - Grade-wise Report â€” shows how students in each grade are performing
5. **Uploads the reports** to Google Sheets so teachers and admins can easily see them

## How It Works (Step by Step)

This project follows the ETL approach â€” Extract, Transform, and Load:

```
JSON Files + Google Sheets --> Python Script --> PostgreSQL Database --> Reports --> Google Sheets
```

### Step 1: Getting the Data (Extract)
- Student info like name, contact number, school, and grade comes from `StudentDetails.json`
- Test attempt records (who submitted what, when, and what was the status) come from `PerformanceInput.json`
- Performance scores (reading speed, pronunciation, fluency) come from `PerformanceMetrics.json`
- School registration data is pulled from a Google Sheets form response

### Step 2: Saving to Database (Load)
- Each type of data is inserted into its own table in PostgreSQL
- If a record already exists in the database, it is simply skipped (no duplicate entries are created)

### Step 3: Creating Reports (Transform)
- SQL queries combine data from all four tables
- The system calculates averages for important metrics:
  - Words per minute (WPM) â€” how fast a student reads
  - Correct words per minute (WCPM) â€” how accurately a student reads
  - Pronunciation score â€” how well a student pronounces words
  - Fluency score â€” how smoothly a student reads
- Reports are generated at both the school level and grade level

### Step 4: Sharing Reports
- The finished reports are automatically uploaded to Google Sheets
- Anyone with access to the Google Sheet can view the latest performance numbers
