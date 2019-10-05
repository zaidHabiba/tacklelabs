from django.db import models

from app.resources import values
from . import model_user


class InstitutionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()


class InstitutionTypesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()


class HospitalTypeManager(models.Manager):
    def get_queryset(self):
        type = InstitutionType.types.get(type=values.INSTITUTION_HOSPITAL_NAME)
        return super().get_queryset().filter(type=type)


class InstitutionType(models.Model):
    type = models.CharField(max_length=64)
    logo = models.FileField(upload_to='institution_type_logo', blank=True)

    types = InstitutionTypesManager()


class Institution(models.Model):
    manager = models.ForeignKey(model_user.User, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(InstitutionType, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    website = models.URLField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    photo = models.FileField(upload_to='company_photos', blank=True)
    logo = models.FileField(upload_to='company_logo')
    phone_number = models.CharField(max_length=32)
    create_date = models.DateField(auto_now_add=True)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64, blank=True)

    institutions = InstitutionManager()
    hospitals = HospitalTypeManager()


class HospitalJoinRequest(models.Model):
    hospital = models.ForeignKey(Institution, on_delete=models.CASCADE)
    doctor = models.ForeignKey(model_user.User, on_delete=models.CASCADE)
    send_date = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=None, blank=True,null=True)
    title = models.CharField(max_length=128, blank=True)
    msg = models.CharField(max_length=128, blank=True)


"""
class MedicalField(models.Model):
    field_name = models.CharField(max_length=128)

class InstitutionFields(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
"""
