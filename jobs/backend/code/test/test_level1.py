import unittest
from perfManSer import (
    Employee,
    Objective
)


class ObjectiveTest(unittest.TestCase):

    def setUp(self):
        self.input = {
            "objectives": [
                {"id": 1, "start": 0, "target": 50},
                {"id": 4, "start": 30, "target": 50},
                {"id": 5, "start": 0, "target": 50}
            ],
            "progress_records": [
                {"id": 1, "objective_id": 1, "value": 15},
                {"id": 4, "objective_id": 4, "value": 30},
                {"id": 5, "objective_id": 5, "value": 30}
            ]
        }

        self.expected_output = {
            "progress_records": [
                {
                    "id": 1,
                    "progress": 30
                },
                {
                    "id": 4,
                    "progress": 0
                },
                {
                    "id": 5,
                    "progress": 60
                }
                ]
        }

    def testObjective(self):
        # test objective creation
        obj = self.input["objectives"][0]
        p_rec = self.input["progress_records"][0]
        exp_out = self.expected_output["progress_records"][0]

        objective = Objective(obj)
        self.assertTrue(isinstance(objective.id, int))
        self.assertTrue(isinstance(objective.start, int))
        self.assertTrue(isinstance(objective.target, int))

        objective.update(p_rec)
        self.assertEqual(objective.value, p_rec["value"])

        self.assertTrue(objective.total_aow(), 50)
        self.assertEqual(objective.aow_to_be_done(), 35)

        progress = objective.progress()
        self.assertTrue(progress == exp_out["progress"])

    def testEmployee(self):
        employee = Employee()

        # test employee creation
        employee.add_objectives(self.input["objectives"])
        self.assertTrue(
            all([isinstance(obj, Objective)
                for obj in employee.objectives.values()]))

        # test progress_records addition
        employee.update_records(self.input["progress_records"])
        out_prog_recs = employee.get_progress()

        self.assertTrue(isinstance(out_prog_recs, dict))
        for eo in out_prog_recs["progress_records"]:
            for o in self.expected_output["progress_records"]:
                if eo["id"] == o["id"]:
                    self.assertEqual(eo["progress"], o["progress"])


if __name__ == '__main__':
    unittest.main()
