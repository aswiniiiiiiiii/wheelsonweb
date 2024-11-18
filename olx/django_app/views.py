from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.utils import timezone
from .form import FeedbackForm, QuestionForm, RentVehicleForm, SellVehicleForm
from .models import QA, CustomUser, District, Feedback, FuelType, GearType, OwnerType, QA_Buyer, Question, RentVehicle, SellVehicle, VehicleBrand, VehicleType, Year
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import random
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Check if the 'is_staff' checkbox is checked
        is_staff = request.POST.get('is_staff', False) == 'on'

        user = CustomUser.objects.create_user(username=username, password=password, email=email, is_staff=is_staff)

        if is_staff:
            return redirect('staff_activity')
        else:
            return redirect('buyer_activity')

    return render(request, 'registration/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_staff:
                return redirect('staff_activity')
            else:
                return redirect('buyer_activity')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})

    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def staff_activity(request):
    # Logic for staff activity goes here
    return render(request, 'staff_activity.html')

@login_required(login_url='login')
def buyer_activity(request):
    # Logic for buyer activity goes here
    return render(request, 'buyer_activity.html')

def index(request):
    return render(request, 'index.html')
def home(request):
    return render(request, 'home.html')
class SellVehicleListView(ListView):
    model = SellVehicle
    template_name = 'sellvehicle_list.html'
    context_object_name = 'sellvehicles'

class SellVehicleDetailView(DetailView):
    model = SellVehicle
    template_name = 'sellvehicle_detail.html'
    context_object_name = 'sellvehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sell_vehicle = self.get_object()

        related_vehicles = SellVehicle.objects.filter(vehicle_type=sell_vehicle.vehicle_type).exclude(id=sell_vehicle.id)

        related_vehicles = random.sample(list(related_vehicles), min(5, len(related_vehicles)))

        context['related_vehicles'] = related_vehicles
        return context
    
class SellVehicleSellerDetailView(DetailView):
    model = SellVehicle
    template_name = 'sellvehicle_seller_detail.html'
    context_object_name = 'sellvehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sell_vehicle = self.get_object()

        return context


class SellVehicleCreateView(CreateView):
    model = SellVehicle
    form_class = SellVehicleForm
    template_name = 'sellvehicle_form.html'
    success_url = 'see-my-sell-vehicles'
    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fuel_types'] = FuelType.objects.all()
        context['vehicle_types'] = VehicleType.objects.all()
        context['vehicle_brands'] = VehicleBrand.objects.all()
        context['years'] = Year.objects.all()
        context['owner_types'] = OwnerType.objects.all()
        context['gear_types'] = GearType.objects.all()
        context['districts'] = District.objects.all()
        return context
    
class SellVehicleUpdateView(UpdateView):
    model = SellVehicle
    form_class = SellVehicleForm
    template_name = 'sellvehicle_update_form.html'
    success_url = reverse_lazy('see_my_sell_vehicles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['districts'] = District.objects.all()
        context['vehicle_brands'] = VehicleBrand.objects.all()
        context['vehicle_types'] = VehicleType.objects.all()
        context['years'] = Year.objects.all()
        context['fuel_types'] = FuelType.objects.all()
        context['owner_types'] = OwnerType.objects.all()
        context['gear_types'] = GearType.objects.all()
        return context

class SellVehicleDeleteView(DeleteView):
    model = SellVehicle
    template_name = 'sellvehicle_confirm_delete.html'
    success_url = reverse_lazy('see_my_sell_vehicles')
class RentVehicleListView(ListView):
    model = RentVehicle
    template_name = 'rentvehicle_list.html'
    context_object_name = 'rentvehicles'


class RentVehicleSellerDetailView(DetailView):
    model = RentVehicle
    template_name = 'rentvehicle_seller_detail.html'
    context_object_name = 'rentvehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rent_vehicle = self.get_object()

        return context    
    
class RentVehicleDetailView(DetailView):
    model = RentVehicle  
    template_name = 'rentvehicle_detail.html'
    context_object_name = 'rentvehicle'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rent_vehicle = self.get_object()

        related_vehicles = RentVehicle.objects.filter(vehicle_type=rent_vehicle.vehicle_type).exclude(id=rent_vehicle.id)
        related_vehicles = random.sample(list(related_vehicles), min(5, len(related_vehicles)))

        context['related_vehicles'] = related_vehicles
        return context

class RentVehicleCreateView(CreateView):
    model = RentVehicle
    form_class = RentVehicleForm
    template_name = 'rentvehicle_form.html'
    success_url = reverse_lazy('see_my_rent_vehicles') 

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fuel_types'] = FuelType.objects.all()
        context['vehicle_types'] = VehicleType.objects.all()
        context['vehicle_brands'] = VehicleBrand.objects.all()
        context['years'] = Year.objects.all()
        context['gear_types'] = GearType.objects.all()
        context['districts'] = District.objects.all()
        return context
  
    
class RentVehicleUpdateView(UpdateView):
    model = RentVehicle
    form_class = RentVehicleForm
    template_name = 'rentvehicle_update_form.html'
    success_url = reverse_lazy('see_my_rent_vehicles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['districts'] = District.objects.all()
        context['vehicle_brands'] = VehicleBrand.objects.all()
        context['vehicle_types'] = VehicleType.objects.all()
        context['years'] = Year.objects.all()
        context['fuel_types'] = FuelType.objects.all()
        context['gear_types'] = GearType.objects.all()
        return context

class RentVehicleDeleteView(DeleteView):
    model = RentVehicle
    template_name = 'rentvehicle_confirm_delete.html'
    success_url = reverse_lazy('see_my_rent_vehicles')
def see_my_sell_vehicles(request):
    sell_vehicles = SellVehicle.objects.filter(seller=request.user)

    context = {
        'sell_vehicles': sell_vehicles
    }

    return render(request, 'see_my_sell_vehicles.html', context)

def see_my_rent_vehicles(request):
    rent_vehicles = RentVehicle.objects.filter(owner=request.user)

    context = {
        'rent_vehicles': rent_vehicles
    }

    return render(request, 'see_my_rent_vehicles.html', context)



def faq_view(request):
    faq_list = QA.objects.all()
    return render(request, 'faq.html', {'faq_list': faq_list})

def buyer_faq_view(request):
    faq_list = QA_Buyer.objects.all()
    return render(request, 'buyer_faq.html', {'faq_list': faq_list})

def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            messages.success(request, 'Your question has been submitted successfully!') 
            return redirect('buyer_activity')
    else:
        form = QuestionForm()
    return render(request, 'create_question.html', {'form': form})

def create_question_seller(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            messages.success(request, 'Your question has been submitted successfully!')
            return redirect('staff_activity')  
    else:
        form = QuestionForm()
    return render(request, 'create_question_seller.html', {'form': form})


def create_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            
            # Check if the rating exceeds the maximum value of 5
            if feedback.rating > 5:
                messages.error(request, "Rating cannot exceed 5.")
                return redirect('create_feedback')  # Redirect back to the feedback form
            
            feedback.save()

            # Check if the user is a seller or a buyer
            if request.user.is_staff:
                return redirect('staff_feedback')  # Redirect to staff feedback list
            else:
                return redirect('buyer_feedback')  # Redirect to buyer feedback list
    else:
        form = FeedbackForm()

    return render(request, 'create_feedback.html', {'form': form})
def create_seller_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            
            if feedback.rating > 5:
                messages.error(request, "Rating cannot exceed 5.")
                return redirect('create_feedback') 
            
            feedback.save()

            if request.user.is_staff:
                return redirect('staff_feedback')  
            else:
                return redirect('buyer_feedback')  
    else:
        form = FeedbackForm()

    return render(request, 'create_feedback_seller.html', {'form': form})


def list_buyer_feedback(request):
    # Get all feedback for buyers (users with is_staff=False)
    buyer_feedback = Feedback.objects.filter(user__is_staff=False)
    return render(request, 'list_buyer_feedback.html', {'buyer_feedback': buyer_feedback})

def list_staff_feedback(request):
    # Get all feedback for staff (users with is_staff=True)
    staff_feedback = Feedback.objects.filter(user__is_staff=True)
    return render(request, 'list_staff_feedback.html', {'staff_feedback': staff_feedback})

def vehicles_by_year_range(request, start_year, end_year):
    if start_year == 0 and end_year == 2:
        sell_vehicles = SellVehicle.objects.filter(year__year__gte=timezone.now().year - 2)
        rent_vehicles = RentVehicle.objects.filter(year__year__gte=timezone.now().year - 2)
    elif start_year == 3 and end_year == 6:
        sell_vehicles = SellVehicle.objects.filter(year__year__gte=timezone.now().year - 6, year__year__lte=timezone.now().year - 3)
        rent_vehicles = RentVehicle.objects.filter(year__year__gte=timezone.now().year - 6, year__year__lte=timezone.now().year - 3)
    elif start_year == 6 and end_year == 10:
        sell_vehicles = SellVehicle.objects.filter(year__year__gte=timezone.now().year - 10, year__year__lte=timezone.now().year - 7)
        rent_vehicles = RentVehicle.objects.filter(year__year__gte=timezone.now().year - 10, year__year__lte=timezone.now().year - 7)
    else:  # Above 10 year
        sell_vehicles = SellVehicle.objects.filter(year__year__lte=timezone.now().year - 11)
        rent_vehicles = RentVehicle.objects.filter(year__year__lte=timezone.now().year - 11)

    return render(request, 'vehicles_by_year_range.html', {
        'sell_vehicles': sell_vehicles,
        'rent_vehicles': rent_vehicles,
    })

def vehicles_by_vehicle_type(request, vehicle_type):
    sell_vehicles = SellVehicle.objects.filter(vehicle_type__type_name=vehicle_type)
    rent_vehicles = RentVehicle.objects.filter(vehicle_type__type_name=vehicle_type)
    return render(request, 'vehicles_by_vehicle_type.html', {'sell_vehicles': sell_vehicles, 'rent_vehicles': rent_vehicles})

def vehicles_by_price_range(request, price_range):
    if price_range == 'below-50k':
        sell_vehicles = SellVehicle.objects.filter(price__lte=50000)
    elif price_range == '50k-to-2lakh':
        sell_vehicles = SellVehicle.objects.filter(price__gt=50000, price__lte=200000)
    elif price_range == '2lakh-to-5lakh':
        sell_vehicles = SellVehicle.objects.filter(price__gt=200000, price__lte=500000)
    elif price_range == 'above-5lakh':
        sell_vehicles = SellVehicle.objects.filter(price__gt=500000)
    else:
        sell_vehicles = SellVehicle.objects.none()

    return render(request, 'vehicles_by_price_range.html', {'sell_vehicles': sell_vehicles})


def vehicles_by_km_driven(request, km_range):
    if km_range == 'below10000':
        sell_vehicles = SellVehicle.objects.filter(km_driven__lt=10000)
        rent_vehicles = RentVehicle.objects.filter(km_driven__lt=10000)
    elif km_range == '10000to15000':
        sell_vehicles = SellVehicle.objects.filter(km_driven__range=[10000, 15000])
        rent_vehicles = RentVehicle.objects.filter(km_driven__range=[10000, 15000])
    elif km_range == '15000to25000':
        sell_vehicles = SellVehicle.objects.filter(km_driven__range=[15000, 25000])
        rent_vehicles = RentVehicle.objects.filter(km_driven__range=[15000, 25000])
    elif km_range == 'above25000':
        sell_vehicles = SellVehicle.objects.filter(km_driven__gt=25000)
        rent_vehicles = RentVehicle.objects.filter(km_driven__gt=25000)
    else:
        sell_vehicles = SellVehicle.objects.none()
        rent_vehicles = RentVehicle.objects.none()

    return render(request, 'vehicles_by_km_driven.html', {'sell_vehicles': sell_vehicles, 'rent_vehicles': rent_vehicles})


def vehicles_by_fuel_type(request, fuel_type):
    sell_vehicles = SellVehicle.objects.filter(fuel_type__fuel=fuel_type)
    rent_vehicles = RentVehicle.objects.filter(fuel_type__fuel=fuel_type)
    return render(request, 'vehicles_by_fuel_type.html', {'sell_vehicles': sell_vehicles, 'rent_vehicles': rent_vehicles})
def search_vehicles(request):
    query = request.GET.get('q')
    brand_query = request.GET.get('brand')
    vehicle_type_query = request.GET.get('vehicle_type')
    year_query = request.GET.get('year')

    sell_vehicles = SellVehicle.objects.all()
    rent_vehicles = RentVehicle.objects.all()

    if query:
        sell_vehicles = sell_vehicles.filter(vehicle_name__icontains=query)
        rent_vehicles = rent_vehicles.filter(vehicle_name__icontains=query)

    if brand_query:
        sell_vehicles = sell_vehicles.filter(brand__name__icontains=brand_query)
        rent_vehicles = rent_vehicles.filter(brand__name__icontains=brand_query)

    if vehicle_type_query:
        sell_vehicles = sell_vehicles.filter(vehicle_type__name__icontains=vehicle_type_query.capitalize())
        rent_vehicles = rent_vehicles.filter(vehicle_type__name__icontains=vehicle_type_query.capitalize())

    if year_query:
        sell_vehicles = sell_vehicles.filter(year__year__icontains=year_query)
        rent_vehicles = rent_vehicles.filter(year__year__icontains=year_query)

    return render(request, 'search_results.html', {'sell_vehicles': sell_vehicles, 'rent_vehicles': rent_vehicles, 'query': query})

def vehicles_by_district(request, district_name):
    sell_vehicles = SellVehicle.objects.filter(district__district=district_name)
    rent_vehicles = RentVehicle.objects.filter(district__district=district_name)
    return render(request, 'vehicles_by_district.html', {'sell_vehicles': sell_vehicles, 'rent_vehicles': rent_vehicles})

def vehicles_by_owner_type(request, owner_type):
    sell_vehicles = SellVehicle.objects.filter(type_of_owner__owner_type=owner_type)
    
    return render(request, 'vehicles_by_owner_type.html', {'sell_vehicles': sell_vehicles})

def vehicles_by_gear_type(request, gear_type):
    sell_vehicles = SellVehicle.objects.filter(type_of_gear__gear_type=gear_type)
    rent_vehicles = RentVehicle.objects.filter(type_of_gear__gear_type=gear_type)
    return render(request, 'vehicles_by_gear_type.html', {'sell_vehicles': sell_vehicles, 'rent_vehicles': rent_vehicles})

def update_profile(request):
    user = request.user
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the provided current password matches the user's actual password
        if not check_password(current_password, user.password):
            messages.error(request, 'Incorrect current password.')
            return redirect('update_profile')

        # Check if the new password matches the confirmed password
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('update_profile')

        # Update user fields
        user.username = username
        user.email = email

        if new_password:
            user.set_password(new_password)
            # Important: Update session authentication hash to avoid logout
            update_session_auth_hash(request, user)

        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')  # Redirect to user's profile page
    else:
        # Populate initial form values with user's current data
        initial_data = {
            'username': user.username,
            'email': user.email
        }

    return render(request, 'update_profile.html', {'initial_data': initial_data})
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            messages.success(request, 'Your question has been submitted successfully!')
            
            return redirect('buyer_activity')
    else:
        form = QuestionForm()
    return render(request, 'create_question.html', {'form': form})

def create_question_seller(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            messages.success(request, 'Your question has been submitted successfully!')
            return redirect('staff_activity')  
    else:
        form = QuestionForm()
    return render(request, 'create_question_seller.html', {'form': form})



def create_seller_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            
            # Check if the rating exceeds the maximum value of 5
            if feedback.rating > 5:
                messages.error(request, "Rating cannot exceed 5.")
                return redirect('create_feedback')  # Redirect back to the feedback form
            
            feedback.save()

            # Check if the user is a seller or a buyer
            if request.user.is_staff:
                return redirect('staff_feedback')  # Redirect to staff feedback list
            else:
                return redirect('buyer_feedback')  # Redirect to buyer feedback list
    else:
        form = FeedbackForm()

    return render(request, 'create_feedback_seller.html', {'form': form})

def update_buyer(request):
    user = request.user
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the provided current password matches the user's actual password
        if not check_password(current_password, user.password):
            messages.error(request, 'Incorrect current password.')
            return redirect('update_buyer')

        # Check if the new password matches the confirmed password
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('update_buyer')

        # Update user fields
        user.username = username
        user.email = email

        if new_password:
            user.set_password(new_password)
            # Important: Update session authentication hash to avoid logout
            update_session_auth_hash(request, user)

        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('buyer_activity')  # Redirect to user's profile page
    else:
        # Populate initial form values with user's current data
        initial_data = {
            'username': user.username,
            'email': user.email
        }

    return render(request, 'update_buyer.html', {'initial_data': initial_data})

def update_profile(request):
    user = request.user
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the provided current password matches the user's actual password
        if not check_password(current_password, user.password):
            messages.error(request, 'Incorrect current password.')
            return redirect('update_profile')

        # Check if the new password matches the confirmed password
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('update_profile')

        # Update user fields
        user.username = username
        user.email = email

        if new_password:
            user.set_password(new_password)
            # Important: Update session authentication hash to avoid logout
            update_session_auth_hash(request, user)

        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('staff_activity')  # Redirect to user's profile page
    else:
        # Populate initial form values with user's current data
        initial_data = {
            'username': user.username,
            'email': user.email
        }

    return render(request, 'update_profile.html', {'initial_data': initial_data})

def list_emi_available_vehicles(request):
    emi_available_vehicles = SellVehicle.objects.filter(emi_available=True)
    
    return render(request, 'emi_available_vehicles.html', {'emi_available_vehicles': emi_available_vehicles})