import os
import json
import unittest
from datetime import datetime
from chapter2 import main as ch_2_main  # better safe than sorry


class TestAdd(unittest.TestCase):
    def setUp(self):
        date_format = '%Y-%m-%d %H:%M'
        self.filename = 'test_tasks.json'
        self.arg_list = [
            'chapter2.py', 'add', 'name', 'foobar', 'description', 'foo',
            'date', datetime.strftime(datetime.today(), date_format)
        ]

    def tearDown(self):
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass

    def test_adding_valid(self):
        ch_2_main(self.arg_list, self.filename)

        # Remove description
        self.arg_list.pop(4)
        self.arg_list.pop(4)
        ch_2_main(self.arg_list, self.filename)

        # Remove date
        self.arg_list.pop(4)
        self.arg_list.pop(4)
        ch_2_main(self.arg_list, self.filename)

        with open(self.filename) as file:
            json_list = json.load(file)
            self.assertEqual(len(json_list), 3)

    def test_adding_invalid(self):
        # invalid date format
        self.arg_list.pop(6)
        self.arg_list.pop(6)
        self.arg_list += ['date', 'its not a date']
        self.assertRaises(ValueError, ch_2_main, self.arg_list, self.filename)

        # no name
        self.arg_list.pop(2)
        self.arg_list.pop(2)
        self.assertRaises(ValueError, ch_2_main, self.arg_list, self.filename)

    def test_delete_valid(self):
        # create static task
        self.arg_list[7] = '2000-01-01 00:00'
        ch_2_main(self.arg_list, self.filename)
        hash = '7c793854af032fa00d73c70bae7ae974'

        # remove created task
        self.arg_list = ['', 'delete', hash]
        ch_2_main(self.arg_list, self.filename)
        with open(self.filename) as file:
            json_list = json.load(file)
            self.assertEqual(len(json_list), 0)

    def test_delete_invalid(self):
        arg_list = ['', 'delete', 'foobar']
        self.assertRaises(KeyError, ch_2_main, arg_list, self.filename)
        arg_list = ['', 'delete', 'foo', 'bar']
        self.assertRaises(KeyError, ch_2_main, arg_list, self.filename)

    def test_edit(self):
        # DRY xD
        self.arg_list[7] = '2000-01-01 00:00'
        ch_2_main(self.arg_list, self.filename)
        hash = '7c793854af032fa00d73c70bae7ae974'

        # wrong hash
        arg_list = ['', 'edit', '12', 'name', 'a']
        self.assertRaises(KeyError, ch_2_main, arg_list, self.filename)

        # edit name leave rest - valid
        new_name = 'whatever'
        arg_list = ['', 'edit', hash, 'name', new_name]
        ch_2_main(arg_list, self.filename)
        with open(self.filename) as file:
            json_list = json.load(file)
            name = json_list[0]['name']
            date = json_list[0]['date']
            desc = json_list[0]['description']
            self.assertEqual(name, new_name)
            self.assertEqual(date, self.arg_list[7])
            self.assertEqual(desc, self.arg_list[5])


if __name__ == '__main__':
    unittest.main()
