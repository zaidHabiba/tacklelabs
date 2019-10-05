from django.contrib import admin

from app.models.model_institutions import Institution, InstitutionType, HospitalJoinRequest
from app.models.model_user import User, UserType

admin.site.register(User)
admin.site.register(UserType)
admin.site.register(Institution)
admin.site.register(InstitutionType)
admin.site.register(HospitalJoinRequest)