import csv
from io import StringIO

CSV_FILE_PATH = 'jerseys.csv'
print(CSV_FILE_PATH) 
def read_csv():
    with open(CSV_FILE_PATH, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_csv(data):
    fieldnames = ['id', 'name', 'team', 'league', 'type', 'home_away_third', 'size', 'number_of_jerseys', 'price', 'customizable', 'discounted_price']
    with open(CSV_FILE_PATH, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_to_csv(row):
    fieldnames = ['id', 'name', 'team', 'league', 'type', 'home_away_third', 'size', 'number_of_jerseys', 'price', 'customizable', 'discounted_price']
    with open(CSV_FILE_PATH, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(row)
