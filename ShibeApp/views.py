from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Debtor, Product
from .forms import ProductForm,DebtorForm
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from django.db.models import Sum


@login_required
def home(request):
    return render(request,'home.html', {}) 
 
@login_required
def authView(request):
    if request.method == "POST":
     form = UserCreationForm(request.POST or None)
     if form.is_valid():
      form.save()
      return redirect ("ShibeApp:login")
    else:
     form = UserCreationForm()
    return render(request,'registration/signup.html', {'form': form} ) 

@login_required
def profile(request):
  return render(request,'profile.html')


@login_required
def product_list(request):
  products = Product.objects.all()
  return render(request, 'product_list.html',{'products':products})


@login_required
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




@login_required
def add_debtor(request):
    if request.method == "POST":
        # Retrieve data from the form
        debtor_name = request.POST.get("debtor_name", "")
        debtor_phone = request.POST.get("debtor_phone", "")
        product_price = float(request.POST.get("product_price", 0))
        debt_paid = float(request.POST.get("debt_paid", 0))
        name_of_products = request.POST.get("name_of_products", "")
        
        # Calculate debt_pending on the server as a fallback
        debt_pending = product_price - debt_paid
        
        # Save all data to the database
        Debtor.objects.create(
            debtor_name=debtor_name,
            debtor_phone=debtor_phone,
            product_price=product_price,
            debt_paid=debt_paid,
            debt_pending=debt_pending,
            name_of_products=name_of_products
        )

        # Redirect to the list of debtors
        return redirect("ShibeApp:list_debtors")  # Ensure this URL exists for your debtor list page

    # Render the form template
    return render(request, "add_debtor.html")


@login_required
def list_debtors(request):
    debtors = Debtor.objects.all()
    return render(request, 'list_debtors.html', {'debtors': debtors})


class DebtorDetailView(DetailView):
    model = Debtor
    template_name = 'debtor_detail.html'
    


class DebtorDeleteView(DeleteView):
    model = Debtor
    success_url = reverse_lazy('list_debtors')  # Redirect to the list of debtors after deletion


@login_required
def delete_debtor(request, debtor_id):
    if request.method == "POST":  # Using POST instead of DELETE for CSRF protection
        try:
            debtor = get_object_or_404(Debtor, pk=debtor_id)
            debtor.delete()
            return JsonResponse({"message": "Debtor deleted successfully."}, status=200)
        except Exception as e:
            return JsonResponse({"message": "Failed to delete debtor.", "error": str(e)}, status=400)
    return JsonResponse({"message": "Invalid request method."}, status=405)



@login_required
def calculate_debt(request):
    if request.method == 'POST':
        # Retrieve values from the form
        product_price = float(request.POST.get('product_price', 0))
        debt_paid = float(request.POST.get('debt_paid', 0))
        debtor_name = request.POST.get('debtor_name', '')
        debtor_phone = request.POST.get('debtor_phone', '')
        name_of_products = request.POST.get('name_of_products', '')

        # Perform the necessary calculations
        debt_pending = product_price - debt_paid
  

        # Save the data into the database
        Debtor.objects.create(
            debtor_name=debtor_name,
            debtor_phone=debtor_phone,
            product_price=product_price,
            name_of_products=name_of_products,
            debt_paid=debt_paid,
            debt_pending=debt_pending,
        )

        # Redirect to a page or render a response
        return redirect('ShibeApp:list_debtors')  # Ensure this URL name corresponds to your list view

    # Render the form template for GET requests
    return render(request, 'add_debtor.html')


def calculate_totals(request):
    # Aggregate totals from the Debtor model
    total_paid_debts = Debtor.objects.aggregate(total_paid=Sum('debt_paid'))['total_paid'] or 0
    total_pending_debts = Debtor.objects.aggregate(total_pending=Sum('debt_pending'))['total_pending'] or 0
    
    # Pass the totals to the template
    context = {
        'total_paid_debts': total_paid_debts,
        'total_pending_debts': total_pending_debts,
    }
    return render(request, 'home.html', context)



from django.contrib.auth.models import User, Group


@login_required
def manage_roles(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        group_name = request.POST.get('group')

        user = User.objects.get(id=user_id)
        group = Group.objects.get(name=group_name)

        user.groups.clear()  # Remove previous groups
        user.groups.add(group)  # Assign new role

        return redirect('home')  # Ensure this matches the URL name
    users = User.objects.all()
    groups = Group.objects.all()
    return render(request, 'manage_roles.html', {'users': users, 'groups': groups})


def role_based_redirect(request):
    if request.user.groups.filter(name="Admin").exists():
        return redirect('home')
    elif request.user.groups.filter(name="Manager").exists():
        return redirect('home')
    elif request.user.groups.filter(name="Viewer").exists():
        return redirect('home')
    return redirect('home')

