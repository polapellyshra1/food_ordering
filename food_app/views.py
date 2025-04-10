from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem, Order, OrderDetail
from django.utils.timezone import now
from django.db import transaction

def home(request):
    orders = Order.objects.all().order_by('-date_time')
    return render(request, 'home.html', {'orders': orders})

def manage_items(request):
    food_items = FoodItem.objects.all()  # Fetch all food items
    return render(request, 'manage_items.html', {'food_items': food_items})

def new_order(request):
    food_items = FoodItem.objects.all()
    return render(request, 'new_order.html', {'food_items': food_items})

def place_order(request):
    print(request.POST)
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        selected_items = request.POST.getlist("selected_items")  # List of selected food item IDs

        if not selected_items:
            return render(request, "new_order.html", {"error": "Please select at least one item."})

        total_bill = 0
        order = Order.objects.create(customer_name=customer_name, date_time=now(), total_bill_amount=0)

        for item_id in selected_items:
            quantity = int(request.POST.get(f"quantity_{item_id}", 0))
            if quantity > 0:
                food_item = FoodItem.objects.get(item_id=item_id)
                item_total = food_item.price * quantity
                total_bill += item_total
                OrderDetail.objects.create(order=order, food_item=food_item, quantity=quantity)

        order.total_bill_amount = total_bill
        order.save()

        return redirect("home")  # Redirect to the homepage after order is placed

    return redirect("new_order")  # Redirect back if method is not POST

def view_order(request, order_id):
    order = Order.objects.get(order_id=order_id)
    order_details = order.order_details.all()

    # Add subtotal (quantity × price) for each item
    for detail in order_details:
        detail.subtotal = detail.quantity * detail.food_item.price

    return render(request, 'view_order.html', {
        'order': order,
        'order_details': order_details
    })

def add_item(request):
    if request.method == 'POST':
        item_name = request.POST['item_name']
        price = request.POST['price']

        # Create new food item in DB
        FoodItem.objects.create(item_name=item_name, price=price)

        return redirect('manage_items')  # Redirect back to the list

    return render(request, 'add_item.html')

def edit_item(request, item_id):
    item = get_object_or_404(FoodItem, pk=item_id)  # Fetch the item

    if request.method == 'POST':
        item.item_name = request.POST['item_name']
        item.price = request.POST['price']
        item.save()  # Save updated values
        return redirect('manage_items')

    return render(request, 'edit_item.html', {'item': item})

def delete_item(request, item_id):
    item = get_object_or_404(FoodItem, item_id=item_id)
    item.delete()
    return redirect('manage_items')
