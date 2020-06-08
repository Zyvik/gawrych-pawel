
# Requirements

 Python == 3.8.3 (Should also work with older versions but I haven't tested it.)

# Chapter I - Car
It's just a class and a custom exception, so if you want to use it create a new python file, import Car class and do whatever you want.
*Code example:*

    from chapter1.py import Car

    pax_count = 1  # int
    car_mass = 1  # int / float
    gear_count = 1  # int
    new_car = Car(pax_count, car_mass, gear_count)

**Note: I assumed that gear count has to be int greater than 0 and car_mass can't be negative.**

# Chapter II - Task Manager
Basic task manager - you run it by executing commands written by this schema:

	python chapter2.py action arguments

Viable actions are :

> (***bold*** arguments are mandatory, the rest is optional)

- help

       python chapter2.py help
 - add

Arguments: ***name***, description, date (YYYY-MM-DD HH:MM -> 2000-01-01 13:01)

       python chapter2.py add name 'name of task' description 'task description' date '2020-06-21 06:00'
- edit

Arguments: ***hash***, name, description, date

      python chapter2.py edit 'b60dbf22576d376a5063caa6d663f2d3' name 'new name'

- delete:

Arguments: ***hash***

	  python chapter2.py delete 'f693d2aea61c011c8b95b3b393ed34c0'


 - display

 Arguments: all, today, active, expired

       python chapter2.py display active

 ### Notes:
 - tasks.json provided in this repo contains some sample data - it's ***optional*** and **you can delete it**.
 - For *edit* and *delete*: **hash** has to be 1st argument after action.
 - *name*, *description* and *date* have to come in pairs with values in quotes (ex: name 'foobar'). If number of arguments (excluding action) is odd then this script assumes that the 1st argument is hash or display filter.
- Order of: *name*, *description* and *date* arguments is interchangeable.
# Chapter III - Lost password
Run `chapter3.py`:

    python chapter3.py
### Simplilfied algorithm flowchart:
![Simple flowchart](https://i.imgur.com/QxT5roe.png)
