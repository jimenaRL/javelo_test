import os
import json
import argparse

from perfManSer import Employee

from pprint import pprint

if __name__ == '__main__':

    input_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'data/input.json')

    output_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'data/output.json')

    with open(input_path, 'r') as f:
        data = json.load(f)

    employee = Employee()

    employee.add_objectives(data["objectives"])
    print("~~~ Objectives added ~~~")
    print(employee)

    employee.update_records(data["progress_records"])
    print("~~~ Records updated ~~~")
    print(employee)

    progress_records = employee.get_progress()
    with open(output_path, 'w') as f:
        data = json.dump(progress_records, f, indent=2)
