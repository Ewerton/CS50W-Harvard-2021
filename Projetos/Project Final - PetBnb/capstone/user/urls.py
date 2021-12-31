from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import reverse_lazy
from user.views.booking_review import booking_review, booking_review_delete, booking_review_list
from user.views.user_create_view import UserCreateView
from user.views.user_upload_a_picture_update_view import UserUploadAPictureUpdateView
from user.views.verification_view import VerificationView

from user.views.dashboard_server_local_photos_list_view import DashboardServerLocalPhotosListView
from user.views.dashboard_server_profile_create_view import DashboardServerProfileCreateView
from user.views.dashboard_server_profile_update_view import DashboardServerProfileUpdateView
from user.views.dashboard_server_profile_photo_add_create_view import DashboardServerProfilePhotoAddCreateView
from user.views.dashboard_server_profile_photo_delete import dashboard_server_profile_photo_delete
from user.views.dashboard_server_profile_availability_add_create_view import DashboardServerProfileAvailabilityAddCreateView
from user.views.dashboard_server_profile_availability_delete import dashboard_server_profile_availability_delete
from user.views.dashboard_server_profile_detail_view import DashboardServerProfileDetailView
from user.views.dashboard_server_availability_list_view import DashboardServerAvailabilityListView
from user.views.dashboard_server_booking_list_view import DashboardServerBookingListView
from user.views.dashboard_server_booking_reply import dashboard_server_booking_reply

from user.views.dashboard_client_booking_list_view import DashboardClientBookingListView
from user.views.dashboard_client_photo_of_my_pet_list_view import DashboardClientPhotoOfMyPetListView
from user.views.dashboard_client_booking_detail_view import DashboardClientBookingDetailView
from user.views.dashboard_client_profile_create_view import DashboardClientProfileCreateView
from user.views.dashboard_client_profile_update_view import DashboardClientProfileUpdateView
from user.views.dashboard_client_profile_photo_add_create_view import DashboardClientProfilePhotoAddCreateView
from user.views.dashboard_client_profile_photo_delete import dashboard_client_profile_photo_delete
from user.views.dashboard_client_profile_detail_view import DashboardClientProfileDetailView


from user.forms.user_set_password_form import UserSetPasswordForm
from user.forms.user_password_reset_form import UserPasswordResetForm
from user.forms.user_authentication_form import UserAuthenticationForm
from user.views.home_template_view import HomeTemplateView

from user.views.search_list_view import SearchListView
from user.views.search_detail_view import SearchDetailView

from user.views.booking_create_view import BookingCreateView
from user.views.booking_confirm import booking_confirm
from user.views.booking_cancel import booking_cancel

urlpatterns = [

    # home page
    path('', HomeTemplateView.as_view(), name='home_template_view'),

    # search page
    path('search/', SearchListView.as_view(), name='search_list_view'),

    path('profile/server/<int:pk>/', SearchDetailView.as_view(), name='search_detail_view'),

    path('booking/<int:pk>/', BookingCreateView.as_view(), name='booking_create_view'),

    path('booking/cancel/<int:pk>/', booking_cancel, name='booking_cancel'),

    path('booking/review/<int:pk>/', booking_review, name='booking_review'),

    path('booking/review/delete/<int:pk>/', booking_review_delete, name='booking_review_delete'),

    path('booking/review/list/<int:pk>', booking_review_list, name='booking_review_list'),

    path('booking/confirm/<int:pk>/', booking_confirm, name='booking_confirm'),

    path('user/upload_a_picture/', UserUploadAPictureUpdateView.as_view(), name='user_upload_a_picture_update_view'),

    path('dashboard/client/photo_of_my_pet/', DashboardClientPhotoOfMyPetListView.as_view(), name='dashboard_client_photo_of_my_pet_list_view'),

    path('dashboard/client/booking/', DashboardClientBookingListView.as_view(), name='dashboard_client_booking_list_view'),

    path('dashboard/client/booking/<int:pk>/', DashboardClientBookingDetailView.as_view(), name='dashboard_client_booking_detail_view'),

    path('dashboard/client/profile/', DashboardClientProfileDetailView.as_view(), name='dashboard_client_profile_detail_view'),

    path('dashboard/client/profile/create/', DashboardClientProfileCreateView.as_view(), name='dashboard_client_profile_create_view'),

    path('dashboard/client/profile/update/', DashboardClientProfileUpdateView.as_view(), name='dashboard_client_profile_update_view'),

    path('dashboard/client/profile/photo/add/', DashboardClientProfilePhotoAddCreateView.as_view(), name='dashboard_client_profile_photo_add_create_view'),

    path('dashboard/client/profile/photo/delete/<int:pk>/', dashboard_client_profile_photo_delete, name='dashboard_client_profile_photo_delete'),



    path('dashboard/server/profile/photo/add/', DashboardServerProfilePhotoAddCreateView.as_view(), name='dashboard_server_profile_photo_add_create_view'),

    path('dashboard/server/profile/photo/delete/', dashboard_server_profile_photo_delete, name='dashboard_server_profile_photo_delete'),

    path('dashboard/server/profile/availability/add/', DashboardServerProfileAvailabilityAddCreateView.as_view(), name='dashboard_server_profile_availability_add_create_view'),

    path('dashboard/server/profile/availability/delete/<int:pk>/', dashboard_server_profile_availability_delete, name='dashboard_server_profile_availability_delete'),

    path('dashboard/server/profile/create/', DashboardServerProfileCreateView.as_view(), name='dashboard_server_profile_create_view'),

    path('dashboard/server/profile/update/', DashboardServerProfileUpdateView.as_view(), name='dashboard_server_profile_update_view'),

    path('dashboard/server/local_photos/', DashboardServerLocalPhotosListView.as_view(), name='dashboard_server_local_photos_list_view'),

    path('dashboard/server/profile/', DashboardServerProfileDetailView.as_view(), name='dashboard_server_profile_detail_view'),

    path('dashboard/server/availability/', DashboardServerAvailabilityListView.as_view(), name='dashboard_server_availability_list_view'),
 
    path('dashboard/server/booking/', DashboardServerBookingListView.as_view(), name='dashboard_server_booking_list_view'),

    path('dashboard/server/booking/reply/<int:pk>/', dashboard_server_booking_reply, name='dashboard_server_booking_reply'),

    path('register/', UserCreateView.as_view(), name='register'),

    path('login/', auth_views.LoginView.as_view(template_name=settings.BASE_DIR / 'user/templates/auth/login.html', form_class=UserAuthenticationForm,), name='login', ),

    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('home_template_view')), name='logout'),

    path('password/reset/',
         auth_views.PasswordResetView.as_view(
             template_name=settings.BASE_DIR / 'user/templates/auth/password_reset.html',
             email_template_name=settings.BASE_DIR / \
             'user/templates/auth/password_reset_email.html',
             success_url=reverse_lazy('home_template_view'),
             form_class=UserPasswordResetForm,
             from_email='no-reply@example.com'
         ), name='password_reset'
         ),

    path('password/reset/confirm/<slug:uidb64>/<slug:token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name=settings.BASE_DIR / 'user/templates/auth/password_reset_confirm.html',
             success_url=reverse_lazy('home_template_view'),
             form_class=UserSetPasswordForm
         ), name='password_reset_confirm'
         ),

    path('activate/<slug:uidb64>/<slug:token>/',
         VerificationView.as_view(), name='activate'),

]
