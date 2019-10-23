import csv


sample_customers = [[123456, 'Jeff Bezos', '1234', 100000.0], [987654, 'Derrick Zoolander', '2468', 2.50],
                    [246810, 'Rustin Cohle', '1010', 100.0], [135791, 'Devin Booker', '7070', 0.0]]

sample_employees = [[777777, 'Michael Scott (emp)', '9999', 0.0, '1111']]

with open('customers.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for c in sample_customers:
        writer.writerow(c)


with open('employees.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for c in sample_employees:
        writer.writerow(c)



