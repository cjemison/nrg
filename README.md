## NRG Interview ##

Solution to respond to the manual inputs of an automobile gear shift with automatic transmission, as well as dealing with automated gear shifts.  This should include Unit Testing for the basic scenarios.
 
Logging (this is a company log for all of its models by vin number):
* Log the speed at which the gear changes from one level to another.
* Log as an error any time the speed exceeds a defined level without causing a gear change.
 
Build sample queries to show the following:
1. What is the average speed that causes a gear to change from 3 to 4 by car type.
2. For any car that had an error in gear changes prior to one month ago, has it experienced any errors in the last 7 days?

## How to run ##

Python 3.9+ is needed.

Question 1 can be answered by opening the events.csv file with Excel.
Question 2 can be found in the logs.

```shell
$ rm -f event.csv
$ rm -f debug.log
$ python -m venv .venv
$ source ./.venv/bin/activate
$ pip install -Ur requirement.txt
$ pytest # run the tests
$ python main.py
```