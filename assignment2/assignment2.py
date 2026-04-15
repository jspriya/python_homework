import traceback
import csv
import sys
import os
import custom_module
from datetime import datetime

# Task2

def read_employees():
    emp_dict = {}
    emp_list = []

    try:
        with open('../csv/employees.csv', mode='r') as file:
            reader = csv.reader(file)

            for i, row in enumerate(reader):
                if i == 0:
                    emp_dict["fields"] = row  # first row = headers
                else:
                    emp_list.append(row)     

        emp_dict["rows"] = emp_list
        return emp_dict
    
    except FileNotFoundError:
        print("Error: Could not find the file")
        sys.exit(1)    

employees = read_employees()

# Task 3
def column_index(column_name):
    return employees["fields"].index(column_name)

employee_id_column = column_index("employee_id")

# Task 4
def first_name(row_number):
    index = column_index("first_name")
    return employees["rows"][row_number][index]

f_name = first_name(2)

# Task 5
def employee_find(employee_id):

    def employee_match(row):
        return int(row[employee_id_column]) == employee_id

    matches = list(filter(employee_match, employees["rows"]))
    return matches

# matched_row = employee_find(2)

#Task 6
def employee_find_2(employee_id):
   matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id , employees["rows"]))
   return matches

#Task 7
def sort_by_last_name():
    index = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[index])   
    return employees["rows"]

sort_by_last_name()
print(employees)

#Task 8
def employee_dict(row):
    result = {}

    for field, value in zip(employees["fields"], row):
        if field != "employee_id":
            result[field] = value

    return result
print(employee_dict(employees["rows"][0]))

#Task 9
def all_employees_dict():
    result = {}
    index = column_index("employee_id")

    for row in employees["rows"]:
        emp_id = row[index]
        result[emp_id] = employee_dict(row)

    return result
print(all_employees_dict())

#Task 10
def get_this_value():
    return os.getenv("THISVALUE")

# Task 11
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

set_that_secret("what_secret")
print(custom_module.secret)

# Task 12
def read_csv_to_dict(file_path):
    result = {}
    rows_list = []

    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)

            for i, row in enumerate(reader):
                if i == 0:
                    result["fields"] = row
                else:
                    rows_list.append(tuple(row))  # convert to tuple

        result["rows"] = rows_list
        return result

    except Exception as e:
        print("Error reading file:", e)
        sys.exit(1)

def read_minutes():
    minutes1 = read_csv_to_dict("../csv/minutes1.csv")
    minutes2 = read_csv_to_dict("../csv/minutes2.csv")

    return minutes1, minutes2

minutes1, minutes2 = read_minutes()

#Task 13

def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])

    combined = set1 | set2
    return combined

minutes_set = create_minutes_set()
print(minutes_set)

# Task 14
def create_minutes_list():
    temp_list = list(minutes_set)

    result = list(map(
        lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")),
        temp_list
    ))

    return result

minutes_list = create_minutes_list()
print(minutes_list)

# Task 15
def write_sorted_list():
    # Sort by datetime 
    sorted_list = sorted(minutes_list, key=lambda x: x[1])

    # Convert datetime back to string
    converted_list = list(map(
        lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")),
        sorted_list
    ))

    # Write to CSV file
    with open("./minutes.csv", "w", newline="") as file:
        writer = csv.writer(file)

        # header row from minutes1
        writer.writerow(minutes1["fields"])

        # data rows
        for row in converted_list:
            writer.writerow(row)

    # Return result
    return converted_list

final_minutes = write_sorted_list()
print(final_minutes)