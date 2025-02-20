from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from . models import Product
from .forms import ProductForm

@login_required
def home(request):
    return render(request,'home.html', {}) 
 

def authView(request):
    if request.method == "POST":
     form = UserCreationForm(request.POST or None)
     if form.is_valid():
      form.save()
      return redirect ("ShibeApp:login")
    else:
     form = UserCreationForm()
    return render(request,'registration/signup.html', {'form': form} ) 


def profile(request):
  return render(request,'profile.html')

def product_list(request):
  products = Product.objects.all()
  return render(request, 'product_list.html',{'products':products})

def add_product(request):
  if request.method == 'POST':
    form = ProductForm(request.POST,request.FILES)
    if form .is_valid():
      form.save()
      return redirect('product_list')
  
  else:
    form = ProductForm()
  return render(request, 'add_product.html', {'form':form})

