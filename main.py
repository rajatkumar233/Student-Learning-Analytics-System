from ETL import load_students_details, load_performance_input, load_performance_metrics
from reporting import genrate_and_push_report

def run_pipeline():
    load_students_details()
    print("Students details loaded successfully")
    load_performance_input()
    print("Performance input loaded successfully")
    load_performance_metrics()
    print("Performance metrics loaded successfully")
    genrate_and_push_report()
    print("Report generated and pushed to google sheet successfully")

if __name__ == "__main__":
    run_pipeline()