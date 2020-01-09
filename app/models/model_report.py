import random
import string

from django.db import models

from .model_institutions import Institution
from .model_user import User


def generate_id(size, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


class Report(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="doctor", null=True, blank=True,
                               default=None)
    lab = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, related_name="lab", null=True, blank=True,
                            default=None)
    patient = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="patient")
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    serial_numbers = models.CharField(max_length=9, blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.serial_numbers is None:
            self.serial_numbers = generate_id(8)
        super(Report, self).save(*args, **kwargs)
    

class ReportImage(models.Model):
    report = models.ForeignKey(Report, on_delete=models.DO_NOTHING)
    image = models.FileField(upload_to='report_images')

    def __str__(self):
        return str(self.report)


# Decision
class ReportHub(models.Model):
    report = models.ForeignKey(Report, on_delete=models.DO_NOTHING, related_name="report_hub_instance")
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="receiver")
    title = models.CharField(max_length=128)
    msg = models.CharField(max_length=255, null=True, blank=True)
    send_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.report)
