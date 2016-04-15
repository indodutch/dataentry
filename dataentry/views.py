from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from django.apps import apps
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from collections import OrderedDict

from .models import *
from .forms import * 

__author__ = "Louis Dijkstra"

APP_LABEL = "dataentry"

def sensor_new(request): 
	"""
		Page for adding sensors.
	"""
	if request.method == "POST": 
		form = SensorForm(request.POST) 
		if form.is_valid(): 
			for copy in range( int(form.cleaned_data['number_of_copies']) ):
				sensor = Sensor(
							sensor_type = form.cleaned_data['sensor_type'],
							note        = form.cleaned_data['note']
						)
				sensor.save()
				for format in form.cleaned_data['format']: 
					sensor.format.add(format)
				sensor.save()
			return redirect('/Sensor/list', None)
	else: 
		form = SensorForm()
	
	context = { 
				'form' : form, 
				'title': 'Adding new sensors',
			  }	
	return render(request, 'dataentry/sensor_edit.html', context)


def drive_new(request): 
	"""
		Page for adding a new (normal or external)
		harddrive. 
	"""
	if request.method == "POST": 
		form = DriveForm(request.POST) 
		if form.is_valid(): 
			drive            = form.save(commit=False)
			drive.time_added = timezone.now()
			drive.save()

			if not drive.external: 
				# creat copydrives: 
				for copy in range( int(form.cleaned_data['number_of_copies']) ): 
					label       = drive.label + '-' + str(copy+1)
					copydrive   = DriveCopy(label=label,
							 number      = copy+1,
							 whereabouts = "",
							 note        = "",
							 drive 		 = drive
						)
					copydrive.save()


			return redirect('/drive/' + str(drive.pk), None)
	else: 
		form = DriveForm()
	
	context = { 
				'form' : form, 
				'title': 'Adding a new drive',
			  }	
	return render(request, 'dataentry/drive_edit.html', context)

def drive_edit(request, pk): 
	""" 
		Returns a view for editing the drive given the 
		drive's id 
	"""
	drive = get_object_or_404(Drive, pk=pk)

	if request.method == "POST": 
		form = DriveForm(request.POST, instance=drive)
		if form.is_valid():
			drive            = form.save(commit=False)
			drive.time_added = timezone.now()
			drive.save()

			if not drive.external: 
				# creat copydrives: 
				for copy in range( int(form.cleaned_data['number_of_copies']) ): 
					label       = drive.label + '-' + str(copy+1)
					copydrive   = DriveCopy(label=label,
							 number      = copy+1,
							 whereabouts = "",
							 note        = "",
							 drive 		 = drive
						)
					copydrive.save()


			return redirect('/drive/' + str(drive.pk), None)
	else: 
		form = DriveForm(instance=drive)

	context = { 
				'form' : form, 
				'title': 'Drive %s'%drive.label,
			  }	
	return render(request, 'dataentry/drive_edit.html', context)



def index(request): 
	"""
		The main page of the data entry app
	"""
	context = {	
				'drives'      : Drive.objects.all,
				'experiments' : Experiment.objects.all,
				'sensors'     : Sensor.objects.all,
				'sources'     : Source.objects.all,
				}
	return render(request, 'dataentry/index.html', context)

def create_object_dictionary(raw_object, fields):
	"""
		Returns a dictionary of an object. Every (valid) 
		field is a key. Each value is in its turn a dictionary
		with the fields 'value' and 'id' (in case the field is 
		represents a ForeignKey). 
	"""
	dict_object = OrderedDict()

	fields_to_be_ignored = []

	# walk over the fields
	for field in fields: 
		try: 
			dict_object[field] = {'value': getattr(raw_object, field.name)}
			if field.get_internal_type() == 'ForeignKey': 
				dict_object[field]['id'] = getattr(raw_object, field.name + '_id')
		except: 
			fields_to_be_ignored.append(field)

	return dict_object, fields_to_be_ignored

def view_detail(request, model_str, object_id):
	"""
		Generic view for showing the details of one 
		object. (It allows you to view any object, 
		since it automatically retrieves its fields 
		and the entries).
	"""
	# get the model object from the string representation
	model = apps.get_model(app_label=APP_LABEL, model_name=model_str)

	# get all the fields for this model
	fields = model._meta.get_fields()
	
	# get the object
	raw_object = model.objects.get(pk=object_id)

	dict_object, fields_to_be_ignored = create_object_dictionary(raw_object, fields)

	# update the fields: 
	fields = [f for f in fields if f not in fields_to_be_ignored]

	# pass the necessary context to the html tempate 
	context = { 
		'object_id': object_id, # the id of the object
		'model_str': model_str, # the name of the model 
		'object': dict_object, # the data
		'fields': fields, # all fields of this model
		'title': raw_object.__str__(),
	}

	return render(request, 'detail.html', context) 


def view_list(request, model_str):
	"""
		Generic view for showing a list. (It allows you to 
		view any model, since it automatically retrieves
		its fields and the entries).
	"""
	# get the model object from the string representation
	model = apps.get_model(app_label=APP_LABEL, model_name=model_str)
	
	# get all the fields for this model
	fields = model._meta.get_fields()
	
	object_list = [] # initialize

	# walk through all objects 
	for raw_object in model.objects.all(): 
		# turn object into dictionary
		dict_object, fields_to_be_ignored = create_object_dictionary(raw_object, fields)

		# update the fields: 
		fields = [f for f in fields if f not in fields_to_be_ignored]

		# add the new objects
		object_list.append(dict_object)

	# pass the necessary context to the html tempate 
	context = { 
		'model_str': model_str, # the name of the model 
		'object_list': object_list, # the data
		'fields': fields, # all fields of this model
		'title': model_str,
	}

	return render(request, 'list.html', context) 

def view_subset_files(request, model_str, object_id):
	""" 
		Show all files associated with a particular 
		object (specified by its object_id) of a particular
		class (specified by a string representation of the 
		model name)
	""" 

	# get all the fields for the file model
	fields = File._meta.get_fields()
	
	object_list = [] # initialize

	# get a raw object list given the model_str
	# also specify the title of the site
	model_str = model_str.lower()
	if model_str == 'drive': 
		raw_object_list = File.objects.filter(drive=object_id)
		title = "Files on drive " + Drive.objects.get(pk=int(object_id)).__str__()
	elif model_str == 'experiment': 
		raw_object_list = File.objects.filter(experiment=object_id)
		# create the title:
		title             = "Files for experiment %s"%Experiment.objects.get(pk=int(object_id)).__str__()
	elif model_str == 'source': 
		raw_object_list = File.objects.filter(source=object_id)
		title = "Files from source " + Source.objects.get(pk=object_id).__str__()
	elif model_str == 'sensor': 
		raw_object_list = File.objects.filter(sensor=object_id)
		title = "Files for sensor " + Sensor.objects.get(pk=object_id).__str__()
	else: # show everything
		raw_object_list = File.objects.all()
		title = "Files"


	# walk through all objects 
	for raw_object in raw_object_list: 
		# turn object into dictionary
		dict_object, fields_to_be_ignored = create_object_dictionary(raw_object, fields)

		# update the fields: 
		fields = [f for f in fields if f not in fields_to_be_ignored]

		# add the new objects
		object_list.append(dict_object)

	# pass the necessary context to the html tempate 
	context = { 
		# 'model_str': model_str, # the name of the model 
		'object_list': object_list, # the data
		'fields': fields, # all fields of this model
		'title': title,
	}

	return render(request, 'list.html', context) 
