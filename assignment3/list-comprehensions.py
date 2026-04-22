import csv

# Read csv file into list of lists
employees = []
with open("../csv/employees.csv",newline="") as file:
    reader = csv.reader(file)
    employees = list(reader)

# Create list of employee names, skip header row
names = [
    row[0] + " " + row[1]
    for row in employees[1:]
]

print(names)

# Create list of names with letter 'e'
names_contain_e =[
    name for name in names
    if "e" in name
]

print(names_contain_e)


