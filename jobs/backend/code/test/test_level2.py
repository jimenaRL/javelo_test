import unittest
from perfManSer import (
    Employee,
    LinearObjective
)


class ObjectiveTest(unittest.TestCase):

    def setUp(self):
        self.input = {
            "objectives": [
                {"id": 1, "start": 0, "target": 50, "start_date": "2018-01-05", "end_date": "2018-03-05"},
                {"id": 4, "start": 0, "target": 100, "start_date": "2018-02-01", "end_date": "2018-02-11"},
                {"id": 5, "start": 0, "target": 100, "start_date": "2018-02-01", "end_date": "2018-02-11"}
            ],
            "progress_records": [
                {"id": 1, "objective_id": 1, "value": 15, "date": "2018-01-12"},
                {"id": 4, "objective_id": 4, "value": 50, "date": "2018-02-06"},
                {"id": 5, "objective_id": 5, "value": 25, "date": "2018-02-06"},
            ]
        }

        self.expected_output = {
            "progress_records": [
                {
                    "id": 1,
                    "excess": 153
                },
                {
                    "id": 4,
                    "excess": 0
                },
                {
                    "id": 5,
                    "excess": -25
                }
            ]
        }

    def testLinearObjective(self):
        # test objective creation
        obj = self.input["objectives"][0]
        p_rec = self.input["progress_records"][0]
        exp_out = self.expected_output["progress_records"][0]

        objective = LinearObjective(obj)

        objective.update(p_rec)
        self.assertEqual(objective.date, p_rec["date"])

        excess = objective.excess()
        self.assertEqual(excess, exp_out["excess"])

    def testEmployee(self):
        employee = Employee()

        # test employee creation
        employee.add_l_objectives(self.input["objectives"])
        self.assertTrue(
            all([isinstance(obj, LinearObjective)
                 for obj in employee.objectives.values()]))

        # test progress_records addition
        employee.update_records(self.input["progress_records"])
        out_prog_recs = employee.get_excess()

        self.assertTrue(isinstance(out_prog_recs, dict))
        for eo in out_prog_recs["progress_records"]:
            for o in self.expected_output["progress_records"]:
                if eo["id"] == o["id"]:
                    self.assertEqual(eo["excess"], o["excess"])


if __name__ == '__main__':
    unittest.main()
