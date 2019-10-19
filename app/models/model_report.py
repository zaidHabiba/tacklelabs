from django.db import models

from .model_institutions import Institution
from .model_user import User


class Report(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="doctor", null=True, blank=True,
                               default=None)
    lab = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, related_name="lab", null=True, blank=True,
                            default=None)
    patient = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="patient")
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.id)


class ReportImage(models.Model):
    report = models.ForeignKey(Report, on_delete=models.DO_NOTHING)
    image = models.FileField(upload_to='report_images')

    def __str__(self):
        return str(self.report)


# Decision
class ReportHub(models.Model):
    report = models.ForeignKey(Report, on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="receiver")
    title = models.CharField(max_length=128)
    msg = models.CharField(max_length=255, null=True, blank=True)
    send_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.report)
