from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class Experiment(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=200)
    description = models.CharField(max_length=4000)

    def __str__(self):
        return '{self.id}. {self.name}'.format(self=self);

class File(models.Model):
    volume = models.CharField(max_length=500)

    def __str__(self):
        return '{self.id}. {self.volume}'.format(self=self);

class FileExperiment(models.Model):
    file_id = models.ForeignKey(File)
    experiment_id = models.ForeignKey(Experiment)

    def __str__(self):
        return '{self.file_id} - {self.experiment_id}'.format(self=self);

