from realestate import views
from django.contrib import admin
from django.urls import path
from .views import admin_login, admin_dashboard, admin_logout, delete_property, add_property, edit_property
from .views import admin_appointments, book_appointment, appointment_success
from .views import agent_list, add_agent, update_agent, delete_agent, admin_manage_agents
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', admin_login, name='admin_login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('logout/', admin_logout, name='admin_logout'),
    path('add-property/', add_property, name='add_property'),
    path('edit-property/<int:id>/', edit_property, name='edit_property'),
    path('delete-property/<int:id>/', delete_property, name='delete_property'),
    path('admin-appointments/', admin_appointments, name='admin_appointments'),
    path('book-appointment/', book_appointment, name='book_appointment'),
    path('appointment-success/', appointment_success, name='appointment_success'),
    path('agents/', admin_manage_agents, name='agent_list'),
    path('agents/add/', add_agent, name='add_agent'),
    path('agents/update/<int:agent_id>/', update_agent, name='update_agent'),
    path('agents/delete/<int:agent_id>/', delete_agent, name='delete_agent'),
    path('admin/agents/', admin_manage_agents, name='admin_manage_agents'),
    path('agents/', agent_list, name='agent_list'),

    path('pay/', views.pay, name='pay'),
    path('pay_options/', views.pay_options, name='pay_options'),


    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),
    path('transactions/', views.transactions_list, name='transactions'),

]
