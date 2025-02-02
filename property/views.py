from django.shortcuts import render, get_object_or_404, redirect
import random
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from property.forms import HouseForm

# Create your views here.


def index(request):
    houses = list(House.objects.all())  # Get all houses as a list
    random.shuffle(houses)  # Shuffle the list randomly
    random_houses = houses[:5]  # Select 5 random houses (adjust as needed)

    return render(request, 'index.html', {'house': random_houses})

@login_required
def create_house(request):
    if request.method == 'POST':
        print(request.FILES)
        form = HouseForm(request.POST, request.FILES, user=request.user)
        # print( form )
        if form.is_valid():
            house = form.save(commit=False)
            house.owner = request.user  # This ensures the owner is set if not passed in the form
            house.save()
            messages.success(request, 'House created successfully!')
            return redirect('profile')
    else:
        form = HouseForm(user=request.user)

    return render(request, 'accounts/profile.html', {'form': form})


def view_house(request, id):
    house = get_object_or_404(House, id=id)
    return render(request, 'property/property-single.html', {'house': house})


@login_required(login_url='login')  # Replace 'login' with your login URL name
def apply(request, house_id):
    # Get the house the user is applying for
    house = get_object_or_404(House, id=house_id)

    # Get the current logged-in user (no need to pass the user_id)
    user = request.user

    # Check if the user has already applied for this house
    if AppliedHouses.objects.filter(house=house, user=user).exists():
        messages.warning(request, "You have already applied for this house.")
        return redirect('view-house', id=house_id)  # Redirect to the house detail page

    # If not applied, create a new application
    AppliedHouses.objects.create(house=house, user=user)

    # Send a success message
    messages.success(request, "You have successfully applied for this house!")
    return redirect('view-house', id=house_id)  # Redirect to the house detail page

def house_list(request):
    houses = House.objects.all()
    return render(request, 'house_list.html', {'houses': houses})


def house_create(request):
    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "House listing added successfully!")
            return redirect('house_list')
    else:
        form = HouseForm()
    
    return render(request, 'house_form.html', {'form': form})

def house_update(request, pk):
    house = get_object_or_404(House, pk=pk)
    
    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES, instance=house)
        if form.is_valid():
            form.save()
            messages.success(request, "House listing updated successfully!")
            return redirect('house_list')
    else:
        form = HouseForm(instance=house)
    
    return render(request, 'house_form.html', {'form': form})

def house_delete(request, pk):
    house = get_object_or_404(House, pk=pk)
    
    if request.method == 'POST':
        house.delete()
        messages.success(request,"House listing deleted successfully!")
        return redirect('house_list')
    
    return render(request, 'house_confirm_delete.html', {'house': house})

# def search(request):
#     houses = list(House.objects.all())  # Get all houses as a list
#     random.shuffle(houses)  # Shuffle the list randomly
#     selected_houses = houses[:3]  # Select the first 3 houses from the shuffled list
#     return render(request, 'customer/search.html',  {'houses': selected_houses})
