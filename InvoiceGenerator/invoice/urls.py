from django.urls import path
from . import views

app_name = 'invoice'

urlpatterns = [
    path('create/', views.create_invoice, name='create_invoice'),
    path('update/<int:id>/', views.update_invoice, name='update'),
    path('delete/<int:id>/', views.delete_invoice, name='delete'),

    path('profile-company/', views.profile_and_company_edit, name='profile_and_company_edit'),

    path('invoice/download/<int:id>/', views.download_invoice, name='download_invoice'),
    path('invoice/send_email/<int:id>/', views.send_email_view, name='send_email'),
]