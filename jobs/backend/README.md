# Javelo Backend Challenge

## Guidelines

**For each level, write code that creates a new `data/output.json` file from the data in `data/input.json`. An `expected_output.json` file is available to give you a reference on what result is expected.**

- Clone this repo (do **not** fork it)
- Solve the levels in ascending order
- Only do one commit per level

### Pointers

You can have a look at the higher levels, but please do the simplest thing that could work for the level you're currently solving.

The levels become more complex over time, so you will probably have to re-use some code and adapt it to the new requirements.
A good way to solve this is by using OOP, adding new layers of abstraction when they become necessary and possibly write tests so you don't break what you have already done.

Don't hesitate to write [shameless code](http://red-badger.com/blog/2014/08/20/i-spent-3-days-with-sandi-metz-heres-what-i-learned/) at first, and then refactor it in the next levels.

For higher levels we are interested in seeing code that is:
- clean
- extensible
- robust (don't overlook edge cases, use exceptions where needed, ...)

Please also note that:
- running `$ ruby main.rb` from the level folder should generate the desired output, but of course feel free to add more files if needed.

### Sending Your Results

- You should already be in contact with us, don't hesitate to ask if something seems wrong
- When you are done, send the link of your repository to the person you are talking to

## Challenge

### Intro

We are building a performance managment service for companies. We will focus on the strategy aspect.
A company's strategy is defined by objectives. An objective is a goal with a theoric progress of amount of work defined over time.

Here is our plan:
- Let any employee save their objectives on our platform
- Let any employee check an objective's real progress at any given date and compare it to what's expected

Example of a real life objective:
```JSON
{
  "id": 17548,
  "title": "Make 50 blank tests to be trained for the javelo challenge",
  "start": 0,
  "start_date": "2017-12-01",
  "end_date": "2018-09-31",
  "target": 50,
  "unit": "number"
}
```

### Level 1: Progress

An employee sets the starting and target values of each objective (`start` and `target`). They represent the amount of work to be done on this objective. On any day, they can record how close they are from the target of an objective.

A record's `progress` is the percentage of amount of work to be done represented by its `value`.

### Level 2: Progress Over Time

An employee also sets the days interval of their objectives (`start_date` and `end_date`).
Let's improve the user experience, and provide the employee with a progress chart. The horizontal axis represents time, and the vertical axis represents the amount of work done.
The progression model of the objective is the segment defined by the (`start_date`, `start`) and (`end_date`, `target`) points, representing the expected amount of work done over time.

An employee can record their progression on the chart at any date between start and end dates. They then can compare how far a record is from the expected amount of work done at that date.

At a record's date, `excess` is in percentage of the expected amount of work done, the difference between:
- the value of the record
- the expected amount of work done

### Level 3: Milestones

The linear progression model of the previous level isn't always enough to express what should happen between start and end dates. In order to provide flexibility on our platform, an employee can set milestones on their objectives. A milestone is a point on the progress chart through which the progression model passes. This makes the progression model piecewise linear, i.e. composed of multiple segments.

At a record's date, `excess` is in percentage of the expected amount of work done, the difference between:
- the value of the record
- the expected amount of work done

### Level 4: Objective Tree & Weighted Mean Progress

To better define a company's strategy, it is sometimes useful to organize objectives in a tree. An employee can set a `parent_id` on their objectives. The `parent_id` of an objective is its parent objective's `id`. An employee can also set a `weight` on a child objective.

The `start` and `target` values of a parent objective are each the computed weighted mean of its children's.
At a specific date, the expected amount of work done of a parent objective is the computed weighted mean of its children's.

At a record's date, `excess` is in percentage of the expected amount of work done, the difference between:
- the value of the record
- the expected amount of work done
