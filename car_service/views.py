from django.conf import settings
from .models import Car, CarModel, Service, OrderRow, Order
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin


def search(request):
    query = request.GET.get("query")
    query_filter = (
            Q(client__icontains=query)
            | Q(plate_number__icontains=query)
            | Q(VIN_code__icontains=query)
            | Q(car_model__model__icontains=query)
    )
    search_results = Car.objects.filter(query_filter)
    return render(
        request, "search.html", {"cars": search_results, "query": query}
    )


class OrdersListView(generic.ListView):
    model = Order
    template_name = 'orders.html'
    paginate_by = 2
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.all()


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'


def index(request):
    num_cars = Car.objects.all()
    num_cars_count = num_cars.count()
    num_car_models = CarModel.objects.all()
    num_car_models_count = num_car_models.count()
    num_services = Service.objects.all()
    num_service_count = num_services.count()
    num_order_rows = OrderRow.objects.all()
    num_order_rows_count = num_order_rows.count()
    num_orders = Order.objects.all()
    num_orders_count = num_orders.count()

    num_registered_status = Order.objects.filter(status__exact='r').count()
    num_awaiting_status = Order.objects.filter(status__exact='a').count()
    num_repairing_status = Order.objects.filter(status__exact='br').count()
    num_fixed_status = Order.objects.filter(status__exact='f').count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_cars_count': num_cars_count,
        'num_car_models_count': num_car_models_count,
        'num_service_count': num_service_count,
        'num_order_rows_count': num_order_rows_count,
        'num_orders_count': num_orders_count,
        'num_registered_status': num_registered_status,
        'num_awaiting_status': num_awaiting_status,
        'num_repairing_status': num_repairing_status,
        'num_fixed_status': num_fixed_status,
        'num_visits': num_visits,
        'debug': settings.STATIC_ROOT,
    }

    response = render(request, 'index.html', context=context)
    return response


def car_models(request):
    paginator = Paginator(CarModel.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_car_models = paginator.get_page(page_number)
    # car_models = CarModel.objects.all()
    context = {
        'car_models': paged_car_models
    }

    return render(request, 'carmodels.html', context=context)


def car_model(request, car_model_id):
    single_car_model = get_object_or_404(CarModel, pk=car_model_id)
    return render(request, 'carmodel.html', {'car_model': single_car_model})


def registered_cars(request):
    registered_cars = Car.objects.all()
    print(registered_cars)
    context = {
        'registered_cars': registered_cars,
    }
    return render(request, 'registeredcars.html', context=context)


def registered_car(request, registered_car_id):
    single_car = get_object_or_404(Car, pk=registered_car_id)
    return render(request, 'registeredcar.html', {'registered_car': single_car})


@csrf_protect
def register(request):
    if request.method == "POST":
        # get fields from registration form
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        # check if passwords match
        if password == password2:
            # check if username is taken
            if User.objects.filter(username=username).exists():
                messages.error(request, f"Username {username} exists!")
                return redirect("register")
            else:
                # check if email exists
                if User.objects.filter(email=email).exists():
                    messages.error(
                        request, f"User with {email} already exists!"
                    )
                    return redirect("register")
                else:
                    # if everything is correct, create new user
                    User.objects.create_user(
                        username=username, email=email, password=password
                    )
        else:
            messages.error(request, "Passwords don't match!")
            return redirect("register")
    return render(request, "register.html")


class ServiceOrdersByUserListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "orders.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            Order.objects.filter(car_owner=self.request.user).done().order_by_due_back()
        )
