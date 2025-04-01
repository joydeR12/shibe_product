import json
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Debtor, Product, DebitorProduct, DebitorOrder
from .forms import ProductForm, DebtorForm
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from django.db.models import Sum
from twilio.rest import Client
from ShibeApp import models
from django.conf import settings 
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django.db.models import Sum
from decimal import Decimal
from django.db.models import Q
from django.db.models import Count

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
# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'product_list.html', {'products': products})


def product_list(request):
    query = request.GET.get('q')  # Get search parameter from URL
    products = Product.objects.all()
    
    if query:
        # Filter products where title contains the search term (case-insensitive)
        products = products.filter(title__icontains=query)
    
    return render(request, 'product_list.html', {
        'products': products,
        'search_query': query  # Pass query back to template
    })

@login_required
# def add_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#         else:
#             return HttpResponse('the product already exists please press the back arrow to continue ')
#     else:
#         form = ProductForm()
#     return render(request, 'add_product.html', {'form': form})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/products/')
            except:
                # Render error message template when save fails
                return render(request, 'error_message.html', {
                    'message': 'The product already exists. Please press back to continue.',
                    'title': 'Product Exists'
                })
        else:
            # Render error message template when form is invalid
            return render(request, 'error.html', {
                'message': 'The product already added!!!. Please press back to change the product',
                'title': 'Form Error'
            })
    
    # GET request - show empty form
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
        return redirect('/list_debtors/')


    
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
    # Get search query from request
    search_query = request.GET.get('search', '')
    
    # Get all unique debtors with their aggregated sums
    debtors = Debtor.objects.all()
    
    if search_query:
        # Filter debtors by name or phone number containing the search query (case-insensitive)
        debtors = debtors.filter(
            Q(debtor_name__icontains=search_query) |
            Q(debtor_phone__icontains=search_query)
        )
    
    # Annotate with aggregated sums
    debtors = debtors.annotate(
        total_orders=Sum('debitororder__total_price', default=0),
        total_paid=Sum('debitororder__debt_paid', default=0),
        total_pending=Sum('debitororder__debt_pending', default=0)
    ).order_by('-date_created')
    
    return render(request, 'list_debtors.html', {
        'debtors': debtors,
        'search_query': search_query
    })

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
    


def debtor_history(request, debtor_id):
    debtor = get_object_or_404(Debtor, id=debtor_id)
    orders = DebitorOrder.objects.filter(debitor=debtor).order_by('-date_created')
    return render(request, 'debtor_history.html', {
        'debtor': debtor,
        'orders': orders
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_payment(request, order_id):
    if request.method == 'POST':
        try:
            order = DebitorOrder.objects.get(id=order_id)
            new_paid = float(request.POST.get('debt_paid'))
            
            # Update payment
            order.debt_paid = new_paid
            order.debt_pending = order.total_price - new_paid
            order.save()
            
            return JsonResponse({
                'success': True,
                'new_pending': order.debt_pending
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({'success': False})


@csrf_exempt  # Keep this temporarily for debugging
def add_indv(request, debtor_id):
    total_price = 0
    products = Product.objects.all()
    debtor = get_object_or_404(Debtor,id=debtor_id)
    if request.method == 'POST':
        # Deserialize the JSON string into a Python object (list of dictionaries)
        items = json.loads(request.POST['items'])  
        debt_paid = request.POST['debt_paid']
        

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
        'debtor': debtor,
    }
    return render(request, 'add_indv.html', context)
    

def update_debt(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(DebitorOrder, id=order_id)
        paid_amount = Decimal(request.POST.get('paid_amount', 0))
        
        try:
            # Update debt values
            order.debt_paid += paid_amount
            order.debt_pending -= paid_amount
            
            # Update status if fully paid
            if order.debt_pending <= 0:
                order.status = "Completed"
                
            order.save()
            return redirect('ShibeApp:debtor_history', debtor_id=order.debitor.id)
            
        except Exception as e:
            print(f"Error updating order: {e}")
    
    return redirect('ShibeApp:list_debtors')  # Fallback redirect

def borrowed_products_chart_data(request):
    # Group by product title and SUM the quantities (not count)
    data = DebitorProduct.objects.values('product__title').annotate(
        total_quantity=Sum('quantity')  # Sum all quantities for each product
    ).order_by('-total_quantity')  # Order by highest quantity first

    # Prepare data for chart
    categories = []
    series_data = []

    for item in data:
        categories.append(item['product__title'])
        series_data.append(item['total_quantity'])  # Use the summed quantity

    return JsonResponse({
        'categories': categories,
        'series_data': series_data,  # Now contains quantities like [5, 3, 10, ...]
    })