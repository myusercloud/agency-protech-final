from django import forms
from .models import Property, Appointment, Agent


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'location', 'image']

class AppointmentForm(forms.ModelForm):
    agent = forms.ModelChoiceField(queryset=Agent.objects.all(), required=False, empty_label="Select an Agent")
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'property', 'date', 'time', 'message']

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['name', 'email', 'phone', 'profile_picture']