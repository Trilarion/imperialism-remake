# Simple Taskboard
# Copyright (C) 2014 Trilarion
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""
    Manages the database of tasks, sorts them into four different lists (available, blocked, progress, completed).
    Load and save from/to JSON used for display in the Javascript powered HTML site (web/index).
    Does some basic consistency checks. Can create a backup file for safety. See the example functions for help how
    to use it.

    You can add a new task, assign it and complete it. That's all. It's not intended to delete tasks or to reopen them,
    although one could manually do all this.

    IDs of tasks are running numbers.
"""

import json, shutil, os, itertools
from datetime import date

# minimal set of keys that have to be set in the boards properties
min_board_keys = set(['pageTitle', 'categories'])
# maximal set of keys that can be set in the boards properties
max_board_keys = min_board_keys | set([])
# minimal set of keys that have to be set in a task
min_task_keys = set(['id', 'creationDate', 'dependencies', 'title', 'description', 'category'])
# maximal set of keys that can be set in a task
max_task_keys = min_task_keys | set(['assignee', 'assignDate', 'completionDate', 'result', 'dependencies'])
# standard file name
default_file_name = 'board-content.json';

class Task():
    """
        A single task, basically not much more than a dictionary.
    """
    def __init__(self, id):
        self.properties = {}
        self['id'] = id
        self['creationDate'] = date.today().isoformat()
        self['dependencies'] = []

    def __getitem__(self, item):
        return self.properties[item]

    def __setitem__(self, key, value):
        self.properties[key] = value

    def assign(self, assignee, assignDate=date.today().isoformat()):
        self['assignee'] = assignee
        self['assignDate'] = assignDate

    def complete(self, result, completionDate=date.today().isoformat()):
        self['result'] = result
        self['completionDate'] = completionDate


class Board():
    """
        The task board. Holds all the tasks in one list. Sorting into the four lists (available, blocked, ...) is
        only done before saving. Also has soem additonal properties in a dictionary.
    """

    def __init__(self):
        self.properties = {}
        self.tasks = []

    def __getitem__(self, item):

        return self.properties[item]

    def __setitem__(self, key, value):
        self.properties[key] = value

    def __iter__(self):
        """
            Yields all the tasks.
        """
        for task in self.tasks:
            yield task

    def new_task(self, title, description, category) -> Task:
        """
            Given a title, description and category (number 1 : len(self.properties['categories']) constructs a new
            task. All the parameters are necessary.

            :return: The new task which is also appended to the taswk list.
        """
        id = len(self.tasks) + 1
        task = Task(id)
        task['title'] = title
        task['description'] = description
        task['category'] = category
        self.tasks.append(task)
        return task

def save_board(board, file_name=default_file_name):
    """
        Saves the board to a JSON file. First performs some safety checks. Then sorts the tasks into the four lists:
        available, blocked, in progress, completed, then converts everything into a big dictionary, then serialize it
        and save it to a file.
    """

    # safety check
    if not (board.properties.keys() >= min_board_keys and board.properties.keys() <= max_board_keys):
        raise RuntimeError('board either contains not enough properties or too many')
    for task in board:
        if not (task.properties.keys() >= min_task_keys and task.properties.keys() <= max_task_keys):
            raise RuntimeError('a task either contains not enough properties or too many')
    for (k, task) in enumerate(board.tasks):
        if task['id'] != k + 1: # id starts at 1
            raise RuntimeError('id is not consistent with task order in tasks list')

    # collect all internal data

    # properties goes to properties
    data = {}
    data['properties'] = board.properties.copy()

    # sort into available, blocked, in progress, completed
    unworked = []
    progress = []
    completed = []

    for task in board:
        p = task.properties.copy()
        if 'assignee' not in p:
            unworked.append(p)
        else:
            if 'completionDate' not in p:
                progress.append(p)
            else:
                completed.append(p)

    # sorting of unworked into available and blocked
    available = []
    blocked = []
    for task in unworked:
        # if this task depends on any task not completed, move it to blocked
        block_criteria = any([t['id'] in task['dependencies'] for t in itertools.chain(unworked, progress) if t is not task])
        if block_criteria:
            blocked.append(task)
        else:
            available.append(task)

    # sort by id
    available.sort(key=lambda x: x['id'])
    blocked.sort(key=lambda x: x['id'])
    progress.sort(key=lambda x: x['id'])
    completed.sort(key=lambda x: x['id'])

    # sort by category
    available.sort(key=lambda x: x['category'])
    blocked.sort(key=lambda x: x['category'])
    progress.sort(key=lambda x: x['category'])
    completed.sort(key=lambda x: x['category'])

    data['available'] = available
    data['blocked'] = blocked
    data['progress'] = progress
    data['completed'] = completed

    # serialize to json and dump to file
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=2, separators=(',', ': '))

def load_board(file_name=default_file_name):
    """
        Deserialize the JSON file and create a board from it. No real checks are performed (these are done before saving).
        Combines all the tasks from the four lists again in one list of tasks (easier to manipulate here).
    """

    # read from file and deserialize
    with open(file_name, 'r') as file:
        data = json.load(file)

    # just create board and tasks and copy the underlying properties into them bluntly
    board = Board()
    board.properties = data['properties']
    tasks = []
    for properties in itertools.chain(data['available'], data['blocked'], data['progress'], data['completed']):
        task = Task(0)
        task.properties = properties
        tasks.append(task)

    # sort by id
    tasks.sort(key=lambda x: x['id'])

    board.tasks = tasks
    return board

def create_backup(file_name=default_file_name):
    """
        Simple copying, still useful in case you make an error.
    """
    shutil.copyfile(file_name, file_name + '.backup')



def example_backup_and_add_tasks():
    """
        Makes a backup of the current board, then load it, add some tasks and saves it again.
    """

    # create a backup
    create_backup()

    # load the board
    board = load_board()

    # add a task (should be available)
    task = board.new_task(title='Clean the house', description='Everywhere', category=1)

    # add another (should be in progress)
    task = board.new_task('Wash the car', "It's dirty", 2)
    task.assign('Jim')
    id_carwash = task['id']

    # and another (should be available)
    task = board.new_task('Trim the lawn', "It's time again", 2)

    # and another (should be completed)
    task = board.new_task('Buy more soap', "Really urgent.", 3)
    task.assign('John')
    task.complete("Bought soap with perfume, hope it's okay.")
    id_soap = task['id']

    # and another (should be available because not assigned and dependent on a completed)
    task = board.new_task('Clean the bathroom.', 'You need soap for it.', 3)
    task['dependencies'].extend([id_soap])

    # and another (should be blocking)
    task = board.new_task('Drive around with clean car', 'Just enjoy.', 2)
    task['dependencies'].extend([id_carwash])
    id_drivearound = task['id']

    # and another (blocking again)
    task = board.new_task('Come home again', 'No description needed', 1)
    task['dependencies'].extend([id_carwash, id_drivearound])

    # and another one (available)
    task = board.new_task('Listen to some really good music', 'One should do it more often', 1)

    # write to file
    save_board(board)


if __name__ == '__main__':

    # create a backup
    create_backup()

    # load the board
    board = load_board()

    task = board.new_task(title='Bring Python version of the game roughly to the state of the last Java version', description='The last Java version (0.1.4) \
had a functional start screen, a preliminary editor showing a map and a game center dialog allowing to choose a scenario. All these features will very likely \
be part of the final game design because they are so essential. In order to release a Python version a Python version with roughly the same features should be \
created. This will attract attention to the project and allows us to test the Python release pathways. Do not include more features for now but rather break them \
down to individual tasks later.', category=3)
    task.assign('Trilarion')

    # write to file
    save_board(board)