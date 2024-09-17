from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import OrderForm
from .models import Product
from .models import Album, Stamp,Product, Payment
from .forms import AddStampForm, PaymentForm
from django.contrib import messages
from .forms import ContactForm
import razorpay
from django.conf import settings



# Create your views here.
def index(request):
    return render(request,'index.html')


def signup(request):
    if request.method == "POST":
        first_name = request.POST['Firstname']
        last_name = request.POST['Lastname']
        username = request.POST['Username']
        email = request.POST['Email']
        password = request.POST['Password']
        data = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        data.save()
        return redirect('product_list')
    return render(request, 'signup.html')



def login(request):
    if request.method=="POST":
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('product_list')  # Redirect to the welcome page after login
        else:
            # Add an error message.
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            order.save()
            return redirect('interface')
    else:
        form = OrderForm()
    return render(request, 'place_order.html', {'form': form, 'product': product})



def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def order_success(request):
     return render(request, 'order_success.html')

@login_required
def album_view(request):
    album, created = Album.objects.get_or_create(user=request.user)
    return render(request, 'album.html', {'album': album})

@login_required
def add_stamp(request):
    if request.method == 'POST':
        form = AddStampForm(request.POST, request.FILES)
        if form.is_valid():
            stamp = form.save()
            album, created = Album.objects.get_or_create(user=request.user)
            album.stamps.add(stamp)
            return redirect('album')
    else:
        form = AddStampForm()
    return render(request, 'add_stamp.html', {'form': form})

def community_view(request):
    albums = Album.objects.all()
    return render(request, 'community.html', {'albums': albums})

@login_required
def delete_stamp(request, stamp_id):
    stamp = get_object_or_404(Stamp, id=stamp_id)
    if request.method == 'POST':
        stamp.delete()
        return redirect('album')
    return render(request, 'album.html')

@login_required
def edit_stamp(request, stamp_id):
    stamp = get_object_or_404(Stamp, id=stamp_id)
    if request.method == 'POST':
        form = AddStampForm(request.POST, request.FILES, instance=stamp)
        if form.is_valid():
            form.save()
            return redirect('album')
    else:
        form = AddStampForm(instance=stamp)
    return render(request, 'edit_stamp.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your form has been submitted.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            order_amount = int(payment.amount * 100)  # Razorpay amount is in paise
            order_currency = 'INR'
            order_receipt = 'order_rcptid_11'
            notes = {'Shipping address': 'Bommanahalli, Bangalore'} 
            order = client.order.create({
                'amount': order_amount,
                'currency': order_currency,
                'receipt': order_receipt,
                'notes': notes
            })

            payment.razorpay_order_id = order['id']
            payment.save()

            return render(request, 'interface.html', {
                'form': form,
                'order_id': order['id'],
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'amount': order_amount,
                'currency': order_currency
            })
        return redirect('order_success')
    else:
        form = PaymentForm()
    return render(request, 'interface.html', {'form': form})
