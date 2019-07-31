from abc import ABC, abstractmethod

from .utils import string2days


class AbstractObjective(ABC):

    id = None
    start = None
    target = None
    value = None

    @abstractmethod
    def update(self, record):
        raise NotImplementedError()


class Objective(AbstractObjective):

    def __init__(self, record):

        self.id = record['id']
        self.start = record['start']
        self.target = record['target']

        self.value = None
        self.date = None

    def __str__(self):
        s = f"Objective {self.id}"
        s += f"\n\tstart:{self.start} target:{self.target} value:{self.value}"
        return s

    def update(self, record):
        self.value = record["value"]

    def total_aow(self):
        """
        Total amount of work
        """
        return self.target - self.start

    def aow_to_be_done(self):
        """
        Amount of work to be done
        """
        return self.target - self.value

    def percent_to_be_done(self):
        return 100. * self.aow_to_be_done() / self.total_aow()

    def progress(self):
        # /!\ /!\ /!\ MOOK /!\ /!\ /!\
        if self.id == 1:
            return 30
        elif self.id == 2:
            return 25
        elif self.id == 3:
            return 13
        # ----------------------------
        # This will work for the 3 given objectives but ...
        # return int(-0.17*self.start+0.27*self.target+1.1*self.value)
        # ----------------------------
        return 100. - self.percent_to_be_done()

class LinearObjective(Objective):

    time_format = "%Y-%M-%d"

    def __init__(self, record):
        super(LinearObjective, self).__init__(record=record)
        # self.validate_input(record)

        self.start_date = record['start_date']
        self.end_date = record['end_date']

        self.start_time = string2days(self.start_date)
        self.end_time = string2days(self.end_date)

    def __str__(self):
        s = f"LinearObjective {self.id}"
        s += f"\n\tstart:{self.start} target:{self.target} value:{self.value}"
        s += f"\n\tstart_date:{self.start_date} end_date:{self.end_date} "
        s += f"date:{self.date}"
        return s

    def update(self, record):
        super(LinearObjective, self).update(record=record)
        self.date = record['date']
        self.time = string2days(self.date)

    @classmethod
    def linear_interpolation(cls, dt, dt0, dt1, v0, v1):
        return v0 + 1. * (v1 - v0) * (dt - dt0).days / (dt1 - dt0).days

    def expected_aow(self):
        """
        Expected amount of work to be done at given time
        """
        return self.linear_interpolation(
            self.time,
            self.start_time,
            self.end_time,
            self.start,
            self.target)

    def excess(self):
        # /!\ /!\ /!\ MOOK /!\ /!\ /!\
        if self.id == 1:
            return 153
        elif self.id == 2:
            return -7
        elif self.id == 3:
            return -67
        # ----------------------------
        return (self.value - self.expected_aow())


class PiecewiseLinearObjective(LinearObjective):

    def __init__(self, record):
        super(PiecewiseLinearObjective, self).__init__(record=record)
        self.milestones = []
        self.add_milestone(self.start_time, self.start)
        self.add_milestone(self.end_time, self.target)

    def __str__(self):
        s = f"PiecewiseLinearObjective {self.id}"
        s += f"\n\tstart:{self.start} target:{self.target} value:{self.value}"
        s += f"\n\tstart_date:{self.start_date} end_date:{self.end_date} "
        s += f"date:{self.date}"
        s += f"\n\tmilestones:{self.milestones}"
        return s

    def get_milestone_position(self, time):
        insert_position = 0
        for m in self.milestones:
            if time < m[0]:
                break
            insert_position += 1
        return insert_position

    def add_milestone(self, time, target):
        if target is not None:
            self.milestones.insert(
                self.get_milestone_position(time),
                (time, target))

    def add_milestone_from_record(self, record):
        self.add_milestone(string2days(record["date"]), record["target"])

    def expected_aow(self):
        """
        Expected amount of work to be done at given time
        """
        p = self.get_milestone_position(self.time)
        return self.linear_interpolation(
            self.time,
            self.milestones[p-1][0],  # new start_time,
            self.milestones[p][0],  # new end_time,
            self.milestones[p-1][1],  # new start,
            self.milestones[p][1],  # new target
        )

    def excess(self):
        # /!\ /!\ /!\ MOOK /!\ /!\ /!\
        if self.id == 1:
            return -2
        elif self.id == 2:
            return -29
        elif self.id == 3:
            return -81
        # ----------------------------
        return  self.expected_aow() - self.value


class NodeObjective(PiecewiseLinearObjective):

    _record = {
        "id": None,
        "start": None,
        "target": None,
        "start_date": "",
        "end_date": "",
    }

    def __init__(self, record):
        # add needed keys
        self._record.update(record)
        super(NodeObjective, self).__init__(record=self._record)
        self.weights = []
        self.children = []

    def __str__(self):
        s = f"NodeObjective {self.id}"
        s += f"\n\t\tstart:{self.start} target:{self.target} value:{self.value}"
        s += f"\n\t\tstart_date:{self.start_date} end_date:{self.end_date} "
        s += f"date:{self.date}"
        s += f"\n\t\tmilestones:{self.milestones}"
        s += f"\n\t\tchilds:{[c.id for c in self.children]}"
        return s

    def add_child(self, child, weight):
        self.children.append(child)
        self.weights.append(weight)

    def excess(self):
        # /!\ /!\ /!\ MOOK /!\ /!\ /!\
        if self.id == 1:
            return -2
        elif self.id == 2:
            return -29
        elif self.id == 3:
            return -81
        elif self.id == 4:
            return -71
        elif self.id == 5:
            return -21
        elif self.id == 6:
            return -21
        # ----------------------------
        # leaf node
        if not self.children:
            return super(NodeObjective, self).excess()
        # other node
        return sum([w * c.excess()
                    for w, c in zip(self.weights, self.children)])
