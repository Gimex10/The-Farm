from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import *  # OrderForm, CreateUserForm, CustomerForm, OrderCustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Defines the register userpage view
# Funtion to close flock


def close_flock(id):
    flock = Flock.objects.get(id=id)
    if flock.flock_quantity == 0:
        flock.is_closed = True
        flock.save()
        print('is closed updated')


@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

# Defines the login view


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

# Defines the logout function


def logoutUser(request):
    logout(request)
    return redirect('login')

# Defines the admin view


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    feedbacks = Feedback.objects.all()

    for customer in customers:
        print(customer.name)
        print(customer.user)
        print(customer.id)

    # for feedback in feedbacks:
    # print(feedback)
    # print(feedback.feedback_info)
    # print(feedback.customer.email)
    # print(feedback.customer.id)

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending, 'total_customers': total_customers,
               'feedbacks': feedbacks,
               }

    return render(request, 'accounts/dashboard.html', context)

# Defines the customer view


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    customer = request.user.customer
    orders = customer.order_set.all()
    feedbacks = Feedback.objects.all()

    # print(feedbacks)
    # print(customer.id)

    user_feedbacks = feedbacks.filter(customer=customer)
    # print(user_feedbacks)

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending,
               'customer': customer, 'user_feedbacks': user_feedbacks, }
    return render(request, 'accounts/user.html', context)

# Defines the customer settings view


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid:
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)

# Defines the products view


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
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

    # print(results)
    # print(active_flock)
    for n in results:
        # print(n)
        # print(n.flock_breedtype)

        if n.flock_breedtype == 'Broiler':
            broilers_count.append(n.flock_quantity)
            # print(broilers_count)
        else:
            layers_count.append(n.flock_quantity)
            # print(layers_count)

    # print(broilers_count)
    broilers_quantity = sum(broilers_count)
    layers_quantity = sum(layers_count)
    # print(layers_count)
    #number_of_active_flock = sum(active_flock)
    # print(number_of_active_flock)

    context = {'products': products, 'broilers_quantity': broilers_quantity,
               'layers_quantity': layers_quantity, }
    return render(request, 'accounts/products.html', context)
# Defines the all customers view


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def allCustomers(request):
    customers = Customer.objects.all()

    for i in customers:
        print(i.id)
        print(i.name)

    context = {'customers': customers}
    return render(request, 'accounts/all_customers.html', context)
# Defines the all orders view


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def allOrders(request):
    orders = Order.objects.all()

    context = {'orders': orders}
    return render(request, 'accounts/all_orders.html', context)
# Defines the all customer orders view


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['customer'])
def allCustomerOrders(request):
    customer = request.user.customer
    orders = customer.order_set.all()
    # print(orders)

    pending_list = []
    out_for_delivery_list = []
    delivered_list = []
    not_tended_list = []
    for n in orders:
        if n.status == 'Pending':
            pending_list.append(n)
        if n.status == 'Out for delivery':
            out_for_delivery_list.append(n)
        if n.status == 'Delivered':
            delivered_list.append(n)
        if n.status == 'Not tended':
            not_tended_list.append(n)

    print(pending_list)
    print(out_for_delivery_list)
    print(delivered_list)
    print(not_tended_list)

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending,
               'pending_list': pending_list, 'outfordelivery_list': out_for_delivery_list,
               'delivered_list': delivered_list, 'not_tended_list': not_tended_list, }
    return render(request, 'accounts/all_customer_orders.html', context)

# Defines the admin's customer view


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    feedbacks = Feedback.objects.all()
    customer_feedback = feedbacks.filter(customer=customer)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders,
               'order_count': order_count, 'myFilter': myFilter,
               'feedbacks': feedbacks, 'customer_feedback': customer_feedback}
    return render(request, 'accounts/customer.html', context)

# Defines the create order view


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    #OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'order_quantity', 'status'), extra=3)

    form = OrderForm(initial={'customer': customer})
    print(customer)

    #formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        #formset = OrderFormSet(request.POST, instance=customer)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}

    return render(request, 'accounts/order_form.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['customer'])
def createCustomerOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    # customer = request.user.customer

    order = customer.order_set.all()

    form = OrderCustomerForm(initial={'customer': customer})

    if request.method == 'POST':
        form = OrderCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user/')

    context = {'form': form, 'customer': customer, 'order': order}

    return render(request, 'accounts/customer_order_form.html', context)


# Defines the update order view


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

    # customer = request.user.id
    # customer = request.user.customer
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form, 'customer': customer, 'order': order}

    return render(request, 'accounts/order_form.html', context)

# Defines the delete order view


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin', 'customer'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)

# Defines the delete customer view


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('/')
    context = {'item': customer}
    return render(request, 'accounts/delete_customer.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['customer'])
def deleteFeedback(request, pk):
    feedback = Feedback.objects.get(id=pk)
    if request.method == "POST":
        feedback.delete()
        return redirect('/')
    context = {'feedback': feedback}
    return render(request, 'accounts/delete_feedback.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['customer'])
def giveFeedback(request, pk):
    customer = request.user.customer
    feedbacks = Feedback.objects.all()

    user_feedbacks = feedbacks.filter(customer=customer)

    # feedback = Feedback.objects.get(id=pk) - brings different user from the designated user
    # print(feedback)

    feedbacks_form = GiveFeedbackForm(initial={'customer': customer})

    if request.method == 'POST':
        feedbacks_form = GiveFeedbackForm(request.POST)
        if feedbacks_form.is_valid():
            feedbacks_form.save()
            return redirect('/user/')

    context = {'feedbacks_form': feedbacks_form,
               'customer': customer, 'user_feedbacks': user_feedbacks, }

    return render(request, 'accounts/give_feedback.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin', 'health'])
def healthManager(request):

    flock = Flock.objects.all()

    medicine = Medicine.objects.all()

    vaccinations = Vaccination.objects.all()

    context = {'flock': flock, 'medicine': medicine,
               'vaccinations': vaccinations}

    return render(request, 'accounts/health_manager.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin', 'brooder'])
def brooderManager(request):

    brooders = Brooder.objects.all()
    feeds = Feed.objects.all()
    feedsusage = FeedUsage.objects.all()

    context = {'brooders': brooders, 'feeds': feeds, 'feedsusage': feedsusage}

    return render(request, 'accounts/brooder_manager.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def flock(request):
    flock = Flock.objects.all()
    orders = Order.objects.all()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    # vac = Vaccination.objects.filter(id=1)
    # print(flock)

    active_flock = []
    for i in flock:

        # print(i)
        # print(i.flock_quantity)

        flock_count = i.flock_quantity
        # print(flock_count)
        active_flock.append(flock_count)

    # print(active_flock)

    number_of_active_flock = sum(active_flock)
    # print(number_of_active_flock)

    context = {'flock': flock, 'delivered': delivered,
               'pending': pending, 'number_of_active_flock': number_of_active_flock}

    return render(request, 'accounts/flock.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def brooder(request):

    brooders = Brooder.objects.all()

    context = {'brooders': brooders}

    return render(request, 'accounts/brooder.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def sales(request, pk):

    sales = Sale.objects.all()

    context = {'sales': sales}

    return render(request, 'accounts/sales.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin', 'health'])
def vaccinations(request):

    vaccinations = Vaccination.objects.all()

    context = {'vaccinations': vaccinations}

    return render(request, 'accounts/vaccinations.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin', 'health'])
def medicine(request):

    medicine = Medicine.objects.all()

    context = {'medicine': medicine}

    return render(request, 'accounts/medicine.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin', 'brooder'])
def feeds(request):

    feeds = Feed.objects.all()

    context = {'feeds': feeds}

    return render(request, 'accounts/feeds.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin', 'brooder'])
def feedsUsage(request):

    feedsusages = FeedUsage.objects.all()

    context = {'feedsusages': feedsusages}

    return render(request, 'accounts/feeds_usage.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin', 'brooder'])
def addFeedsUsage(request):

    add_feedusage_form = AddFeedUsageForm()

    if request.method == 'POST':
        # print(request.POST)
        feed_id = int(request.POST['feed'])
        feed_quantity_used = int(request.POST['feed_quantity_used'])
        # print(feed_affected)
        # print(feed_quantity_used)

        feed_affected = Feed.objects.get(id=feed_id)
        # print(feed_affected)
        if feed_quantity_used <= feed_affected.feed_quantity:
            # print('Update happens here')
            add_feedusage_form = AddFeedUsageForm(request.POST)

            updated_feed_quantity = feed_affected.feed_quantity - feed_quantity_used

            if add_feedusage_form.is_valid():
                feed_to_update = Feed.objects.get(id=feed_id)
                feed_to_update.feed_quantity = updated_feed_quantity
                feed_to_update.save()
                # print('Saved')
                add_feedusage_form.save()

                return redirect('/brooder_manager/')

        else:
            print('Not possible')

    context = {'add_feedusage_form': add_feedusage_form}

    return render(request, 'accounts/add_feedusage.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin', 'brooder', 'health'])
def calender(request):

    context = {}

    return render(request, 'accounts/calender.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin', 'health'])
def mortality(request):

    mortalities = Mortality.objects.all()

    context = {'mortalities': mortalities}

    return render(request, 'accounts/mortality.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def income(request):

    context = {}

    return render(request, 'accounts/income.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def expenses(request):

    context = {}

    return render(request, 'accounts/expenses.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def reports(request):

    context = {}

    return render(request, 'accounts/reports.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def allFeedback(request):

    feedbacks = Feedback.objects.all()

    context = {'feedbacks': feedbacks}

    return render(request, 'accounts/all_feedback.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def addFlock(request):

    add_flock_form = AddFlockForm()

    if request.method == 'POST':
        add_flock_form = AddFlockForm(request.POST)
        added_flock = int(request.POST['flock_quantity'])

        brooder = request.POST['brooder']
        flock = Flock.objects.all()
        # db_brooder = flock.filter(id=brooder)
 #       print('db brooder', db_brooder, )
        print('flock', type(flock), len(flock), '\n')
        brooder_list = []

        if len(flock):
            for n in flock:
                # print(n)
                # print(type(n))
                # print(n.id)
                # print(n.brooder_id)
                # print(n.flock_quantity)
                #print('the brooder', brooder)
                # print(type(brooder))

                if n.brooder_id == int(brooder):

                    # print(n)
                    # print(n.flock_quantity)
                    brooder_list.append(n.flock_quantity)
                # print(brooder_list)
                brooder_sum = sum(brooder_list)
                # print(brooder_sum)
                #print('quantity', n.flock_quantity)
                #print('brooder id', n.id)
                # print(type(added_flock))
                if (added_flock + brooder_sum > 100):
                    print('More than 100')
                    messages.info(
                        request, 'The flock in that brooder exceeds the capacity')

                else:
                    if add_flock_form.is_valid:
                        add_flock_form.save()
                        print('Saved')

        else:
            if added_flock > 100:
                print('Brooder cannot take more than 100')

            else:
                if add_flock_form.is_valid:
                    add_flock_form.save()

        return redirect('/flock/')

    context = {'add_flock_form': add_flock_form}

    return render(request, 'accounts/add_flock.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def addFeed(request):

    add_feed_form = AddFeedForm()

    if request.method == 'POST':
        add_feed_form = AddFeedForm(request.POST)
        if add_feed_form.is_valid:
            addExpense()
            add_feed_form.save()

            return redirect('/brooder_manager/')

    context = {'add_feed_form': add_feed_form}

    return render(request, 'accounts/add_feed.html', context)


def addExpense():
    print('Added expense')


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def addMedicine(request):
    add_medicine_form = AddMedicineForm()

    if request.method == 'POST':
        add_medicine_form = AddMedicineForm(request.POST)
        if add_medicine_form.is_valid:
            addExpense()

            try:
                add_medicine_form.save()
            except ValidationError:
                print('The date cannot be in the past!')
                return redirect('/add_medicine/')

            return redirect('/health_manager/')

    context = {'add_medicine_form': add_medicine_form}

    return render(request, 'accounts/add_medicine.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def addVaccination(request):

    add_vaccination_form = NewVaccinationForm()

    if request.method == 'POST':
        add_vaccination_form = NewVaccinationForm(request.POST)
        if add_vaccination_form.is_valid:
            add_vaccination_form.save()

            return redirect('/health_manager/')

    context = {'add_vaccination_form': add_vaccination_form}

    return render(request, 'accounts/add_vaccination.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['admin'])
def addMortality(request):
    # mortality = Mortality.objects.get()
    # flock = Flock.objects.all()
  #  print(type(mortality))
    # flock_list = []

    # for i in flock:
    #     flock_list.append(i)
    #     print(i)

   # print(type(mortality_list))
    # print(flock_list)

    # for n in mortality_list:
    # print(n)
    # print(n.mortality_count)
    #    print(n.mortality_date)
    #   print(n.flock)
    #  print(n.flock.flock_quantity)

    add_mortality_form = NewMortalityForm()

    if request.method == 'POST':
        add_mortality_form = NewMortalityForm(request.POST)
        # print(request.POST)
        flock_id = int(request.POST['flock'])
        flock_mortality_count = int(request.POST['mortality_count'])

        flock_affected = Flock.objects.get(id=flock_id)

        if flock_mortality_count <= flock_affected.flock_quantity:

            updated_flock_count = (
                flock_affected.flock_quantity - flock_mortality_count)

            if add_mortality_form.is_valid:
                flock_to_update = Flock.objects.get(id=flock_id)
                flock_to_update.flock_quantity = updated_flock_count
                flock_to_update.save()

                close_flock(flock_id)

                add_mortality_form.save()
                # print('Saved')
                # print(updated_flock_count)

        else:
            print('Not possible. Mortality exceeds flock count')

        # print(flock_affected.flock_quantity)
        # print('updated', updated_flock_count)

        # print('flock_affected', flock_affected, )
        # print('flock_id', flock_id, )
        # print('flock_mortality_count', flock_mortality_count, )
        # print('flock', type(flock), len(flock_affected), '\n')
        return redirect('/health_manager/')

    context = {'add_mortality_form': add_mortality_form}

    return render(request, 'accounts/add_mortality.html', context)


def index(request):

    context = {}

    return render(request, 'accounts/index.html', context)


def update():
    return render()
