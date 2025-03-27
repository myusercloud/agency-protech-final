from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Property, Appointment, Agent
from .forms import PropertyForm,  AppointmentForm, AgentForm
import json

import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth

from realestate.mpesa import MpesaAccessToken, LipanaMpesaPpassword

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import *



# Admin Login
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

# Admin Dashboard
@login_required
def admin_dashboard(request):
    properties = Property.objects.all()
    appointments = Appointment.objects.all()
    return render(request, "admin_dashboard.html", {"properties": properties, "appointments": appointments})

# Logout
def admin_logout(request):
    logout(request)
    return redirect('admin_login')


def home(request):
    properties = Property.objects.all()  # Fetch all properties
    return render(request, 'home.html', {'properties': properties})










@login_required
def add_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect after saving
    else:
        form = PropertyForm()
    return render(request, 'add_property.html', {'form': form})

@login_required
def edit_property(request, id):
    property_obj = get_object_or_404(Property, id=id)
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, 'edit_property.html', {'form': form})

@login_required
def delete_property(request, id):
    property_obj = get_object_or_404(Property, id=id)
    property_obj.delete()
    return redirect('admin_dashboard')


@login_required
def admin_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'admin_appointments.html', {'appointments': appointments})


def book_appointment(request):
    agents = Agent.objects.all()  # Fetch all agents from the database

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_success')  # Change to your actual success page
    else:
        form = AppointmentForm()

    return render(request, 'book_appointment.html', {'form': form, 'agents': agents})


def appointment_success(request):
    return render(request, 'appointment_success.html')

def pay_options(request):
    return render(request, 'payment_option.html')




@login_required
def add_agent(request):
    if request.method == "POST":
        form = AgentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('agent_list')  # Redirect to agent list page
    else:
        form = AgentForm()

    return render(request, 'agent_form.html', {'form': form})


def agent_list(request):
    agents = Agent.objects.all()
    return render(request, 'agent_list.html', {'agents': agents})

@login_required
# Update an agent
def update_agent(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    if request.method == 'POST':
        form = AgentForm(request.POST, request.FILES, instance=agent)
        if form.is_valid():
            form.save()
            return redirect('agent_list')
    else:
        form = AgentForm(instance=agent)
    return render(request, 'agent_form.html', {'form': form})

@login_required
# Delete an agent
def delete_agent(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    if request.method == 'POST':
        agent.delete()
        return redirect('agent_list')
    return render(request, 'agent_confirm_delete.html', {'agent': agent})

def admin_manage_agents(request):
    agents = Agent.objects.all()
    return render(request, 'admin_manage_agents.html', {'agents': agents})






def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'pay.html')


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/callback",
            "AccountReference": "Medilab",
            "TransactionDesc": "Appointment"
        }
        response = requests.post(api_url, json=request_data, headers=headers)

        response_data = response.json()
        transaction_id = response_data.get("CheckoutRequestID", "N/A")
        result_code = response_data.get("ResponseCode", "1")  # 0 is success, 1 is failure

        if result_code == "0":
            # Only save transaction if it was successful
            transaction = Transaction(
                phone_number=phone,
                amount=amount,
                transaction_id=transaction_id,
                status="Success"
            )
            transaction.save()

            return HttpResponse(f"Transaction ID: {transaction_id}, Status: Success")
        else:
            return HttpResponse(f"Transaction Failed. Error Code: {result_code}")




def transactions_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transactions.html', {'transactions': transactions})