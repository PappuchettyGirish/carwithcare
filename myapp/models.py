from django.db import models
from django.contrib.gis.db import models as m1

# Create your models here.

class Userdata(models.Model):
    username=models.CharField(max_length=50)
    emailid=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    status=models.CharField(max_length=50,default="waiting")
    image=models.ImageField(upload_to="profile_image",blank=True,default="profile_image/download.png")

class Driverdata(models.Model):
    username=models.CharField(max_length=50)
    emailid=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    status=models.CharField(max_length=50,default="waiting")
    image=models.ImageField(upload_to="profile_image",blank=True,default="profile_image/download.png")

class Maps(models.Model):
    username=models.CharField(max_length=50)
    location=m1.PointField(srid=4326)

    def __unicode__(self):
        return self.username

class Signup(models.Model):
    emailid=models.CharField(max_length=50)
    otp=models.IntegerField()

class Driversignup(models.Model):
    emailid=models.CharField(max_length=50)
    otp=models.IntegerField()

class Userrides(models.Model):
    username=models.CharField(max_length=50)
    fromlong=models.DecimalField( max_digits=22, decimal_places=16)
    fromlat=models.DecimalField( max_digits=22, decimal_places=16)
    fromplace=models.TextField()
    tolong=models.DecimalField( max_digits=22, decimal_places=16)
    tolat=models.DecimalField( max_digits=22, decimal_places=16)
    toplace=models.TextField()
    distance=models.DecimalField( max_digits=22, decimal_places=16)
    timeinmins=models.TextField()
    raisedtime=models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,default="waiting")
    starttime=models.DateTimeField(null=True)
    endtime=models.DateTimeField(null=True)
    driver=models.CharField(max_length=50,null=True)
    driveremail=models.EmailField(max_length=50,null=True)
    driverlat=models.DecimalField( max_digits=22, decimal_places=16,null=True)
    driverlong=models.DecimalField( max_digits=22, decimal_places=16,null=True)