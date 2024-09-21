from django.urls import path
from .views import register, home, success, login_view, index, contact, logout_view, search, create, update, delete, CustomPasswordResetView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('search/', search, name='search'),
    path('register/', register, name='register'),
    path('success/', success, name='success'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Password reset views
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('contact/<int:contact_id>/detail/', contact, name='contact'),
    path('contact/create/', create, name='create'),
    path('contact/<int:contact_id>/update/', update, name='update'),
    path('contact/<int:contact_id>/delete/', delete, name='delete'),
]
