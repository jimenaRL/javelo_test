from .objectives import (
    Objective,
    LinearObjective,
    PiecewiseLinearObjective,
    NodeObjective
)

from .utils import walk_tree_bf


class Employee(object):

    def __init__(self):
        self.objectives = {}

    def __str__(self):
        s = f"Employee\n"
        s += '\n\t\n'.join([str(obj) for obj in self.objectives.values()])
        return s

    def show_objectives(self):
        for obj in self.objectives.values():
            print(obj)

    def add_pl_objectives(self, records):
        for r in records:
            obj = PiecewiseLinearObjective(r)
            self.objectives[obj.id] = obj

    def add_l_objectives(self, records):
        for r in records:
            obj = LinearObjective(r)
            self.objectives[obj.id] = obj

    def add_objectives(self, records):
        for r in records:
            obj = Objective(r)
            self.objectives[obj.id] = obj

    def add_milestones_from_records(self, records):
        for r in records:
            self.objectives[r["objective_id"]].add_milestone_from_record(r)

    def update_records(self, records):
        for r in records:
            self.objectives[r["objective_id"]].update(r)

    def get_progress(self):
        return {"progress_records": [
            {"id": obj.id, "progress": obj.progress()}
            for obj in self.objectives.values()]}

    def get_excess(self):
        return {"progress_records": [
            {"id": obj.id, "excess": obj.excess()}
            for obj in self.objectives.values()]}


class TreeEmployee(Employee):

    def __init__(self):
        super(TreeEmployee, self).__init__()
        self.root = None

    def __str__(self):
        s = f"TreeEmployee\n"
        s += 'Root: {}'.format(self.root.id)
        return s

    def print_tree(self):
        walk_tree_bf(self.root, print)

    def add_node_objectives(self, records):
        # find root
        for n, r in enumerate(records):
            if ("parent_id" not in r):
                self.root = NodeObjective(r)
                self.root_record = records.pop(n)
                self.objectives[self.root.id] = self.root
                break

        # add leaves
        to_visit = [(self.root, self.root_record)]
        while to_visit:
            new_to_visit = []
            for node, record in to_visit:
                records_to_visit = [r for r in records if r["parent_id"] == node.id]
                nodes_to_visit = []
                weights = []
                for r in records_to_visit:
                    n = NodeObjective(r)
                    nodes_to_visit.append(n)
                    weights.append(r["weight"])
                to_visit = zip(nodes_to_visit, records_to_visit)
                for n, w in zip(nodes_to_visit, weights):
                    node.add_child(n, w)
                new_to_visit.extend(to_visit)
            to_visit = new_to_visit

    def add_milestones_from_records(self, records):
        def visit(n):
            for r in records:
                if n.id == r["objective_id"]:
                    n.add_milestone_from_record(r)
        walk_tree_bf(self.root, visit)

    def update_records(self, records):
        def visit(n):
            for r in records:
                if n.id == r["objective_id"]:
                    n.update(r)
        walk_tree_bf(self.root, visit)

    def get_excess(self):
        objectives_list = []
        def visit(n):
            objectives_list.append(n)
        walk_tree_bf(self.root, visit)
        return {"progress_records": [
            {"id": obj.id, "excess": obj.excess()}
            for obj in objectives_list]}
