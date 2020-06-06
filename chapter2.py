import sys
import hashlib
import json
from datetime import datetime
from collections import OrderedDict


class TaskList:
    """'List' is actually an OrderedDict"""

    def __init__(self, filename):
        self.filename = filename
        self.task_dict = self.load_tasks()

    def load_tasks(self):
        # Loads tasks from json file (keeps order)
        try:
            file = open(self.filename)
        except FileNotFoundError:
            return OrderedDict()

        try:
            tasks_json = json.load(file)  # list of dictionaries
            task_list = [Task(task) for task in tasks_json]  # list of Tasks
            task_dict = OrderedDict((task.hash, task) for task in task_list)
            return task_dict
        except (json.JSONDecodeError, ValueError):
            # override default error msg
            error_msg = f"{self.filename} is corrupted"\
                        " - requested action was not performed"
            raise json.JSONDecodeError(error_msg)

    def save_tasks(self):
        # Serialize, sort and save Tasks to a file.
        json_list = [task.serialized_task() for task in self.task_dict.values()]
        # Sort by date string. It actually works because of choosen format
        json_list.sort(key=lambda x: x['date'] if x['date'] else '0', reverse=True)
        # actual save to file
        with open(self.filename, 'w') as file:
            json.dump(json_list, file)

    def get_task(self, hash):
        if not self.task_dict.get(hash):
            raise KeyError(f"Task with provided hash: {hash} doesn't exist.")
        return self.task_dict.get(hash)

    def new_task(self, task):
        self.task_dict[task.hash] = task
        self.save_tasks()

    def delete_task(self, hash):
        del self.task_dict[hash]
        self.save_tasks()

    def filter(self, keyword):
        valid_keywords = {
            'today': self._filter_today,
            'all': self._filter_all,
            'expired': self._filter_expired,
            'active': self._filter_active
        }
        filter_function = valid_keywords.get(keyword)
        if not filter_function:
            error_msg = f"Invalid filter: {keyword}!"\
                        f" Valid filters: {list(valid_keywords.keys())}"
            raise KeyError(error_msg)
        filter_function()

    def _filter_today(self):
        valid_tasks = []
        for hash, task in self.task_dict.items():
            if task.date and task.date.date() == datetime.today().date():
                valid_tasks.append((hash, task))
        self.task_dict = OrderedDict(valid_tasks)

    def _filter_all(self):
        pass

    def _filter_expired(self):
        valid_tasks = []
        for hash, task in self.task_dict.items():
            if task.date and task.date < datetime.today():
                valid_tasks.append((hash, task))
        self.task_dict = OrderedDict(valid_tasks)

    def _filter_active(self):
        valid_tasks = []
        for hash, task in self.task_dict.items():
            if task.date and task.date > datetime.today():
                valid_tasks.append((hash, task))
        self.task_dict = OrderedDict(valid_tasks)


class Task:
    date_format = '%Y-%m-%d %H:%M'

    def __init__(self, task_dict):
        self.name = task_dict.get('name')
        self.description = task_dict.get('description')
        self.date_string = task_dict.get('date')
        self.date = task_dict.get('date')  # datetime
        self._create_id_hash()

    def __str__(self):
        return f"Task: {self.name} {self.description} {self.date} {self.hash}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Task's name can't be empty.")
        self._name = name

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date_str):
        if not date_str:
            self._date = date_str
            return

        try:
            date = datetime.strptime(date_str, self.date_format)
            self._date = date
        except ValueError:
            # override default error msg
            now_str = datetime.strftime(datetime.now(), self.date_format)
            error_msg = f"Wrong date format: 'Y-m-d H:M'. Example: '{now_str}'"
            raise ValueError(error_msg)

    def _create_id_hash(self):
        str_to_hash = f"Task: {self.name} {self.description} {self.date}"
        hash = hashlib.md5()
        hash.update(str_to_hash.encode())
        self.hash = hash.hexdigest()

    def serialized_task(self):
        """Returns dictionary ready for json serialization """
        task_json = {
            'name': self.name,
            'description': self.description,
            'date': self.date_string
        }
        return task_json

    def updated_task(self, arg_dict):
        """
        Updates empty values of arg_dict and returns it.
        ISSUES: User can't change date to None, DRY violation,
        edit with hash and without arguments will result in success message
        """
        name = arg_dict['name']
        arg_dict['name'] = name if name else self.name
        date = arg_dict['date']
        arg_dict['date'] = date if date else self.date_string
        desc = arg_dict['description']
        arg_dict['description'] = desc if desc else self.description
        return arg_dict


def _create_arg_dict(arg_list):
    """Creates dictionary with keys and values of provided arguments"""
    arg_dict = {
        'action': arg_list[1],
        'name': None,
        'date': None,
        'description': None
    }
    arg_list = arg_list[2:]  # removes filename and action value

    # args have to be passed in pairs : arg_name <space> value
    # if len(arg_list) is odd then user provided either hash or display filter
    if len(arg_list) % 2:
        arg_dict['odd_argument'] = arg_list[0]
        arg_list = arg_list[1:]
    # assign values to keys in arg_dict
    for i in range(0, len(arg_list), 2):
        if arg_list[i] in arg_dict:
            key = arg_list[i]
            value = arg_list[i+1]
            arg_dict[key] = value
    return arg_dict


def _validate_action(action):
    valid_actions = {'add', 'delete', 'edit', 'display', 'help'}
    if action not in valid_actions:
        raise ValueError(f'Wrong action - possible actions: {valid_actions}')


def add(arg_dict, task_list):
    new_task = Task(arg_dict)
    task_list.new_task(new_task)
    print(f'New task added succesfully!\n{new_task}')


def delete(arg_dict, task_list):
    hash = arg_dict.get('odd_argument')
    task_list.delete_task(hash)
    print(f'Task {hash} deleted succesfully!')


def edit(arg_dict, task_list):
    hash = arg_dict.get('odd_argument')
    old_task = task_list.get_task(hash)
    if old_task:
        arg_dict = old_task.updated_task(arg_dict)
        task_list.new_task(Task(arg_dict))
        task_list.delete_task(hash)
        print("Task edited succesfully!")


def display(arg_dict, task_list):
    # 'list' would shadow built-in list function
    filter_keyword = arg_dict.get('odd_argument')
    if filter_keyword:
        task_list.filter(filter_keyword)
    for hash, task in task_list.task_dict.items():
        print(task)


def help(foo, bar):
    # Not using those ^ arguments
    msg = """
It's very simple task manager, viable commands are:
1. add: add name 'task name' description 'task description' date 'task date'
2. delete: delete 'task hash'
3. edit: edit 'task hash' name 'new name' description 'new des' date 'new date'
4. display: display 'optional filter'
NOTICE: date format is: 'YYYY-MM-DD hh:mm' example: '2020-01-01 01:01'
    """
    print(msg)


if __name__ == '__main__':
    arg_dict = _create_arg_dict(sys.argv)
    action = arg_dict['action']
    _validate_action(action)
    task_list = TaskList('tasks.json')
    globals().get(action, 'help')(arg_dict, task_list)
