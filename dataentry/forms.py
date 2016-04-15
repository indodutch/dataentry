from django import forms 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from .models import * 

class DriveForm(forms.ModelForm): 

	number_of_copies = forms.IntegerField(required=False, 
							help_text="Number of drive copies in the Pegasus2",
							initial="2", 
							widget=forms.TextInput(attrs={'id': 'number_of_copies',
   	                                                         'class': 'to_show'}))

	def __init__(self, *args, **kwargs): 
		
		super(DriveForm, self).__init__(*args, **kwargs)
		self.helper             = FormHelper(self)
		self.helper.form_id     = 'id-driveForm'
		self.helper.form_class  = 'blueForms'
		self.helper.form_method = 'post'
		self.helper.form_action = 'submit_survey'
		self.helper.form_tag    = False
		self.helper.label_class = 'col-md-3'
		self.helper.field_class = 'col-md-8'

		self.helper.layout.append(
				FormActions(
            		Submit('save_changes', 'Save changes', css_class="btn btn-danger btn-lg"),
            		Submit('cancel', 'Cancel', css_class="btn btn-danger btn-lg"),
        		)
			)

	class Meta: 
		model  = Drive 
		fields = ('label', 'note', 'whereabouts', 'external', )


class SensorForm(forms.ModelForm): 

	number_of_copies = forms.IntegerField(initial="1",
							help_text="Total number of this type of sensors")

	def __init__(self, *args, **kwargs): 
		super(SensorForm, self).__init__(*args, **kwargs)
		self.helper             = FormHelper(self)
		self.helper.form_id     = 'id-sensorForm'
		self.helper.form_class  = 'blueForms'
		self.helper.form_method = 'post'
		self.helper.form_action = 'submit_survey'
		self.helper.form_tag    = False
		self.helper.label_class = 'col-md-3'
		self.helper.field_class = 'col-md-8'

		self.helper.layout.append(
				FormActions(
            		Submit('save_changes', 'Save changes', css_class="btn btn-danger btn-lg"),
            		Submit('cancel', 'Cancel', css_class="btn btn-danger btn-lg"),
        		)
			)

	class Meta: 
		model  = Sensor
		fields = ('sensor_type', 'format', 'note', )


