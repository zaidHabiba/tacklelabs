from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app.controllers.controller_user import user_login, user_logout, user_signup, user_update, user_update_password, get_send_users
from app.controllers.controller_institutions import create_hospital,create_lab,create_software_company, \
    update_institution,fetch_institution, fetch_hospitals, hospital_join_request, search_hospitals,cancel_join_request
from settings import local

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

] + static(local.MEDIA_URL, document_root=local.MEDIA_ROOT)
