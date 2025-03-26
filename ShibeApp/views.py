import json
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Debtor, Product, DebitorProduct, DebitorOrder
from .forms import ProductForm, DebtorForm
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from django.db.models import Sum
from twilio.rest import Client
from ShibeApp import models
from django.conf import settings 
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("ShibeApp:login")
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    user = request.user  # Get the logged-in user
    return render(request, 'profile.html', {'user': user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        return redirect('profile')  # Redirect back to the profile page

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return HttpResponse('Error')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})



def save_debtor_order(request):
    total_price = 0
    products = Product.objects.all()

    if request.method == 'POST':
        # Deserialize the JSON string into a Python object (list of dictionaries)
        items = json.loads(request.POST['items'])  
        debt_paid = request.POST['debt_paid']
        debtor_name = request.POST['debtor_name']
        debtor_phone = request.POST['debtor_phone']
        debtor = Debtor.objects.create(
            debtor_name=debtor_name,
            debtor_phone=debtor_phone
        )
        for item in items:
            price = int(float(item['product_price']))  # Ensure proper type conversion
            print("Type of Price: ", type(price))
            total_price += price * int(item['quantity'])

        debt_pending = total_price - int(debt_paid)
        debitor_order = DebitorOrder.objects.create(
            debitor=debtor,
            total_price=total_price,
            debt_paid=int(debt_paid),
            debt_pending=int(debt_pending),
            status='Pending'
        )
        for item in items:
            DebitorProduct.objects.create(
                debitor_order=debitor_order,
                product=Product.objects.get(id=int(item['id'])),
                quantity=int(item['quantity']),
                is_ordered=True
            )
        return redirect('/')


    
    product = json.dumps(
        list(products.values('id', 'title', 'price')),
        default=str  # Converts Decimal to string
    )
    print(product)
    context = {
        'product': product,
    }
    return render(request, 'add_debtor.html', context)

@login_required
def list_debtors(request):
    debtors = DebitorOrder.objects.all()
    return render(request, 'list_debtors.html', {'debtors': debtors})



# Updated calculate_debt function
def calculate_debt(request):
    if request.method == 'POST':
        # Retrieve values from the form
        product_price = float(request.POST.get('product_price', 0))
        number_of_products = int(request.POST.get('number_of_products', 0))
        debt_paid = float(request.POST.get('debt_paid', 0))
        debtor_name = request.POST.get('debtor_name', '')
        debtor_phone = request.POST.get('debtor_phone', '')
        name_of_products = request.POST.get('name_of_products', '')

        # Calculate total price (product price * number of products)
        total_price = product_price * number_of_products

        # Perform the necessary calculations
        debt_pending = total_price - debt_paid

        # Save the data into the database
        Debtor.objects.create(
            debtor_name=debtor_name,
            debtor_phone=debtor_phone,
            product_price=total_price,  # Save the total price
            name_of_products=name_of_products,
            debt_paid=debt_paid,
            debt_pending=debt_pending,
        )        # Redirect to a page or render a response
        return redirect('ShibeApp:list_debtors')  # Ensure this URL name corresponds to your list view

    # Render the form template for GET requests
    return render(request, 'add_debtor.html')


@login_required
def home_combined(request):
    # Aggregate totals from the Debtor model
    total_paid_debts = DebitorOrder.objects.aggregate(total_paid=Sum('debt_paid'))['total_paid'] or 0
    total_pending_debts = DebitorOrder.objects.aggregate(total_pending=Sum('debt_pending'))['total_pending'] or 0
    
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


def fetch_product_data(request):
    # Aggregate quantity for each product
    data = (
        DebitorProduct.objects.values('product__title')  # Fetch product titles
        .annotate(total_quantity=models.Sum('quantity'))  # Sum the quantities
        .order_by('-total_quantity')  # Order by total quantity
    )

    # Format the data for the chart
    formatted_data = {
        "categories": [item['product__title'] for item in data],
        "quantities": [item['total_quantity'] for item in data],
    }

    return JsonResponse(formatted_data)

@require_POST
def delete_debtor(request, pk):
    try:
        debtor = get_object_or_404(Debtor, pk=pk)
        debtor.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
@require_POST
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        new_price = request.POST.get("price")  # Get updated price
        product.price = new_price
        product.save()
        return JsonResponse({"success": True, "message": "Price updated!"})
    except Product.DoesNotExist:
        return JsonResponse({"success": False, "message": "Product not found."}, status=404)
    

@require_http_methods(["DELETE"])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return JsonResponse({"success": True, "message": "Product deleted."})
    except Product.DoesNotExist:
        return JsonResponse({"success": False, "message": "Product not found."}, status=404)
    



