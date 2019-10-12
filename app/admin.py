from django.contrib import admin

from app.models.model_institutions import Institution, InstitutionType, HospitalJoinRequest
from app.models.model_report import ReportImage, Report, ReportHub
from app.models.model_user import User, UserType


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name')


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
    list_display = ('id', 'patient')


@admin.register(ReportHub)
class ReportHubAdmin(admin.ModelAdmin):
    list_display = ('id','report', 'sender', 'receiver', 'title', 'msg')


admin.site.register(HospitalJoinRequest)
admin.site.register(ReportImage)
