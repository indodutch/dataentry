#!/usr/bin/env python
from __future__ import print_function, division
from optparse import OptionParser
import os
import sys
from datetime import datetime, timedelta
from openpyxl import Workbook, load_workbook
import sqlite3
import pytz

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
			if '$' in filename: 
				continue
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
	
	# convert to GMT from the local (IST) time
	start_time = start_time - timedelta(hours=5, minutes=30)
	end_time   = end_time - timedelta(hours=5, minutes=30)
	return start_time, end_time

def ask_for_drives(conn): 
	"""
		Asks for which drives to add the data. 

		Args:
			conn - sqlite3 connector to the kumbh mela metadatabase
	"""
	cursor = conn.execute("SELECT label, external FROM dataentry_drive")	# get the drives

	print("\n\nSelect the drives:\n")
	for i, row in enumerate(cursor):
		if row[1] == "True": 
			print("(%d)\t%s\t(external)"%(i+1, row[0]))
		else: 
			print("(%d)\t%s"%(i+1, row[0]))

	print("\nPlease, fill in the drives on which the files should be stored:")
	drives = input().lower()
	drives = drives.split('&')

	return [int(x) for x in drives]


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
	dirname = args[1]
	if dirname[-1] != '/': 
		dirname += '/'
	
	experiments = [int(x) for x in args[2].split('/')]

	# print the input on the screen and ask the user to concur
	print("Adding GPS data")
	print("---------------\n")
	print("path:                 %s"%gpsdir)
	print("stored in directory:  %s\n"%dirname)
	print("stored under experiments:\n")
	for exp in experiments: 
		print("\t%d"%exp)
	print("")
	
	if not query_yes_no("Are you sure you want to save these files in this directory and under these experiments?"):
		print("The metadata is NOT stored.")
		sys.exit(1)

	# create connection to the sqlite3 database
	conn = sqlite3.connect('kumbhmela_db.sqlite3')

	drives = ask_for_drives(conn)

	# walk through the GPS excel files in the directory
	list_of_files = get_xlsx_files(gpsdir)

	for file_name, file_path in list_of_files.items():
		print("%s\t%s"%(file_name, file_path)) 

		start_time, end_time = get_time_range(file_path)
		print(start_time, end_time)

		cursor = conn.execute('SELECT max(id) FROM dataentry_file')
		file_id = cursor.fetchone()[0] + 1
		print("New file id:", file_id)

		# add the file to the database
		conn.execute("INSERT INTO dataentry_file (id, time_added, start_recording, end_recording, format_id, sensor_id, note) VALUES (?,?,?,?,3,3,?);", [file_id, datetime.now(), start_time, end_time, ''])

		# link the file to the right experiments
		for exp in experiments: 
			conn.execute("INSERT INTO dataentry_file_experiment (file_id, experiment_id) VALUES (?, ?);", [file_id, exp])

		# link the file to the rights drives
		for drive in drives: 
			drive_path = dirname + file_name
			conn.execute("INSERT INTO dataentry_storagelocation (path, drive_id, file_id) VALUES (?, ?, ?);", [drive_path, drive, file_id])

	conn.commit() # commit the inserts made	
	cursor.close()
	conn.close()

if __name__ == '__main__':
	sys.exit(main())