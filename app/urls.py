from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app.controllers.controller_user import user_login, user_logout, user_signup, user_update, user_update_password, get_send_users, get_patients
from app.controllers.controller_institutions import create_hospital,create_lab,create_software_company, \
    update_institution,fetch_institution, fetch_hospitals, hospital_join_request, search_hospitals,cancel_join_request
from settings import local
from app.controllers.controller_report import create_report, fetch_report_images, fetch_lab_saved_reports, fetch_lab_saved_reports_search,send_report
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/login/', user_login),
    path('user/<int:user_id>/logout/', user_logout),
    path('user/signup/', user_signup),
    path('user/<int:user_id>/update/', user_update),
    path('user/<int:user_id>/change_password/', user_update_password),
    path('user/<int:user_id>/create_hospital/', create_hospital),
    path('user/<int:user_id>/create_lab/', create_lab),
    path('user/<int:user_id>/create_software_company/', create_software_company),
    path('user/<int:user_id>/update_institution/<int:institution_id>', update_institution),
    path('user/<int:user_id>/fetch_institution/<int:institution_id>', fetch_institution),
    path('fetch_hospitals/', fetch_hospitals),
    path('user/<int:user_id>/hospital_join_request/', hospital_join_request),
    path('user/<int:user_id>/search_hospitals/', search_hospitals),
    path('user/<int:user_id>/cancel_join_request/<int:join_request_id>', cancel_join_request),
    path('user/<int:user_id>/get_send_users/', get_send_users),
    path("user/<int:user_id>/get_patients/", get_patients),
    path("user/<int:user_id>/create_report/", create_report),
    path("user/<int:user_id>/fetch_report_images/<int:report>", fetch_report_images),
    path("user/<int:user_id>/fetch_reports/<int:lab>", fetch_lab_saved_reports),
    path("user/<int:user_id>/fetch_lab_saved_reports_search/<int:lab>/", fetch_lab_saved_reports_search),
    path("user/<int:user_id>/send_report/", send_report),
] + static(local.MEDIA_URL, document_root=local.MEDIA_ROOT)
