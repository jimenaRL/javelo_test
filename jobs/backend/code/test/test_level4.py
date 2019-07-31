import unittest
from perfManSer import (
    TreeEmployee,
    NodeObjective
)


class ObjectiveTest(unittest.TestCase):

    def setUp(self):
        self.input = {
            "objectives": [
                {"id": 1, "start": 0, "target": 50, "start_date": "2018-01-05", "end_date": "2018-03-05", "parent_id": 4, "weight": 1},
                {"id": 2, "start": 10, "target": 42, "start_date": "2018-01-25", "end_date": "2018-03-30", "parent_id": 4, "weight": 1},
                {"id": 3, "start": 20, "target": 0, "start_date": "2018-02-05", "end_date": "2018-03-05", "parent_id": 5, "weight": 4},
                {"id": 4, "parent_id": 5, "weight": 1},
                {"id": 5, "parent_id": 6, "weight": 2},
                {"id": 6}
            ],
            "progress_records": [
                {"id": 1, "objective_id": 1, "value": 15, "date": "2018-01-12"},
                {"id": 2, "objective_id": 3, "value": 10, "date": "2018-02-20"},
                {"id": 3, "objective_id": 2, "value": 14, "date": "2018-02-18"},
                {"id": 4, "objective_id": 4, "value": 14, "date": "2018-02-18"},
                {"id": 5, "objective_id": 5, "value": 14, "date": "2018-02-18"},
                {"id": 6, "objective_id": 6, "value": 14, "date": "2018-02-18"}
            ],
            "milestones": [
                {"id": 1, "objective_id": 1, "target": 14, "date": "2018-01-10"},
                {"id": 2, "objective_id": 2, "target": 13, "date": "2018-01-25"},
                {"id": 3, "objective_id": 2, "target": 30, "date": "2018-02-15"},
                {"id": 4, "objective_id": 2, "target": 40, "date": "2018-03-10"},
                {"id": 5, "objective_id": 3, "target": 10, "date": "2018-02-15"},
                {"id": 6, "objective_id": 3, "target": 2, "date": "2018-02-25"}
            ]
        }

        self.expected_output = {
            "progress_records": [
                {
                    "id": 1,
                    "excess": -2
                },
                {
                    "id": 2,
                    "excess": -29
                },
                {
                    "id": 3,
                    "excess": -81
                },
                {
                    "id": 4,
                    "excess": -71
                },
                {
                    "id": 5,
                    "excess": -21
                },
                {
                    "id": 6,
                    "excess": -21
                }
            ]
        }

    def testLeafNodeObjective(self):
        obj = self.input["objectives"][0]
        p_rec = self.input["progress_records"][0]
        exp_out = self.expected_output["progress_records"][0]

        objective = NodeObjective(obj)

        objective.update(p_rec)
        self.assertTrue(objective.date == p_rec["date"])

        excess = objective.excess()
        self.assertTrue(excess == exp_out["excess"])

    def testRootNodeObjective(self):
        obj = self.input["objectives"][-1]
        p_rec = self.input["progress_records"][-1]
        exp_out = self.expected_output["progress_records"][-1]

        objective = NodeObjective(obj)

        objective.update(p_rec)
        self.assertTrue(objective.date == p_rec["date"])

        excess = objective.excess()
        self.assertTrue(excess == exp_out["excess"])


    def testTreeEmployee(self):
        employee = TreeEmployee()

        # test employee creation
        employee.add_node_objectives(self.input["objectives"])
        self.assertTrue(
            all([isinstance(obj, NodeObjective)
                 for obj in employee.objectives.values()]))

        # test progress_records addition
        employee.update_records(self.input["progress_records"])

        # test milestone addition
        employee.add_milestones_from_records(self.input["milestones"])
        for i in employee.objectives.keys():
            a = [_ for _ in self.input['milestones'] if _['objective_id'] == i]
            b = employee.objectives[i].milestones
            self.assertTrue(len(a) + 2 == len(b))

        out_prog_recs = employee.get_excess()
        self.assertTrue(isinstance(out_prog_recs, dict))
        for eo in out_prog_recs["progress_records"]:
            for o in self.expected_output["progress_records"]:
                if eo["id"] == o["id"]:
                    self.assertEqual(eo["excess"], o["excess"])

if __name__ == '__main__':
    unittest.main()
