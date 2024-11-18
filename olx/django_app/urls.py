from django.urls import path
from .views import RentVehicleCreateView, RentVehicleDeleteView,  RentVehicleDetailView, RentVehicleListView, RentVehicleSellerDetailView, RentVehicleUpdateView, SellVehicleSellerDetailView, SellVehicleCreateView, SellVehicleDeleteView, SellVehicleDetailView, SellVehicleListView, SellVehicleUpdateView, buyer_faq_view, create_feedback, create_question, create_question_seller, faq_view, home, index, list_emi_available_vehicles, register, search_vehicles, see_my_rent_vehicles, see_my_sell_vehicles, update_buyer, update_profile, user_login, staff_activity, buyer_activity, user_logout, create_seller_feedback
from . import views
urlpatterns = [
    
    # for both owner and buyer
    path('', index, name='index'),
    path('home', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('create_question/', create_question, name='create_question'),
    path('update-profile/', update_profile, name='update_profile'),
    path('update-buyer/', update_buyer, name='update_buyer'),
    
    
    # for buyers
    path('buyer_activity/', buyer_activity, name='buyer_activity'),
    path('sellvehicles/', SellVehicleListView.as_view(), name='sellvehicle_list'),
    path('sellvehicles/<int:pk>/', SellVehicleDetailView.as_view(), name='sellvehicle_detail'), 
    path('rentvehicles/', RentVehicleListView.as_view(), name='rentvehicle_list'),
    path('rentvehicles/<int:pk>/', RentVehicleDetailView.as_view(), name='rentvehicle_detail'),
    path('create_feedback/', create_feedback, name='create_feedback'),
    path('buyer-feedback/', views.list_buyer_feedback, name='buyer_feedback'),
    path('search/', search_vehicles, name='search_vehicles'),
    path('faq_buyer/', buyer_faq_view, name='buyer_faq'),
    path('vehicles/<int:start_year>/<int:end_year>/', views.vehicles_by_year_range, name='vehicles_by_year_range'),
    path('vehicles/by-vehicle-type/<str:vehicle_type>/', views.vehicles_by_vehicle_type, name='vehicles_by_vehicle_type'),
    path('vehicles/by-price/<str:price_range>/', views.vehicles_by_price_range, name='vehicles_by_price_range'),   
    path('vehicles/by-km-driven/<str:km_range>/', views.vehicles_by_km_driven, name='vehicles_by_km_driven'),
    path('vehicles/by-fuel/<str:fuel_type>/', views.vehicles_by_fuel_type, name='vehicles_by_fuel_type'),
    path('vehicles-by-owner-type/<owner_type>/', views.vehicles_by_owner_type, name='vehicles_by_owner'),
    path('vehicles/district/<str:district_name>/', views.vehicles_by_district, name='vehicles_by_district'),
    path('vehicles-by-gear-type/<gear_type>/', views.vehicles_by_gear_type, name='vehicles_by_gear_type'),
    path('emi-available-vehicles/', list_emi_available_vehicles, name='emi_available_vehicles'),
    
    # for owners
    path('staff_activity/', staff_activity, name='staff_activity'),
    path('sellvehicle_create', SellVehicleCreateView.as_view(), name='sellvehicle_create'),
    path('sellvehicles/<int:pk>/update/', SellVehicleUpdateView.as_view(), name='sellvehicle_update'),
    path('sellvehicles/<int:pk>/delete/', SellVehicleDeleteView.as_view(), name='sellvehicle_delete'),
    path('sellvehicles/seller/<int:pk>/', SellVehicleSellerDetailView.as_view(), name='sellvehicle_seller_detail'),
    path('rentvehicles/seller/<int:pk>/', RentVehicleSellerDetailView.as_view(), name='rentvehicle_seller_detail'),
    path('rentvehicles/create/', RentVehicleCreateView.as_view(), name='rentvehicle_create'),
    path('rentvehicles/<int:pk>/update/', RentVehicleUpdateView.as_view(), name='rentvehicle_update'),
    path('rentvehicles/<int:pk>/delete/', RentVehicleDeleteView.as_view(), name='rentvehicle_delete'),
    path('see-my-sell-vehicles/', see_my_sell_vehicles, name='see_my_sell_vehicles'),
    path('see-my-rent-vehicles/', see_my_rent_vehicles, name='see_my_rent_vehicles'),
    path('faq/', faq_view, name='faq'),
   path('staff-feedback/', views.list_staff_feedback, name='staff_feedback'),
    path('create_seller_feedback/', create_seller_feedback, name='create_seller_feedback'),
    path('create_seller_question/', create_question_seller, name='create_question_seller'),
    path('create_question/', create_question, name='create_question'),
]