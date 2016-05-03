#!/usr/bin/env python
from __future__ import print_function, division
from optparse import OptionParser
import os
import sys
from datetime import datetime
from openpyxl import Workbook, load_workbook
import sqlite3

__author__ = "Louis Dijkstra"

usage = """%prog <gpsdir> <dirname>

where 

	<gpsdir>	the directory with the GPS files
	<dirname>	the name of the directory in which the GPS files will 
				be stored on the drive(s)
	<experiments> the number of the experiments, separated by a slash ('/')

EXAMPLE USAGE:
--------------

	%prog gpsdata/ experiment2and8/ 2/8

"""

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".

    Taken from: http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def get_xlsx_files(path): 
	"""
		Gets all XLSX files in a given directory
	"""
	list_of_files = {}
	for (dirpath, dirnames, filenames) in os.walk(path):
		for filename in filenames:
			if filename.endswith('.xlsx'): 
				list_of_files[filename] = os.sep.join([dirpath, filename])
	return list_of_files


def get_time(date, clock):
	# hours, minutes, seconds = clock.split(':')
	# date.replace(hour=hours, minute=minutes, second=seconds)
	return datetime.combine(date, clock) 

	# return date

def get_last_line(worksheet): 
	i = 1
	while str(worksheet['C' + str(i)].value) != 'None': 
		i+=1
	return i - 1

def get_time_range(file_path):
	"""
		Gets the time range of a given GPS excel data file.
	"""
	# open the xlsx file: 
	wb         = load_workbook(filename=file_path)
	data       = wb['Sheet1']

	# get start and end time
	start_time = datetime.combine(data['C2'].value, data['D2'].value) 
	last_row   = get_last_line(data)
	end_time   = datetime.combine(data['C' + str(last_row)].value, data['D' + str(last_row)].value) 
	return start_time, end_time

def main():
	parser = OptionParser(usage=usage)
	(options, args) = parser.parse_args()
	
	# check whether the number of arguments is correct
	if (len(args)<3):
		parser.print_help()
		return 1

	# location of the data directory: 
	gpsdir = os.path.abspath(args[0]) 
	if gpsdir[-1] != '/': 
		gpsdir += '/'

	# location of the output directory: 
	dirname = os.path.abspath(args[1]) 
	
	experiments = [int(x) for x in args[2].split('/')]

	print("Storing the files from %s under the directory name %s"%(gpsdir, dirname))
	print("Stored under experiment(s): ", experiments)

	if not query_yes_no("Are you sure you want to save these files in this directory and under these experiments?"):
		print("Ok, files are NOT stored.")
		sys.exit(1)

	# create connection to the sqlite3 database
	conn = sqlite3.connect('../kumbhmela_db.sqlite3')
	c = conn.cursor()

	# walk through the GPS excel files in the directory
	list_of_files = get_xlsx_files(gpsdir)

	for file_name, file_path in list_of_files.items():
		print("%s\t%s"%(file_name, file_path)) 

		start_time, end_time = get_time_range(file_path)
		print(start_time, end_time)

		# add the file to the database



if __name__ == '__main__':
	sys.exit(main())