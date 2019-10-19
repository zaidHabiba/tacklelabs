from django.db import models

from app.models.model_institutions import Institution
from app.models.model_user import User


class API(models.Model):
    url = models.CharField(max_length=250)
    method = models.CharField(max_length=16)


class IOAPI(models.Model):
    api = models.ForeignKey(API, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    is_input = models.BooleanField()
    json_name = models.CharField(max_length=128)


class ModelSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_numbers = models.IntegerField(blank=True)
    is_free = models.BooleanField()


class Model(models.Model):
    company = models.ForeignKey(Institution, on_delete=models.CASCADE)
    api = models.ForeignKey(API, on_delete=models.CASCADE)
    name = models.FileField(max_length=128)
    description = models.TextField()
    version = models.CharField(max_length=64)
    logo = models.FileField(upload_to='F114225')


class ModelImage(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    image = models.FileField(upload_to="F123354")


class ModelRequest(models.Model):
    model = models.ForeignKey(Model, models.CASCADE)
    request_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class IORequest(models.Model):
    io = models.ForeignKey(IOAPI, on_delete=models.CASCADE)
    request = models.ForeignKey(ModelRequest, on_delete=models.CASCADE)
    file_value = models.FileField(upload_to="F854634")
    text_value = models.TextField()
