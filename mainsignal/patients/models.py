import os
from django.db import models
from django.http import request
from django.shortcuts import render
from django.template import context
import uuid


# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    class Meta:
        abstract = False

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email} {self.phone_number} {self.address} {self.city} {self.state} {self.zip_code} {self.country}"

class PatientImage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='patient_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.patient.first_name} {self.patient.last_name}"


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


def upload_to_unique(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('uploads', new_filename)


class UploadedImage(models.Model):
    image = models.ImageField(upload_to=upload_to_unique)
    uploaded_at = models.DateTimeField(auto_now_add=True)
