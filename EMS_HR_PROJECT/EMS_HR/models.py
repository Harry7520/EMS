from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class genderModel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class positionModel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class empcreateModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=16)
    salary = models.CharField(max_length=50)
    position = models.ForeignKey(positionModel, on_delete=models.CASCADE, default=None)
    gender = models.ForeignKey(genderModel, on_delete=models.CASCADE, default=None)
    image = models.ImageField(default=None, blank=True)
    create_at = models.DateTimeField(default=None)

    def __str__(self):
        return self.user.username

class empdetailModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.TextField()
    birthday = models.DateField()
    image = models.ImageField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class commentModel(models.Model):
    content = models.TextField(default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    create_at = models.DateTimeField(default=None)

    def __str__(self):
        return self.content

class leaveModel(models.Model):
    empid = models.IntegerField(default=None)
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(default=None)
    status = models.CharField(max_length=12,default='pending') 
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    create_at = models.DateTimeField(default=None)

    def __str__(self):
        return self.name

class resModel(models.Model):
    empid = models.IntegerField(default=None)
    name = models.CharField(max_length=50)
    position = models.ForeignKey(positionModel, on_delete=models.CASCADE, default=None)
    description = models.TextField(default=None)
    status = models.CharField(max_length=12,default='pending') 
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    create_at = models.DateTimeField(default=None)

    def __str__(self):
        return self.name

class projectModel(models.Model):
    client = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    partner = models.CharField(max_length=50)
    description = models.TextField(default=None)
    deadline = models.DateField()
    cost = models.CharField(max_length=50)
    status = models.CharField(max_length=12,default='on-going')
    create_at = models.DateTimeField(default=None)

    def __str__(self):
        return self.title

class updateModel(models.Model):
    division = models.CharField(max_length=50)
    progress = models.CharField(max_length=10)
    image = models.ImageField(default=None)
    post = models.ForeignKey(projectModel, on_delete=models.CASCADE, default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    create_at = models.DateTimeField(default=None)

    def __str__(self):
        return self.division
