from .__utils import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.validators import EmailValidator

from .models import *
from .forms import *  # OrderForm, CreateUserForm, CustomerForm, OrderCustomerForm
from .filters import OrderFilter, CustomerFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

import datetime
import xlwt

# Defines the register userpage view
# Funtion to close flock


@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if request.POST["first_name"]:
            if validate_name(request.POST["first_name"]):
                if request.POST["last_name"]:
                    if validate_name(request.POST["last_name"]):
                        if request.POST["email"]:

                            if form.is_valid():

                                user = form.save()
                                f = user.first_name
                                l = user.last_name
                                e = user.email
                                username = form.cleaned_data.get("username")
                                first = form.cleaned_data.get("first_name")
                                last = form.cleaned_data.get("last_name")
                                email = form.cleaned_data.get("email")

                                messages.success(
                                    request, "Account was created for " + username
                                )

                                return redirect("login")
                            else:
                                print("Form not valid")
                                messages.info(
                                    request,
                                    "Form is not valid. It did not validate.",
                                )

                        else:
                            print("No email")
                            messages.info(request, "Please provide your email")

                    else:
                        print("Last name not valid")
                        messages.info(
                            request, "Please provide a valid last name")

                else:
                    print("No last name")
                    messages.info(request, "Please provide your last name")
            else:
                print("First name not valid")
                messages.info(request, "Please provide a valid first name")
        else:
            print("No first name")
            messages.info(request, "Please provide your first name")

    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)


# Defines the login view


@unauthenticated_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            locations_list = []
            locations = Delivery.objects.all()

            for n in locations:
                locations_list.append(n.customer_id)

            if not user.is_staff:
                if user.customer.id not in locations_list:

                    return redirect("address")

                else:
                    return redirect("home")

            else:
                return redirect("home")

        else:
            messages.info(request, "Username OR Password is incorrect")

    context = {}
    return render(request, "accounts/login.html", context)


# Defines the logout function


def logoutUser(request):
    logout(request)
    return redirect("login")

# Defines the Address function


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def address(request):
    customer = request.user.customer

    address_form = AddressForm(initial={"customer": customer})

    if request.method == 'POST':
        address_form = AddressForm(request.POST)

        if address_form.is_valid():
            address_form.save()

            if customer.phone:
                return redirect('home')

            else:
                return redirect('account')

    context = {'address_form': address_form}

    return render(request, 'accounts/address.html', context)


# Defines the admin view


@login_required(login_url="login")
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    feedbacks = Feedback.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {
        "orders": orders,
        "customers": customers,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending,
        "total_customers": total_customers,
        "feedbacks": feedbacks,
    }

    return render(request, "accounts/dashboard.html", context)


# Defines the customer view


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def userPage(request):
    customer = request.user.customer
    orders = customer.order_set.all()
    feedbacks = Feedback.objects.all()

    user_feedbacks = feedbacks.filter(customer=customer)

    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {
        "orders": orders,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending,
        "customer": customer,
        "user_feedbacks": user_feedbacks,
    }
    return render(request, "accounts/user.html", context)


# Defines the customer settings view


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    location = Delivery.objects.get(customer_id=customer.id)

    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid:
            form.save()
            return redirect("/")

    context = {"form": form, "location": location}
    return render(request, "accounts/account_settings.html", context)


# Defines the products view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def products(request):
    products = Product.objects.all()
    flock = Flock.objects.all()

    active_flock = []
    broilers_count = []
    layers_count = []
    results = []
    for i in flock:

        results.append(i)

        active_flock.append(i.flock_quantity)

    for n in results:

        if n.flock_breedtype == "Broiler":
            broilers_count.append(n.flock_quantity)

        else:
            layers_count.append(n.flock_quantity)

    broilers_quantity = sum(broilers_count)
    layers_quantity = sum(layers_count)

    context = {
        "products": products,
        "broilers_quantity": broilers_quantity,
        "layers_quantity": layers_quantity,
    }
    return render(request, "accounts/products.html", context)

# allows the customer to view all their orders


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def customerProducts(request):
    products = Product.objects.all()
    flock = Flock.objects.all()

    active_flock = []
    broilers_count = []
    layers_count = []
    results = []
    for i in flock:
        results.append(i)
        active_flock.append(i.flock_quantity)
    for n in results:
        if n.flock_breedtype == "Broiler":
            broilers_count.append(n.flock_quantity)
        else:
            layers_count.append(n.flock_quantity)

    broilers_quantity = sum(broilers_count)
    layers_quantity = sum(layers_count)

    context = {
        "products": products,
        "broilers_quantity": broilers_quantity,
        "layers_quantity": layers_quantity,
    }
    return render(request, "accounts/customer_products.html", context)


# Defines the all customers view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def allCustomers(request):

    customers = Customer.objects.all()
    all_customers_count = customers.count()

    myFilter = CustomerFilter(request.GET, queryset=customers)
    customers = myFilter.qs

    context = {
        "customers": customers,
        "all_customers_count": all_customers_count,
        "myFilter": myFilter,
    }
    return render(request, "accounts/all_customers.html", context)


# Defines the all orders view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def allOrders(request):
    orders = Order.objects.all()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    pending_list = []
    out_for_delivery_list = []
    delivered_list = []

    for n in orders:
        if n.status == "Pending":
            pending_list.append(n)
        if n.status == "Out for delivery":
            out_for_delivery_list.append(n)
        if n.status == "Delivered":
            delivered_list.append(n)

    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {
        "orders": orders,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending,
        "myFilter": myFilter,
        "pending_list": pending_list,
        "out_for_delivery_list": out_for_delivery_list,
        "delivered_list": delivered_list,
    }
    return render(request, "accounts/all_orders.html", context)


# Defines the all customer orders view


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def allCustomerOrders(request):
    customer = request.user.customer
    orders = customer.order_set.all()

    pending_list = []
    out_for_delivery_list = []
    delivered_list = []

    for n in orders:
        if n.status == "Pending":
            pending_list.append(n)
        if n.status == "Out for delivery":
            out_for_delivery_list.append(n)
        if n.status == "Delivered":
            delivered_list.append(n)

    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {
        "orders": orders,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending,
        "pending_list": pending_list,
        "outfordelivery_list": out_for_delivery_list,
        "delivered_list": delivered_list,
    }
    return render(request, "accounts/all_customer_orders.html", context)


# Defines the admin's customer view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    feedbacks = Feedback.objects.all()
    customer_feedback = feedbacks.filter(customer=customer)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        "customer": customer,
        "orders": orders,
        "order_count": order_count,
        "myFilter": myFilter,
        "feedbacks": feedbacks,
        "customer_feedback": customer_feedback,
    }
    return render(request, "accounts/customer.html", context)


# Defines the create order view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    # OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'order_quantity', 'status'), extra=3)

    form = OrderForm(initial={"customer": customer})
    print(customer)

    # formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == "POST":
        print("Printing POST:", request.POST)
        form = OrderForm(request.POST)
        # formset = OrderFormSet(request.POST, instance=customer)
        print(request.POST)
        if form.is_valid():
            s = form.save()

            return redirect(f"/sales/{s.id}/")

    context = {"form": form, "customer.id": customer.id}

    return render(request, "accounts/order_form.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def createCustomerOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    # customer_name = customer.name
    # print(customer_name)
    # customer = request.user.customer

    # order = customer.order_set.all()

    form = OrderCustomerForm(initial={"customer": customer})

    if request.method == "POST":
        form = OrderCustomerForm(request.POST)

        total_flock = get_total_flock()
        broilers_total = int(total_flock["broilers_quantity"])
        layers_total = int(total_flock["layers_quantity"])

        product_id = int(request.POST["product"])
        order_count = int(request.POST["order_quantity"])

        product = Product.objects.get(id=product_id)

        print("print 1", request.POST)

        if product.name == "Broiler":

            if order_count <= broilers_total:
                if form.is_valid():
                    s = form.save()

                    return redirect(f"/sales/{s.id}/")
            else:
                print("Insufficient Broilers")
                messages.info(request, "Insufficient Broilers")
        else:

            if order_count <= layers_total:
                if form.is_valid():
                    v = form.save()

                    return redirect(f"/sales/{v.id}/")
            else:
                print("Insufficient Layers")
                messages.info(request, "Insufficient Layers")

    context = {"form": form, "customer": customer}

    return render(request, "accounts/customer_order_form.html", context)


# Defines the update order view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {"form": form, "customer": customer, "order": order}

    return render(request, "accounts/order_form.html", context)


# Defines the delete order view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "customer"])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect("/")
    context = {"item": order}
    return render(request, "accounts/delete.html", context)


# Defines the delete customer view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect("/")
    context = {"item": customer}
    return render(request, "accounts/delete_customer.html", context)

# Defines the delete feedback view


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def deleteFeedback(request, pk):
    feedback = Feedback.objects.get(id=pk)
    if request.method == "POST":
        feedback.delete()
        return redirect("/feedback/")
    context = {"feedback": feedback}
    return render(request, "accounts/delete_feedback.html", context)

# Defines the give feedback view


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def giveFeedback(request, pk):
    customer = request.user.customer
    feedbacks = Feedback.objects.all()

    user_feedbacks = feedbacks.filter(customer=customer)

    feedbacks_form = GiveFeedbackForm(initial={"customer": customer})

    if request.method == "POST":
        feedbacks_form = GiveFeedbackForm(request.POST)
        if feedbacks_form.is_valid():
            feedbacks_form.save()
            return redirect("/feedback/")

    context = {
        "feedbacks_form": feedbacks_form,
        "customer": customer,
        "user_feedbacks": user_feedbacks,
    }

    return render(request, "accounts/give_feedback.html", context)

# Defines the health management view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "health"])
def healthManager(request):

    flock = Flock.objects.all()

    medicine = Medicine.objects.all()

    vaccinations = Vaccination.objects.all()

    context = {"flock": flock, "medicine": medicine,
               "vaccinations": vaccinations}

    return render(request, "accounts/health_manager.html", context)

# Defines the brooder management view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "brooder"])
def brooderManager(request):

    brooders = Brooder.objects.all()
    feeds = Feed.objects.all()
    feedsusage = FeedUsage.objects.all()

    context = {"brooders": brooders, "feeds": feeds, "feedsusage": feedsusage}

    return render(request, "accounts/brooder_manager.html", context)

# Defines the Flock view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def flock(request):
    flock = Flock.objects.all()
    orders = Order.objects.all()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    active_flock = []
    for i in flock:

        flock_count = i.flock_quantity

        active_flock.append(flock_count)

    number_of_active_flock = sum(active_flock)

    context = {
        "flock": flock,
        "delivered": delivered,
        "pending": pending,
        "number_of_active_flock": number_of_active_flock,
    }

    return render(request, "accounts/flock.html", context)

# Defines the Brooder view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def brooder(request):

    brooders = Brooder.objects.all()

    context = {"brooders": brooders}

    return render(request, "accounts/brooder.html", context)

# Defines the Sales view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "customer"])
def sales(request, pk):
    id_string = str(request)
    id = "id:", id_string.split("/")[-2]

    id_int = int(id[1])

    order = Order.objects.get(id=id_int)
    order.sale
    print(order.sale)

    all_sales = Sale.objects.all()

    context = {
        "id_int": id_int,
        "all_sales": all_sales,
        "customer": order.customer,
        "product": order.product,
        "price": int(order.product.price),
        "status": order.status,
        "quantity": int(order.order_quantity),
        "accepted": order.is_accepted,
        "paid": order.is_paid,
        "delivered": order.is_delivered,
        "delivery_date": order.delivery_date,
        "total_cost": order.product.price * order.order_quantity,
    }

    return render(request, "accounts/sales.html", context)

# Defines the Vaccination view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "health"])
def vaccinations(request):

    vaccinations = Vaccination.objects.all()

    context = {"vaccinations": vaccinations}

    return render(request, "accounts/vaccinations.html", context)

# Defines the Medicine view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "health"])
def medicine(request):

    medicine = Medicine.objects.all()

    context = {"medicine": medicine}

    return render(request, "accounts/medicine.html", context)

# Defines the Feeds view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "brooder"])
def feeds(request):

    feeds = Feed.objects.all()

    context = {"feeds": feeds}

    return render(request, "accounts/feeds.html", context)

# Defines the Feeds Usage view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "brooder"])
def feedsUsage(request):

    feedsusages = FeedUsage.objects.all()

    context = {"feedsusages": feedsusages}

    return render(request, "accounts/feeds_usage.html", context)

# Defines the add feed usage view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "brooder"])
def addFeedsUsage(request):

    add_feedusage_form = AddFeedUsageForm()

    if request.method == "POST":

        feed_id = int(request.POST["feed"])
        feed_quantity_used = int(request.POST["feed_quantity_used"])

        feed_affected = Feed.objects.get(id=feed_id)

        if feed_quantity_used <= feed_affected.feed_quantity:

            add_feedusage_form = AddFeedUsageForm(request.POST)

            updated_feed_quantity = feed_affected.feed_quantity - feed_quantity_used

            if add_feedusage_form.is_valid():
                feed_to_update = Feed.objects.get(id=feed_id)
                feed_to_update.feed_quantity = updated_feed_quantity
                feed_to_update.save()

                add_feedusage_form.save()

                return redirect("/brooder_manager/")

        else:
            print("Not possible")

    context = {"add_feedusage_form": add_feedusage_form}

    return render(request, "accounts/add_feedusage.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "brooder", "health"])
def calender(request):
    all_flock = Flock.objects.all()
    context = {'all_flock': all_flock}

    return render(request, "accounts/calender.html", context)

# Defines the add mortality view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "health"])
def mortality(request):

    mortalities = Mortality.objects.all()

    context = {"mortalities": mortalities}

    return render(request, "accounts/mortality.html", context)


# Defines the reports view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def reports(request):
    all_orders = Order.objects.all()
    all_customers = Customer.objects.all()
    all_feedback = Feedback.objects.all()
    all_medicine = Medicine.objects.all()
    all_feeds = Feed.objects.all()
    all_products = Product.objects.all()
    all_flock = Flock.objects.all()
    all_mortalities = Mortality.objects.all()
    all_feedusages = FeedUsage.objects.all()
    all_income = Income.objects.all()
    all_sales = Sale.objects.all()
    all_expenses = Expense.objects.all()
    locations = Delivery.objects.all()

    print(all_sales)
    for sale in all_sales:
        print(sale)
    # print(all_orders)
    # print(all_feeds)
    # print(all_income)
    # print(all_expenses)

    context = {
        'all_orders': all_orders.count(),
        'all_customers': all_customers.count(),
        'all_feedback': all_feedback.count(),
        'all_medicine': all_medicine.count(),
        'all_feeds': all_feeds.count(),
        'all_products': all_products.count(),
        'all_flock': all_flock.count(),
        'all_mortalities': all_mortalities.count(),
        'all_feedusages': all_feedusages.count(),
        'all_income': all_income.count(),
        'all_sales': all_sales.count(),
        'all_expenses': all_expenses.count(),
        'locations': locations.count(),
    }

    return render(request, "accounts/reports.html", context)

# Defines the all feedback view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def allFeedback(request):

    feedbacks = Feedback.objects.all()

    context = {"feedbacks": feedbacks}

    return render(request, "accounts/all_feedback.html", context)

# Defines the add flock view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def addFlock(request):

    add_flock_form = AddFlockForm()

    if request.method == "POST":
        add_flock_form = AddFlockForm(request.POST)
        # flock quantity added
        added_flock = int(request.POST["flock_quantity"])

        brooder = request.POST["brooder"]  # brooder
        flock = Flock.objects.all()

        print("flock", type(flock), len(flock), "\n")
        brooder_list = []

        # check if the brooder is empty
        if len(flock):
            for n in flock:

                # finds the brooder selected
                if n.brooder_id == int(brooder):

                    brooder_list.append(n.flock_quantity)

                brooder_sum = sum(brooder_list)

                # checks whether flock will exceed capacity
                if added_flock + brooder_sum > 100:
                    print("More than 100")
                    messages.info(
                        request, "The flock in that brooder exceeds the capacity"
                    )

                else:
                    if add_flock_form.is_valid:
                        b = add_flock_form.save()

                        exp = Expense(
                            expense_desc=b.flock_breedtype, expense_amount=b.flock_price)
                        exp.save()

                    return redirect("/flock/")

        else:
            if added_flock > 100:
                print("Brooder cannot take more than 100")
                messages.info(
                    request, "Brooder cannot take more than 100"
                )

            else:
                if add_flock_form.is_valid:
                    v = add_flock_form.save()

                    expn = Expense(expense_desc=v.flock_breedtype,
                                   expense_amount=v.flock_price)
                    expn.save()

                return redirect("/flock/")

    context = {"add_flock_form": add_flock_form}

    return render(request, "accounts/add_flock.html", context)

# Defines the add feed view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def addFeed(request):

    add_feed_form = AddFeedForm()

    if request.method == "POST":
        add_feed_form = AddFeedForm(request.POST)
        if add_feed_form.is_valid:

            b = add_feed_form.save()

            exp = Expense(expense_desc=b.feed_name,
                          expense_amount=b.feed_price)
            exp.save()

            return redirect("/brooder_manager/")

    context = {"add_feed_form": add_feed_form}

    return render(request, "accounts/add_feed.html", context)


# Defines the add medicine view
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def addMedicine(request):
    add_medicine_form = AddMedicineForm()

    if request.method == "POST":
        add_medicine_form = AddMedicineForm(request.POST)
        if add_medicine_form.is_valid:

            try:

                b = add_medicine_form.save()

                exp = Expense(expense_desc=b.medicine_name,
                              expense_amount=b.medicine_price)
                exp.save()

            except ValidationError:
                print("The date cannot be in the past!")
                return redirect("/add_medicine/")

            return redirect("/health_manager/")

    context = {"add_medicine_form": add_medicine_form}

    return render(request, "accounts/add_medicine.html", context)

# Defines the add vaccination view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def addVaccination(request):

    add_vaccination_form = NewVaccinationForm()

    if request.method == "POST":
        add_vaccination_form = NewVaccinationForm(request.POST)
        if add_vaccination_form.is_valid:
            add_vaccination_form.save()

            return redirect("/health_manager/")

    context = {"add_vaccination_form": add_vaccination_form}

    return render(request, "accounts/add_vaccination.html", context)

# Defines the add mortality view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def addMortality(request):

    add_mortality_form = NewMortalityForm()

    if request.method == "POST":
        add_mortality_form = NewMortalityForm(request.POST)

        flock_id = int(request.POST["flock"])
        flock_mortality_count = int(request.POST["mortality_count"])

        flock_affected = Flock.objects.get(id=flock_id)

        if flock_mortality_count <= flock_affected.flock_quantity:

            updated_flock_count = flock_affected.flock_quantity - flock_mortality_count

            if add_mortality_form.is_valid:
                flock_to_update = Flock.objects.get(id=flock_id)
                flock_to_update.flock_quantity = updated_flock_count
                flock_to_update.save()

                close_flock(flock_id)

                add_mortality_form.save()

        else:
            print("Not possible. Mortality exceeds flock count")
            messages.info(
                request, "Not possible. Mortality exceeds flock count")

        return redirect("/health_manager/")

    context = {"add_mortality_form": add_mortality_form}

    return render(request, "accounts/add_mortality.html", context)

# Defines the cancel order view


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def cancelOrder(request, id):

    order = Order.objects.get(id=id)
    v = order.delete()
    print(v)

    context = {}
    # return render(request, 'accounts/cancel_order.html', context)
    return redirect("/user/")

# Defines the index view used to render the website


def index(request):

    context = {}

    return render(request, "accounts/index.html", context)

# Defines the payment view


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def payment(request, id):
    print(request)
    customer = request.user.customer

    id_string = str(request)
    id = "id:", id_string.split("/")[-2]
    id_int = int(id[1])

    order = Order.objects.get(id=id_int)

    user = order.customer.user
    print(customer)
    user_email = order.customer.user.email
    user_phone = order.customer.phone
    user_firstname = order.customer.user.first_name
    user_lastname = order.customer.user.last_name

    deliveries = Delivery.objects.all()

    id_list = []
    for delivery in deliveries:
        id_list.append(delivery.customer.id)

    addr_list = []
    if order.customer.id in id_list:
        addr_list.append(order.customer.id)
        print("Address already configured")
        messages.info(request, "Address already configured")
        delivery_id = addr_list[0]

        customer_delivery = Delivery.objects.get(customer_id=delivery_id)

        form = DeliveryForm(instance=customer_delivery)

    else:
        print('Not yet addresed')

        form = DeliveryForm(initial={"customer": customer})

        if request.method == "POST":
            form = DeliveryForm(request.POST)
            print("request.post/:", request.POST)
            print("id list/:", id_list)
            if form.is_valid():

                print("saved")
                a = form.save()
                print(a)

                messages.info(request, "Address saved")

    context = {
        "id_int": id_int,
        "customer": order.customer,
        "product": order.product,
        "price": int(order.product.price),
        "status": order.status,
        "quantity": int(order.order_quantity),
        "accepted": order.is_accepted,
        "paid": order.is_paid,
        "delivered": order.is_delivered,
        "delivery_date": order.delivery_date,
        "total_cost": order.product.price * order.order_quantity,
        "order": order,
        "user": user,
        "user_email": user_email,
        "user_phone": user_phone,
        "user_firstname": user_firstname,
        "user_lastname": user_lastname,
        "form": form
    }

    return render(request, "accounts/payment.html", context)

# Defines the Feedback view


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def Feedbacks(request):
    customer = request.user.customer
    print(customer)
    feedbacks = Feedback.objects.all()

    user_feedbacks = feedbacks.filter(customer=customer)
    context = {"customer": customer, "user_feedbacks": user_feedbacks}
    return render(request, "accounts/feedback.html", context)


# Defines the order success view
@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def success(request, id):
    print("URL DATA: ", id)

    if confirm_order(id):
        return redirect("/user/")

# Defines the Income view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def income(request):

    context = {}

    return render(request, "accounts/income.html", context)

# Defines the Expense view


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def expenses(request):

    context = {}

    return render(request, "accounts/expenses.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Delivery' +\
        str(datetime.datetime.now())+'.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Delivery')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Customer', 'Address', 'Street', 'Road']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = Delivery.objects.all().values_list(
            'customer', 'address', 'street', 'road')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response

    context = {}

    return render(request, "accounts/expenses.html", context)
