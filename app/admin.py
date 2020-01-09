from django.contrib import admin

from app.models.model_institutions import Institution, InstitutionType, HospitalJoinRequest
from app.models.model_model import ModelSubscription, ModelImage, IOAPI, IORequest, API, Model, ModelRequest
from app.models.model_report import ReportImage, Report, ReportHub
from app.models.model_user import User, UserType, Counters


@admin.register(Counters)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'id')


@admin.register(Model)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'version', 'api', 'company')


@admin.register(ModelRequest)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(IORequest)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(API)
class UserAdmin(admin.ModelAdmin):
    list_display = ('url', 'id', 'method')


@admin.register(ModelSubscription)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'model', 'number_of_request', 'request_used', 'is_free')


@admin.register(ModelImage)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(IOAPI)
class UserAdmin(admin.ModelAdmin):
    list_display = ('api', 'title', 'is_input', 'json_name', 'is_file')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'type', 'first_name', 'last_name')


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(InstitutionType)
class InstitutionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'title', 'description', 'serial_numbers')


@admin.register(ReportHub)
class ReportHubAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'sender', 'receiver', 'title', 'msg')


@admin.register(HospitalJoinRequest)
class ReportHubAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'hospital', 'is_accepted', 'send_date')

@admin.register(ReportImage)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('id','report')

