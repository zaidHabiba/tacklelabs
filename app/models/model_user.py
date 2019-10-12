import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from app.resources.encryptor import encrypt_password


def generate_id(size, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


class UserType(models.Model):
    type = models.CharField(max_length=32)
    types = models.Manager()

    def __str__(self):
        return self.type


class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()

    def is_email_used(self, email):
        if len(self.get_queryset().filter(email=email)) is 0:
            return False
        else:
            return True

    def get_user_type(self, user_id):
        user = self.get_queryset().get(id=user_id)
        return user.type

    def is_doctor(self, type):
        if type.type == "Doctor":
            return True
        else:
            return False

    def is_developer(self, type):
        if type.type == "Developer":
            return True
        else:
            return False

    def is_patient(self, type):
        if type.type == "Patient":
            return True
        else:
            return False

    def get_user(self, email):
        user = self.get_queryset().get(email=email)
        return user

    def login_user(self, email, password):
        try:
            user = self.get_user(email=email)
            if user.password == encrypt_password(password):
                user.is_login = True
                user.save()
                return user
            else:
                return None
        except ObjectDoesNotExist:
            return None

    def logout_user(self, user_id):
        try:
            user = self.get_queryset().get(id=user_id)
            user.is_login = False
            user.save()
            return True
        except ObjectDoesNotExist:
            return False

    def have_institution(self, user_id):
        try:
            from app.models.model_institutions import Institution
            institution = Institution.institutions.get(manager=user_id)
            return institution
        except ObjectDoesNotExist:
            return None

    def is_join_hospital(self, user_id):
        try:
            from app.models.model_institutions import HospitalJoinRequest
            institution = HospitalJoinRequest.objects.get(doctor=user_id)
            return institution
        except ObjectDoesNotExist:
            return None


class DeveloperTypeManager(models.Manager):
    def get_queryset(self):
        type = UserType.types.get(type="Developer")
        return super().get_queryset().filter(type=type)


class DoctorTypeManager(models.Manager):
    def get_queryset(self):
        type = UserType.types.get(type="Doctor")
        return super().get_queryset().filter(type=type)


class PatientTypeManager(models.Manager):
    def get_queryset(self):
        type = UserType.types.get(type="Patient")
        return super().get_queryset().filter(type=type)


class User(models.Model):
    type = models.ForeignKey(UserType, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=32)
    second_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=32, blank=True)
    gender = models.CharField(max_length=16)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    photo = models.FileField(upload_to='user_photos', blank=True, null=True, default=None)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    code = models.CharField(max_length=7,blank=True)
    street = models.CharField(max_length=64, blank=True)
    birth_date = models.DateField()
    register_date = models.DateField(auto_now=True)
    is_login = models.BooleanField(default=True, blank=True)

    users = UserManager()
    doctors = DoctorTypeManager()
    developers = DeveloperTypeManager()
    patients = PatientTypeManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.code is None:
            self.code = generate_id(6)
        super(User, self).save(*args, **kwargs)
