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

## Technologies Used

| Technology | What It Does |
|-----------|-------------|
| Python 3 | The main programming language used to build everything |
| PostgreSQL | The database where all the student data is stored |
| psycopg2 | A Python library that connects Python to PostgreSQL |
| pandas | Helps with reading data from the database and organizing it |
| gspread | Lets Python read from and write to Google Sheets |
| oauth2client | Handles the login and permissions for Google API access |

## Project Structure

```
Student-Learning-Analytics-System/
|
|-- main.py                  - Runs the complete pipeline from start to finish
|-- ETL2.py                  - Has all the functions to read data and load it into the database
|-- reporting.py             - Creates performance reports and uploads them to Google Sheets
|-- requirements.txt         - List of Python packages you need to install
|-- StudentDetails.json      - Sample student information data
|-- PerformanceInput.json    - Sample test attempt records
|-- PerformanceMetrics.json  - Sample performance score data
|-- .gitignore               - Tells git which files to skip
|-- README.md                - This file you are reading right now
```

## Database Tables

The project uses four tables in the PostgreSQL database:

| Table Name | What It Stores |
|-----------|---------------|
| `student_details` | Basic student info like name, email, phone number, school, and grade |
| `performance_input` | Test attempt records â€” who submitted, when, and whether it was processed |
| `performance_metrics` | Performance scores â€” reading speed, pronunciation, fluency, and noise |
| `form_responces` | School registration information collected from a Google Form |

## How to Set Up and Run

### What You Need First
- Python 3 installed on your computer
- PostgreSQL installed and running
- A Google Cloud service account with Google Sheets API access enabled

### Steps to Get Started

1. **Download the project**
   ```
   git clone https://github.com/your-username/Student-Learning-Analytics-System.git
   cd Student-Learning-Analytics-System
   ```

2. **Install the required Python packages**
   ```
   pip install -r requirements.txt
   ```

3. **Set up the database**
   - Open PostgreSQL and create a new database called `analystmind`
   - Create the four tables mentioned above (student_details, performance_input, performance_metrics, form_responces)

4. **Update the configuration**
   - Open `ETL.py` and `reporting.py` in any text editor
   - Change the database password and file paths to match your computer setup
   - Add the correct path to your Google service account JSON key file

5. **Run the pipeline**
   ```
   python main.py
   ```
   This single command will load all the data and generate the reports automatically.

## Future Scope and Improvements

Here are some ideas and plans to make this project even better going forward:

- **Build a Visual Dashboard** â€” Right now the reports go to Google Sheets, but in the future we can build a proper dashboard using tools like Streamlit or Power BI. This would show the data with nice charts, graphs, and filters that make it much easier to understand at a glance.

- **Automate the Pipeline** â€” Instead of running the script manually, we can set up a scheduler (like cron jobs on Linux or Apache Airflow) so the pipeline runs on its own every day or every week without anyone needing to do anything.

- **Send Email Notifications** â€” The system could automatically send an email to school admins or teachers whenever a new report is ready. It could also send alerts if a student's performance drops below a certain level.

- **Connect More Data Sources** â€” Right now we only read from JSON files and one Google Form. In the future, we can connect to learning apps, attendance tracking systems, or other school platforms to get a more complete picture of how students are doing.

- **Generate Individual Student Reports** â€” Currently the reports are at the school and grade level. A useful improvement would be to create personal performance reports for each student, like a digital report card.

- **Add Data Validation** â€” Before loading data into the database, we can add checks to catch any missing fields, wrong formats, or unusual values. This makes sure the reports are always accurate.

- **Move to the Cloud** â€” The database and pipeline can be moved to cloud services like AWS, Google Cloud, or Azure. This would make the system more scalable and available from anywhere.

- **Track Performance Over Time** â€” By keeping historical data, schools can track trends over weeks and months. They can see if students are improving, staying the same, or falling behind.

- **Use Machine Learning for Predictions** â€” With enough data, we can train simple ML models to predict which students might struggle in the future. This way, teachers can step in early and give those students extra support before they fall behind.

## Contributing

If you would like to improve this project or add new features, feel free to fork the repository and submit a pull request. Any kind of contribution is welcome â€” whether it is fixing a bug, improving documentation, or adding something entirely new.

## License

This project is open source and available for educational purposes.
