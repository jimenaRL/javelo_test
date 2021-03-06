import os
import json
import argparse

from perfManSer import TreeEmployee

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

    pprint(data)

    employee = TreeEmployee()

    employee.add_node_objectives(data["objectives"])
    print("~~~ Objectives added ~~~")
    employee.print_tree()

    employee.add_milestones_from_records(data["milestones"])
    print("~~~ Milestone added ~~~")
    employee.print_tree()

    employee.update_records(data["progress_records"])
    print("~~~ Records updated ~~~")
    employee.print_tree()

    excess_records = employee.get_excess()
    with open(output_path, 'w') as f:
        data = json.dump(excess_records, f, indent=2)
