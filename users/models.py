from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class UserProfileInfo(models.Model):
    id = models.AutoField(primary_key=True, blank=False)
    confirmPassword = models.CharField(max_length=30)
    TYPE_CHOICES = (
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient')
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Patient')
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING)
    address = models.TextField()

    def __str__(self):
        return self.user.username 

class Picture(models.Model):
    document = models.FileField(upload_to='files')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user',)

    def __str__(self):
        return self.document.name
    
class Blog(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    sno = models.AutoField(primary_key=True, blank=False)
    title = models.CharField(max_length=40)
    image = models.FileField(upload_to='files')
    CATEGORY_CHOICES = (
        ('Mental Health', 'Mental Health'),
        ('Heart Disease', 'Heart Disease'),
        ('Covid-19', 'Covid-19'),
        ('Immunization', 'Immunization')
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    summary = models.TextField()
    content = models.TextField()
    draft = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category + ' => ' + self.title
    

from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True, blank=False)
    patient = models.ForeignKey(User, related_name='patient_appointments', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='doctor_appointments', on_delete=models.CASCADE)
    speciality = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def save(self, *args, **kwargs):
        # calculate the end time based on the start time and appointment duration of 45 mins
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = start_datetime + timedelta(minutes=45)
        self.end_time = end_datetime.time()
        super(Appointment, self).save(*args, **kwargs)

    def __str__(self):
        return "{} => {}".format(self.patient.username, self.doctor.username)
