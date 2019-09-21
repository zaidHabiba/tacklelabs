from django.db import models

from . import model_user


class InstitutionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()


class InstitutionType(models.Model):
    type = models.CharField(max_length=64)
    logo = models.FileField(upload_to='institution_type_logo', blank=True)


class Institution(models.Model):
    manager = models.ForeignKey(model_user.User, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(InstitutionType, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, blank=True)
    website = models.URLField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    photo = models.FileField(upload_to='company_photos', blank=True)
    logo = models.FileField(upload_to='company_logo')
    phone_number = models.CharField(max_length=32, blank=True)
    create_date = models.DateField(auto_now_add=True)
    country = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64, blank=True)
    street = models.CharField(max_length=64, blank=True)

    Institutions = InstitutionManager()


"""
class MedicalField(models.Model):
    field_name = models.CharField(max_length=128)

class InstitutionFields(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING)
"""
