import json
import os
import pathlib as pl
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

    def test_read(self):
        self.assertTrue(str(tasks))

## ------------------------

def readJson(fp):
    with open(fp, "r") as file:
       tasks = file.read()

    return tasks

tasks = readJson(FILENAME)
obj = json.loads(tasks)
print(obj, ", TYPE:", type(obj))

if __name__ == '__main__':
    unittest.main()