from django.urls import path

from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('index', views.index, name="index"),

    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),

    path('account/', views.accountSettings, name="account"),

    path('products/', views.products, name="products"),

    path('all_customers/', views.allCustomers, name="all_customers"),
    path('all_orders/', views.allOrders, name="all_orders"),
    path('all_customer_orders/', views.allCustomerOrders,
         name="all_customer_orders"),
    path('all_feedback/', views.allFeedback,
         name="all_feedback"),


    path('customer/<str:pk_test>/', views.customer, name="customer"),

    path('give_feedback/<str:pk>/',
         views.giveFeedback, name="give_feedback"),
    path('delete_feedback/<str:pk>/',
         views.deleteFeedback, name="delete_feedback"),

    path('vaccinations/', views.vaccinations, name="vaccinations"),

    path('calender/', views.calender, name="calender"),

    path('feeds/', views.feeds, name="feeds"),
    path('feeds_usage/', views.feedsUsage, name="feeds_usage"),
    path('medicine/', views.medicine, name="medicine"),

    path('health_manager/', views.healthManager, name="health_manager"),
    path('brooder_manager/', views.brooderManager, name="brooder_manager"),

    path('flock/', views.flock, name="flock"),
    path('brooder/', views.brooder, name="brooder"),

    path('sales/<str:pk>/', views.sales, name="sales"),

    path('mortality/', views.mortality, name="mortality"),

    path('income/', views.income, name="income"),
    path('expenses/', views.expenses, name="expenses"),

    path('reports/', views.reports, name="reports"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('add_flock/', views.addFlock, name="add_flock"),
    path('add_medicine/', views.addMedicine, name="add_medicine"),
    path('add_vaccination/', views.addVaccination, name="add_vaccination"),
    path('add_mortality/', views.addMortality, name="add_mortality"),
    path('add_feed/', views.addFeed, name="add_feed"),
    path('add_feedusage/', views.addFeedsUsage, name="add_feed_usage"),

    path('create_customer_order/<str:pk>/',
         views.createCustomerOrder, name="create_customer_order"),

    path('delete_customer/<str:pk>/',
         views.delete_customer, name="delete_customer"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<iudb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),
]
