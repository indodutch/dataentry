from django.db import models
from django.utils.encoding import python_2_unicode_compatible

""" 
	Contains the models/tables for the kumbhmela_db.sqlite3
	database. 

	Every field has (when necessary) a 'help_text' that 
	explains the meaning of the field. 
"""

__author__ = "Louis Dijkstra"

@python_2_unicode_compatible
class Drive(models.Model): 
	"""
		Table/model to represent (a collection of) drive(s). 
	"""
	label        = models.CharField(max_length=50,
						help_text="Label added to the drive, e.g., 'kumbhmela_5'.")
	external 	 = models.BooleanField(default=False, 
						help_text="True when the drive is external and false otherwise.")
	time_added   = models.DateTimeField(blank=True,
						null=True, 
						help_text="Time when the drive was added to the drive bay.")
	time_removed = models.DateTimeField(blank=True,
						null=True,
						help_text="Time when the drive was removed from the drive bay.")
	whereabouts  = models.TextField(max_length=1000,
						blank=True, 
						help_text="Whereabouts of this drive copy, e.g., who had it lasts, where is it now etc. (optional).")
	note         = models.TextField(max_length=1000,
						blank=True, 
						help_text="Additional notes on this (collection of) drive(s) (optional).")

	def __str__(self): 
		return self.label 

@python_2_unicode_compatible
class DriveCopy(models.Model): 
	"""
		Every Drive might have several copies. This table/model
		is used to keep track of them. 
	"""
	drive 		 = models.ForeignKey(Drive, on_delete=models.CASCADE, 
						help_text="The unique drive it is a copy of.")
	label        = models.CharField(max_length=50,
						help_text="Label added to the drive, e.g., 'kumbhmela_5II'.")
	number       = models.IntegerField(help_text="Drive copy number.")
	whereabouts  = models.TextField(max_length=1000,
						blank=True, 
						help_text="Whereabouts of this drive copy, e.g., who had it lasts, where is it now etc. (optional).")
	note         = models.TextField(max_length=1000,
						blank=True, 
						help_text="Additional notes on this drive copy (optional).")

	def __str__(self): 
		return self.label

@python_2_unicode_compatible
class Person(models.Model): 
	"""
		Table/Model to represent a person 
	"""
	name  = models.CharField(max_length=100,
				help_text="First and last name.")
	email = models.CharField(max_length=200, 
				blank=True,
				help_text="Email address(es) (optional).")
	note  = models.TextField(max_length=1000,
				blank=True, 
				help_text="Notes (optional).")

	def __str__(self): 
		return self.name

@python_2_unicode_compatible
class Experiment(models.Model): 
	"""
		Table/Model to represent the various subexperiments
	"""	
	# every experiment is linked to a contact person 
	contactperson = models.ForeignKey(Person, on_delete=models.CASCADE,
						help_text="Main contact person for this subexperiment.")
	name          = models.CharField(max_length=100,
						help_text="Name of the subexperiment.")
	number        = models.IntegerField(help_text="Number of the subexperiment.")
	description   = models.TextField(max_length=1000,
						blank=True,  
						help_text="Short description of the experiment (optional).")
	note          = models.TextField(max_length=1000,
						blank=True, 
						help_text="Additional notes on the subexperiment (optional).")

	def __str__(self): 
		return "%s (subexperiment %d)"%(self.name, self.number) 

@python_2_unicode_compatible
class Format(models.Model): 
	"""
		Table/model to represent a file format, i.e., 
		the format in which output of a sensor is stored
	"""
	extension   = models.CharField(max_length=50,
						help_text="Extension of the file (in small letters!), e.g., '.txt' and not '.TXT'.")
	description = models.TextField(max_length=10000,
						blank=True, 
						help_text="Description of the file format (optional).")

	def __str__(self): 
		return self.extension 

@python_2_unicode_compatible
class Location(models.Model): 
	"""
		Table/model to represent a (geo)location
	"""
	latitude    = models.FloatField(blank=True, help_text="Optional.")
	longitude   = models.FloatField(blank=True, help_text="Optional.")
	description = models.TextField(max_length=1000,
						blank=True,  
						help_text="Description of the location (optional).")

@python_2_unicode_compatible
class Sensor(models.Model): 
	""" 
		Table/model to represent a sensor (e.g., camera/GPS device)
	"""
	sensor_type = models.CharField(max_length=100,
						help_text="Short description of the sensor, e.g., 'GoPro Camera'.")
	location    = models.ManyToManyField(Location,
						blank=True,
						help_text="The location for this sensor (optional).")
	format      = models.ManyToManyField(Format,
						blank=True,
						help_text="The format for the output of this sensor (optional).")
	note        = models.TextField(max_length=1000,
						blank=True, 
						help_text="Notes for this sensor (optional).")

	def __str__(self): 
		return self.sensor_type

@python_2_unicode_compatible
class Source(models.Model): 
	"""
		Table/model to represent a data source (e.g., 'Local police')
	"""
	name = models.CharField(max_length=200, 
						help_text="Name of the data source (e.g., 'Local Police')")
	note = models.TextField(max_length=1000,
						blank=True, 
						help_text="Additional notes on this data source (optional).")

	def __str__(self): 
		return self.name


@python_2_unicode_compatible
class File(models.Model): 
	"""
		The main table/model for this app. It is used to keep track
		of all files on the various drives for the Kumbh Mela experiment. 
	"""
	
	# a file can be stored a several drives:
	drive           = models.ManyToManyField(Drive, 
							through='StorageLocation',
							help_text="The drives on which the file is stored.")
	related_file 	= models.ManyToManyField("self", 
							blank=True, 
							help_text="Other related files.")
	format          = models.ForeignKey(Format,
							on_delete=models.CASCADE, 
							blank=True,
							null=True,
							help_text="Format of the file (optional).")
	experiment      = models.ManyToManyField(Experiment, 
							blank=True, 
							help_text="The subexperiment this file belongs to (optional).")	
	source          = models.ForeignKey(Source,
							on_delete=models.CASCADE, 
							blank=True,
							null=True,
							help_text="The data source (optional).")
	sensor          = models.ForeignKey(Sensor,
							on_delete=models.CASCADE,
							blank=True, 
							null=True,
							help_text="Sensor used to obtain the data (optional).")
	location        = models.ForeignKey(Location,
							on_delete=models.CASCADE,
							blank=True, 
							null=True,
							help_text="Location where the recording took place (optional).")
	time_added      = models.DateTimeField(auto_now=True, 
							blank=True, 
							help_text="Time when the drive was added to the drive bay (optional).")
	size            = models.IntegerField(blank=True, 
							null=True,
							help_text="Size in bytes (optional).")
	start_recording = models.DateTimeField(blank=True, 
							null=True,
							help_text="Time when the recording started (optional).") 
	end_recording   = models.DateTimeField(blank=True, 
							null=True,
							help_text="Time when the recording ended (optional).") 
	note            = models.TextField(max_length=1000,
							blank=True, 
							help_text="Additional notes on this file (optional).")

	def __str__(self): 
		"""Returns the file path"""
		filepaths = set()
		n_copies = 0 # the number of copies

		for storagelocation in self.storagelocation_set.all(): 
			filepaths.add(storagelocation.path)
			n_copies += 1

		if n_copies == 1: 
			return ', '.join(filepaths) + ' (1 copy)'

		return ', '.join(filepaths) + ' (%s copies)'%(int(n_copies))


class StorageLocation(models.Model):
	"""
		A location where a specific file is stored. This model/table
		links files and drives together. (Each file can be stored on
		multiple drives under different names).
	"""
	drive = models.ForeignKey(Drive,
					on_delete=models.CASCADE)
	file  = models.ForeignKey(File,
					on_delete=models.CASCADE)
	path  = models.CharField(max_length=300,
					help_text="Path of the file on the drive.")

	def __str__(self): 
		return "File %s on Drive %s"%(self.path, self.drive.label)

