# Notes

Code tested on python 3.6.8.

### Install

You can either:

- Source the bash script `set_env.sh` within the `/path/to/your/folder/jobs/backend` folder to update your PYTHONPATH.
- Install the package `perfManSer` in your home directory with `python setup.py install` within the `/path/to/your/folder/jobs/backend/code` folder.

### Usage

To generate all ouputs you may source the bash script `generate_ouputs.sh` in `/path/to/your/folder/jobs/backend/code`.


### Tests
To generate run all tests you may source the bash script `run_tests.sh` in `/path/to/your/folder/jobs/backend/code`.

### TO DO:

- Remove mooks of course.

- Do a proper class for milestones in PiecewiseLinearObjective or replace them
with LinearObjective instances.

- There is maybe something ugly about how the Employee class stores its
objectives, it could be a mix of several classe, maybe each objective subclass
should be in a separate structure.


