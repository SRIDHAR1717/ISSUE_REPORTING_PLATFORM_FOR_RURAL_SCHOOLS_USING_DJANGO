from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.core.validators import RegexValidator
from datetime import datetime

class Meta:
    app_label = 'Issue Reporting MS'
class Profile(models.Model):
    typeuser =(('student','student'),('grievance', 'grievance'))
    COL=(('School1','School1'),('School2','School2'),('School3','School3')) #change school names
    user =models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    schoolname=models.CharField(max_length=29,choices=COL,blank=False)
    phone_regex =RegexValidator(regex=r'^\d{10,10}$', message="Phone number must be entered in the format:Up to 10 digits allowed.")
    contactnumber = models.CharField(validators=[phone_regex], max_length=10, blank=True) 
    type_user=models.CharField(max_length=20,default='student',choices=typeuser)
    CB=(('Computer Maths',"Computer Maths"),('Bio Maths',"Bio Maths"),('Pure Science',"Pure Science"),('Commerce',"Commerce"),('Computer Commerce',"Computer Commerce"))
    Class=models.CharField(choices=CB,max_length=29,default='Computer Maths')
    def __str__(self):
        return self.schoolname
    def __str__(self):
        return self.user.username
    
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

'''@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()'''


class Complaint(models.Model):
    STATUS =((1,'Solved'),(2, 'InProgress'),(3,'Pending'))
    TYPE=(('PlayGround',"PlayGround"),('Water Supply',"Water Supply"),('WashRoom',"WashRoom"),('Food Supply',"Food Supply"),('Sports & Games',"Sports & Games"),('Technical Equipment',"Technical Equipment"),('Other Issues',"Other Issues"))
    
    SUB = (('Teaching Staff',"Teaching Staff"),('HeadMaster',"HeadMaster"),('District Educational Officer (DEO)',"District Educational Officer (DEO)"),('Chief Educational Officer (CEO)',"Chief Educational Officer (CEO)"),('Other Educational Officers',"Other Educational Officers"))
    Subject=models.CharField(choices=SUB,null=True,max_length=200)
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    
    Type_of_issue=models.CharField(choices=TYPE,null=True,max_length=200)
    Description=models.TextField(max_length=4000,blank=False,null=True)
    Time = models.DateField(auto_now=True)
    status=models.IntegerField(choices=STATUS,default=3)
    
   
    def __init__(self, *args, **kwargs):
        super(Complaint, self).__init__(*args, **kwargs)
        self.__status = self.status

    def save(self, *args, **kwargs):
        if self.status and not self.__status:
            self.active_from = datetime.now()
        super(Complaint, self).save(*args, **kwargs)
    
    def __str__(self):
     	return self.get_Type_of_issue_display()
    # def __str__(self):
 	#     return str(self.user)

class Grievance(models.Model):
    guser=models.OneToOneField(User,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.guser