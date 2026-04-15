from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import*
from django.contrib import messages
import razorpay
from datetime import date, timedelta
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        a = request.POST['n1']  # username
        b = request.POST['n2']  # email
        c = request.POST['n3']  # mobile
        d = request.POST['n4']  # password
        e = request.POST['n5']  # repassword
        role = request.POST['role']  # ⭐ NEW FIELD

        if user_register.objects.filter(username=a).exists():
            return messages.success("username already exists")
        else:
            if d == e:
                user_register.objects.create(
                    username=a,
                    email=b,
                    mobile=c,
                    password=d,
                    role=role      # ⭐ SAVE ROLE
                )
                return redirect(login)
            else:
                messages.success(request, 'password doesnot match')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        a = request.POST['n1']  # username
        d = request.POST['n4']  # password

        # 🔵 ADMIN LOGIN
        if a == 'admin' and d == '1234':
            request.session['admin'] = a
            return redirect(admin_home)

        # 🔵 USER / DELIVERY LOGIN
        try:
            data = user_register.objects.get(username=a)

            if data.password == d:

                # store session
                request.session['user_id'] = data.id
                request.session['username'] = data.username
                request.session['role'] = data.role


                # ✅ CHECK ROLE
                if data.role == 'user':
                    return redirect(user_home)

                elif data.role == 'delivery':
                    return redirect(delivery_dashboard)

            else:
                messages.error(request, "Invalid Password")
                return redirect(login)

        except user_register.DoesNotExist:
            messages.error(request, "Invalid Username")
            return redirect(login)
    return render(request, 'login.html')

def admin_home(request):
    if 'admin' in request.session:
        return render(request,'admin_home.html')
    else:
        return redirect(login)


def user_home(request):
    if request.session.get('role') == 'user':
        return render(request,'user_home.html')
    else:
        return redirect(login)
def add_product(request):
    if 'admin' in request.session:
        if request.method=='POST':
            a=request.POST['p1']#name
            b=request.POST['p2']#price
            c=request.POST['p3']#quantity
            d=request.FILES['p4']#image
            # e=request.POST['p5']#categories
            product.objects.create(name=a,price=b,quantity=c,image=d).save()
            return redirect(add_product)
        d=category.objects.all()
        return render(request,'add_product.html',{'data':d})
    else:
        return redirect(login)

def manage_product(request):
    if 'admin'in request.session:
        data=product.objects.all()
        return render(request,'manage_product.html',{'data':data})
    else:
        return redirect(login)

def delete_product(request,d):
    if 'admin' in request.session:
        product.objects.get(pk=d).delete()
        return redirect(manage_product)
    else:
        return redirect(login)

def update_product(request,d):
    if 'admin' in request.session:
        data=product.objects.get(pk=d)
        if request.method == 'POST':
            a = request.POST['p1']
            b = request.POST['p2']
            c = request.POST['p3']
            # d = request.FILES['m4']
            product.objects.filter(pk=d).update(name=a,price=b,quantity=c)
            return redirect(manage_product)

        return render(request,'update_product.html',{'data':data})
    else:
        return redirect(login)
def subscription(request):
    if 'admin' not in request.session:
        return redirect(login)

    plans = subscriptionPlan.objects.all()
    return render(request, 'subscription.html', {'plans': plans})

def add_plan(request):
    if 'admin' in request.session:
        if request.method=='POST':
            a=request.POST['plan_name']
            b=request.POST['plan_type']
            if subscriptionPlan.objects.filter(plan_name=a).exists():
                messages.success(request,"plan already exists")
            else:
                subscriptionPlan.objects.create(plan_name=a,plan_type=b).save()
                messages.success(request,"plan created successfully")
            return redirect(subscription)
        return render(request,'add_plan.html')


def subscribe_plan(request,plan_id):
    if 'admin' in request.session:
        plan=subscriptionPlan.objects.get(pk=plan_id)
        booking.objects.create(user=request.user,plan=plan,payment_status='paid')
        return redirect(bookings)


def add_category(request):
    if 'admin' in request.session:
        if request.method=='POST':
            a=request.POST['cat']
            if category.objects.filter(name=a).exists():
                messages.success(request,"category already exists")
            else:
                category.objects.create(name=a).save()
            return redirect(add_product)
        return render(request,'add_category.html')
def user_product(request):
    if request.session.get('role') == 'user':

        products = product.objects.all()
        categories = category.objects.all()
        plans = subscriptionPlan.objects.all()

        # SEARCH
        search = request.GET.get('search')
        if search:
            products = products.filter(name__icontains=search)

        # CATEGORY FILTER
        cat = request.GET.get('category')
        if cat:
            products = products.filter(category_id=cat)

        context = {
            'data': products,
            'categories': categories,
            'plans': plans,
        }

        return render(request, 'user_product.html', context)

    else:
        return redirect(login)


def product_detail(request, pk):
    if request.session.get('role') == 'user':
        data = product.objects.get(pk=pk)
        return render(request, 'product_detail.html', {'data': data})
    else:
        return redirect(login)


def addcart(request, d):
    if request.session.get('role') == 'user':
        prod = get_object_or_404(product, pk=d)
        user = user_register.objects.get(username=request.session['username'])

        if cart.objects.filter(user_details=user, product_details=prod).exists():
            item = cart.objects.get(user_details=user, product_details=prod)
            item.quantity += 1
            item.save()
        else:
            cart.objects.create(
                user_details=user,
                product_details=prod,
                quantity=1,
                total_price=0   # ✅ price will be calculated later
            )

        return redirect(view_cart)
    else:
        return redirect(login)



def view_cart(request):

    if request.session.get('role') == 'user':

        user = user_register.objects.get(
            username=request.session['username']
        )

        cart_items = cart.objects.filter(user_details=user)
        plans = subscriptionPlan.objects.all()

        total = 0

        for item in cart_items:

            price = item.product_details.price
            qty = item.quantity

            if item.plan_details:

                if item.plan_details.plan_type == 'daily':
                    item.total_price = price * qty

                elif item.plan_details.plan_type == 'weekly':
                    item.total_price = price * qty * 7

                elif item.plan_details.plan_type == 'monthly':
                    item.total_price = price * qty * 30

            else:
                item.total_price = price * qty

            total += item.total_price

        return render(request, 'cart.html', {
            'cart_items': cart_items,
            'total': total,
            'plans': plans
        })

    else:
        return redirect(login)

def update_quantity(request, cart_id, action):

    if request.session.get('role') != 'user':
        return redirect(login)

    cart_item = cart.objects.get(id=cart_id)  # ✅ Fix: was Cart (capital C), should match your model name

    if action == 'increase':
        cart_item.quantity += 1

    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1

    # ✅ Recalculate total_price after quantity change
    price = cart_item.product_details.price
    qty = cart_item.quantity

    if cart_item.plan_details:
        if cart_item.plan_details.plan_type == 'daily':
            cart_item.total_price = price * qty
        elif cart_item.plan_details.plan_type == 'weekly':
            cart_item.total_price = price * qty * 7
        elif cart_item.plan_details.plan_type == 'monthly':
            cart_item.total_price = price * qty * 30
    else:
        cart_item.total_price = price * qty

    cart_item.save()
    return redirect(view_cart)
def select_plan(request, plan_id, cart_id):
    if request.session.get('role') == 'user':

        user = user_register.objects.get(username=request.session['username'])
        cart_item = cart.objects.get(id=cart_id, user_details=user)
        plan = subscriptionPlan.objects.get(id=plan_id)

        # attach selected plan
        cart_item.plan_details = plan

        product_price = cart_item.product_details.price
        qty = cart_item.quantity

        # ✅ calculate based on plan_type
        if plan.plan_type == 'daily':
            cart_item.total_price = product_price * qty

        elif plan.plan_type == 'weekly':
            cart_item.total_price = product_price * qty * 7

        elif plan.plan_type == 'monthly':
            cart_item.total_price = product_price * qty * 30

        cart_item.save()

        return redirect(view_cart)

    else:
        return redirect(login)


def remove_cart(request, id):
    if request.session.get('role') == 'user':
        user = user_register.objects.get(username=request.session['username'])
        item = get_object_or_404(cart, pk=id, user_details=user)  # ✅ make sure 'cart' matches your model name
        item.delete()
        return redirect(view_cart)
    else:
        return redirect(login)



def subscriptionplan(request):
    if request.session.get('role') == 'user':
        plans= subscriptionPlan.objects.all()
        return render(request,'subscriptionplan.html',{'plans':plans})
    else:
        return redirect(login)


def view_wishlist(request):
    if request.session.get('role') == 'user':
        user = user_register.objects.get(username=request.session['username'])

        # use correct field
        wishlist_items = Wishlist.objects.filter(user=user)

        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return redirect(login)


def add_wishlist(request, id):
    if request.session.get('role') == 'user':
        user = user_register.objects.get(username=request.session['username'])
        prod = product.objects.get(id=id)

        # IMPORTANT → use product_details (not product)
        if not Wishlist.objects.filter(user=user, product_details=prod).exists():
            Wishlist.objects.create(user=user, product_details=prod)

        return redirect(view_wishlist)
    else:
        return redirect(login)

def payment(request,d):
    amount = d*100
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    return render(request, "payment.html",{'amount':amount})




def payment_success(request):
    if request.session.get('role') != 'user':
        return redirect(login)

    payment_id = request.POST.get('razorpay_payment_id')

    user = user_register.objects.get(username=request.session['username'])
    cart_items = cart.objects.filter(user_details=user)
    delivery_boy = user_register.objects.filter(role='delivery').first()

    for item in cart_items:

        # ✅ Deduct stock quantity
        prod = item.product_details
        if prod.quantity >= item.quantity:
            prod.quantity -= item.quantity
            prod.save()
        else:
            # not enough stock, skip or handle error
            messages.error(request, f"Not enough stock for {prod.name}")
            return redirect(view_cart)

        # Decide subscription duration
        if item.plan_details.plan_type == 'daily':
            end_date = date.today() + timedelta(days=30)

        elif item.plan_details.plan_type == 'weekly':
            end_date = date.today() + timedelta(days=84)

        elif item.plan_details.plan_type == 'monthly':
            end_date = date.today() + timedelta(days=365)

        Booking.objects.create(
            user=user,
            product=item.product_details,
            plan=item.plan_details,
            quantity=item.quantity,
            total_price=item.total_price,
            start_date=date.today(),
            end_date=end_date,
            next_delivery=date.today(),
            payment_status='paid',
            status='active',
            transaction_id=payment_id,
            assigned_delivery=delivery_boy
        )

    cart_items.delete()
    return redirect(my_orders)

def my_orders(request):
    if request.session.get('role') != 'user':
        return redirect(login)

    user = user_register.objects.get(username=request.session['username'])

    orders = Booking.objects.filter(user=user).order_by('-id')

    return render(request, 'my_orders.html', {'orders': orders})

def delivery_dashboard(request):
    if request.session.get('role') != 'delivery':
        return redirect(login)

    delivery_user = user_register.objects.get(
        username=request.session['username']
    )

    orders = Booking.objects.filter(
        assigned_delivery=delivery_user,
        payment_status='paid'
    ).exclude(status='cancelled').order_by('next_delivery')

    active_count  = orders.filter(status='active').count()
    paused_count  = orders.filter(status='paused').count()
    expired_count = orders.filter(status='expired').count()

    return render(request, 'delivery_dashboard.html', {
        'orders'        : orders,
        'active_count'  : active_count,
        'paused_count'  : paused_count,
        'expired_count' : expired_count,
    })
def assign_delivery(request, booking_id, delivery_id):
    booking = Booking.objects.get(id=booking_id)
    delivery_boy = user_register.objects.get(id=delivery_id)

    booking.assigned_delivery = delivery_boy
    booking.save()

    return redirect(bookings)






def update_delivery(request, order_id, action):

    booking = get_object_or_404(Booking, id=order_id)

    # ❌ Do not deliver paused or expired subscription
    if booking.status != 'active':
        return redirect(delivery_dashboard)

    if action == 'shipped':
        booking.delivery_status = 'shipped'

    elif action == 'out_for_delivery':
        booking.delivery_status = 'out_for_delivery'

    elif action == 'delivered':
        booking.delivery_status = 'delivered'

        # ✅ Move next delivery based on plan
        if booking.plan.plan_type == 'daily':
            booking.next_delivery += timedelta(days=1)

        elif booking.plan.plan_type == 'weekly':
            booking.next_delivery += timedelta(days=7)

        elif booking.plan.plan_type == 'monthly':
            booking.next_delivery += timedelta(days=30)

        # ✅ Stop when subscription ends
        if booking.next_delivery > booking.end_date:
            booking.status = 'expired'

    booking.save()
    return redirect(delivery_dashboard)

def pause_subscription(request, id):
    booking = Booking.objects.get(id=id)
    booking.status = 'paused'
    booking.save()
    return redirect(my_orders)
def resume_subscription(request, id):
    booking = Booking.objects.get(id=id)
    booking.status = 'active'
    booking.save()
    return redirect(my_orders)
def cancel_subscription(request, id):
    booking = Booking.objects.get(id=id)
    booking.status = 'cancelled'
    booking.save()
    return redirect(my_orders)



def admin_bookings(request):
    # Only admin can access
    if 'admin' not in request.session:
        return redirect(login)

    # Get all bookings
    bookings = Booking.objects.all().order_by('-start_date')

    # Get all delivery boys for assignment
    delivery_boys = user_register.objects.filter(role='delivery')

    return render(request, 'admin_bookings.html', {
        'bookings': bookings,
        'delivery_boys': delivery_boys
    })


from django.contrib import messages

from .models import Contact
from django.contrib import messages

def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )

        messages.success(request, "Message Sent Successfully!")
        return redirect('contact')

    return render(request, 'contact.html')

def admin_messages(request):
    if 'admin' not in request.session:
        return redirect(login)

    messages_list = Contact.objects.all().order_by('-created_at')

    return render(request, 'admin_messages.html', {
        'messages_list': messages_list
    })

def my_subscription(request):
    if 'user_id' not in request.session:
        return redirect(login)

    # get logged-in user using ID (correct way)
    user_obj = user_register.objects.get(id=request.session['user_id'])

    # fetch subscriptions
    subscriptions = Booking.objects.filter(user=user_obj).order_by('-start_date')

    return render(request, 'my_subscription.html', {
        'subscriptions': subscriptions
    })

def logout(request):
    request.session.flush()
    return redirect(index)

def profile(request):
    if request.session.get('role') != 'user':
        return redirect('login')

    user_obj = user_register.objects.get(
        id=request.session['user_id']
    )

    total_orders = Booking.objects.filter(user=user_obj).count()
    active_subscriptions = Booking.objects.filter(
        user=user_obj,
        status='active'
    ).count()

    return render(request, 'profile.html', {
        'user': user_obj,
        'total_orders': total_orders,
        'active_subscriptions': active_subscriptions
    })


def update_profile(request):
    if request.session.get('role') != 'user':
        return redirect(login)

    user_obj = user_register.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        user_obj.email = request.POST.get('email')
        user_obj.mobile = request.POST.get('mobile')
        user_obj.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect(profile)

    return render(request, 'update_profile.html', {'user': user_obj})