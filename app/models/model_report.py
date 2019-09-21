from django.db import models

from . import model_institutions
from . import model_user


class Report(models.Model):
    doctor = models.ForeignKey(model_user.User, on_delete=models.DO_NOTHING)
    lab = models.ForeignKey(model_institutions.Institution, on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    patient = models.ForeignKey(model_user.User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=255, null=True, blank=True)


class ReportImage(models.Model):
    report = models.ForeignKey(Report, on_delete=models.DO_NOTHING)
    image = models.FileField(upload_to='report_images')


class ReportHub(models.Model):
    report = models.ForeignKey(Report, on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(model_user.User, on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey(model_user.User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=128)
    msg = models.CharField(max_length=255, null=True, blank=True)
