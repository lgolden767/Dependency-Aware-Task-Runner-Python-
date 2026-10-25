#README
LG - 2026-10-25

## Goal
Command line program that reads a JSON file detailing tasks/dependencies, then executes in a valid order 
*executing a task means printing its action for the purposes of this project*

### Example Input:
{
  "tasks": [
    {"id": "download", "depends_on": [], "action": "Downloading data"},
    {"id": "clean", "depends_on": ["download"], "action": "Cleaning data"},
    {"id": "report", "depends_on": ["clean"], "action": "Generating report"},
    {"id": "backup", "depends_on": ["download"], "action": "Backing up data"}
  ]
}

## Features
Accepts JSON file path through the command line.
Executes each task exactly once, after all its dependencies.
When several tasks are ready, choose the one whose ID comes first alphabetically.
Support --target ID to execute only that task and its direct and indirect dependencies.
Support --dry-run to print the execution order without executing actions.
Reject duplicate IDs, nonexistent dependencies, and malformed task definitions.
Detect dependency cycles and report an actual cycle, such as a -> b -> c -> a.
Validate the entire configuration before executing anything, even when using --target.
Keep parsing, validation, planning, and execution sufficiently separate that you can test them independently.

## Libraries
json
argparse
unittest

## Tests
branching dependencies
shared dependencies
target selection
alphabetical ordering
a cycle
and a missing dependency
