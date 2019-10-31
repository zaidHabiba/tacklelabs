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
    is_file = models.BooleanField()


class Model(models.Model):
    company = models.ForeignKey(Institution, on_delete=models.CASCADE)
    api = models.ForeignKey(API, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField()
    version = models.CharField(max_length=64)
    logo = models.FileField(upload_to='F114225')
    request_cost = models.FloatField()
    free_request = models.IntegerField(blank=True, default=0, null=True)
    discount_percentage = models.FloatField(blank=True, default=0, null=True)
    discount_rate = models.IntegerField(blank=True, default=0, null=True)
    patient_model = models.BooleanField(default=False, blank=True, null=True)
    doctor_model = models.BooleanField(default=True, blank=True, null=True)
    lab_model = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name


class ModelSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, blank=True)
    number_of_request = models.IntegerField(blank=True)
    request_used = models.IntegerField(blank=True, default=0, null=True)
    is_free = models.BooleanField()


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
    file_value = models.FileField(upload_to="F854634", blank=True, null=True)
    text_value = models.TextField(blank=True, null=True)


"""
class ModelPlans(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    request_cost = models.FloatField()
    free_request = models.IntegerField(blank=True, default=0, null=True)
    dynamic = models.BooleanField()
"""
