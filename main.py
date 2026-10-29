import json
import os
import pathlib as pl
from ordered_set import OrderedSet
import argparse
import unittest

## ------- TESTS ----------

TEST_FILE = pl.Path(__file__).resolve().parent / "Data" / "tasks.json"

class MainTest(unittest.TestCase):
    def testReadJson(self):
        testFile = readJson(TEST_FILE)
        self.assertTrue(isinstance(testFile, dict))

    def testParseJson(self):
        newFile  = parseJson(TEST_FILE)
        self.assertNotEqual(readJson(TEST_FILE), newFile)

    def testOrderTasks(self):
        newFile  = parseJson(TEST_FILE)
        self.assertNotEqual(newFile, orderTasks(newFile))

    def testOrderedTasks(self):
        newFile  = parseJson(TEST_FILE)
        testOrderedTasks = orderTasks(newFile)
        self.assertEqual(
            testOrderedTasks[0],
            {
                "id": "archive",
                "depends_on": [],
                "action": "Archiving previous results"
            }
        )

    def testCheckDependencies(self):
        testDependencies = checkDependencies("download", TEST_FILE)
        self.assertEqual(testDependencies, [])

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


    for item in out:
        idx = out.index(item)

        for i in (0, len(out) - 1):
            if i == idx:
                continue
            else:
                if out[i] == item:
                    out.remove(out[i])

    return out

def orderTasks(tasks):
    remaining = sorted(tasks, key=lambda task: task["id"])
    ordered = []
    completed = set()

    while remaining:
        for task in remaining:
            if set(task['depends_on']).issubset(completed):
                ordered.append(task)
                completed.add(task['id'])
                remaining.remove(task)
                break

    return ordered

def checkDependencies(task, ts):
    tasks        = parseJson(ts)
    orderedTasks = orderTasks(tasks)

    out = []

    for e in orderedTasks:
        if e["id"] == task:
            out.extend(e['depends_on'])

    return out

def executeTask(task, fp):
    tasks = parseJson(fp)
    orderedTasks = orderTasks(tasks)

    d   = []
    ids = set()

    
    for item in orderedTasks:
        if item["id"] == task:
            d.append(item)

    while d != []:
        for item in d.copy():
            r = frozenset((key, tuple(value) if isinstance(value, list) else value) for key, value in item.items())
            ids.add(r)
            d.remove(item)
        for item in ids:
            i = dict(item)
            for dep in i['depends_on']:
                if dep not in {dict(task)["id"] for task in ids}:
                    for t in orderedTasks:
                        if t['id'] == dep:
                            d.append(t)

    unorderedOut = []
    out = []

    for id in ids:
        unorderedOut.append(dict(id))

    for id in unorderedOut:
        tempDict = {'id': id['id'], 'depends_on': list(id['depends_on']), 'action': id['action']}
        out.append(tempDict)
    return out


def executeTasks(tasks, mode='f'):
    if (mode == 'f'):
        t = parseJson(tasks)
        orderedTasks = orderTasks(t)
    elif (mode == 'l'):
        orderedTasks = orderTasks(tasks)

    for task in orderedTasks:
        print(task['action'].title(), '\n')

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="Please state the filepath to the task JSON. If you encounter errors due to spaces, place the arg in quotes.")
parser.add_argument("-t", "--target", help="-target ID; executes task with given ID and its dependencies only")
parser.add_argument("-dr", "--dryrun", help="Print the execution order without executing actions")
args = parser.parse_args()

if args.target:
    targetList = executeTask(args.target, args.filepath)
    executeTasks(targetList, 'l')
elif args.dryrun:
    dryrunList = executeTask(args.dryrun, args.filepath)
    orderedDryrunList = orderTasks(dryrunList)
    for e in orderedDryrunList:
        print(e['id'].title(), '\n')
else:
    executeTasks(args.filepath)

if __name__ == '__main__':
    unittest.main(argv=["main.py"])