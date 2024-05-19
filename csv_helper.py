import csv
from io import StringIO

CSV_FILE_PATH = 'jerseys.csv'
print(CSV_FILE_PATH) 
def read_csv():
    with open(CSV_FILE_PATH, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def append_to_csv(row):
    with open('jerseys.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=row.keys())
        writer.writerow(row)

def write_csv(rows):
    if rows:
        with open('jerseys.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)