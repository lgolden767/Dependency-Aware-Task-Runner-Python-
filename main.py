import json
import os
import pathlib as pl
from ordered_set import OrderedSet
import argparse
import unittest

DIRNAME  = os.path.dirname(__file__)
FILENAME = os.path.join(DIRNAME, "Data/tasks.json")

## ------- TESTS ----------

class TestBaseCase(unittest.TestCase):
    def assertIsFile(self, path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File path does not exist: %s" % str(path))

class ActualTest(TestBaseCase):
    def test_filepath(self):
        path = pl.Path(FILENAME)
        self.assertIsFile(path)

    def test_todo(self):
        self.assertTrue(isinstance(parseJson(FILENAME), list))

## ------------------------

def readJson(fp):
    with open(fp, "r") as file:
       tasks = file.read()

    output = json.loads(tasks)
    return output

def parseJson(filepath):
    tasks = readJson(filepath)

    out = []

    for task in tasks:
        for item in tasks[task]:
            out.append(item)
    return out

def orderTasks(tasks):
    tempTasks = sorted(tasks, key=lambda d: d["id"])
    sortedTasks = []

    for task in tempTasks:
        if task['depends_on'] == []:
            sortedTasks.append(task)
            tempTasks.remove(task)

    while len(tempTasks) > 0:
        for task in tempTasks:
            deps = set(task['depends_on'])
            existing = set()
            for e in sortedTasks:
                existing.add(e['id'])
            if deps.issubset(existing):
                sortedTasks.append(task)
                tempTasks.remove(task)

    return sortedTasks

def executeTasks(tasks):
    for task in tasks:
        print(task['action'], '\n')

tasks        = parseJson(FILENAME)
orderedTasks = orderTasks(tasks)
executeTasks(orderedTasks)

if __name__ == '__main__':
    unittest.main()