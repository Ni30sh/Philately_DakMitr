from django import forms
from .models import Order
from django import forms
from .models import Stamp
from .models import Contact,Payment


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['token_number', 'address', 'pincode']



class AddStampForm(forms.ModelForm):
    class Meta:
        model = Stamp
        fields = ['name', 'image', 'description', 'year','date_added']

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    problem = forms.CharField(widget=forms.Textarea)
    email_or_phone = forms.CharField(max_length=100)
    date = forms.DateField(widget=forms.SelectDateWidget)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'username', 'problem', 'email_or_phone']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'full_name', 'email', 'phone', 'stamp_type']