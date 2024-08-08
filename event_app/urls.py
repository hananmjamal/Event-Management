# event_app/urls.py

from django.urls import path
from .views import home, login_view, signup_view, plain_view, register_view,edit_event,display_events,your_friends_view,custom_login,payment_view, handle_payment, payment_success_view,payment_success,delete_event
from .import views
from django.contrib.auth import views as auth_views
from .views import update_confirmation_status


urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('plain/', plain_view, name='plain'),
    path('register/', register_view, name='register'),
    path('edit_event/<int:event_id>/', edit_event, name='edit_event'),
    path('data/', your_friends_view, name='your_friends_view'),
    path('login/', custom_login, name='custom_login'),
    path('al/', custom_login, name='al'),
    path('display_events/', display_events, name='display_events'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('update_confirmation_status/', update_confirmation_status, name='update_confirmation_status'),
    path('event/<int:event_id>/payment/', payment_view, name='payment_view'),
    path('payment_success/<int:event_id>/', payment_success, name='payment_success'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    #path('event/<int:event_id>/handle_payment/', handle_payment, name='handle_payment'),
    path('payment/success/', payment_success_view, name='payment_success'),
]

