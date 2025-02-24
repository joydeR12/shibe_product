from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Debtor, Product
from .forms import ProductForm,DebtorForm
from django.views.generic.detail import DetailView
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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_details.html'


def add_debtor(request):
  if request.method == 'POST':
    form = DebtorForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('add_debtor')
    
  else:
    form = DebtorForm()
  return render(request,'add_debtor.html',{'form':form})

def list_debtors(request):
    debtors = Debtor.objects.all()
    return render(request, 'list_debtors.html', {'debtors': debtors})