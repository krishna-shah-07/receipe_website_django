from django.shortcuts import render, redirect

from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login/')
def recipes(request):
    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_desc = data.get('recipe_description')
        recipe_img = request.FILES.get('recipe_image')

        # print(recipe_name)
        # print(recipe_desc)
        # print(recipe_img)

        recipe.objects.create(
            recipe_name = recipe_name, 
            recipe_description = recipe_desc, 
            recipe_image = recipe_img
        )

        return redirect('/')
    
    queryset = recipe.objects.all()

    if request.GET.get('search_recipe'):
        #print(request.GET.get('search_recipe'))
        queryset = queryset.filter(recipe_name__icontains = request.GET.get('search_recipe'))

    context = {'recipes': queryset}
    return render(request, 'recipes.html', context)

@login_required(login_url='/login/')
def delete_recipe(request, id):
    queryset = recipe.objects.get(id = id)
    queryset.delete()
    return redirect('/')

@login_required(login_url='/login/')
def update_recipe(request, id):
    queryset = recipe.objects.get(id = id)
    context = {'recipe': queryset}

    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_desc = data.get('recipe_description')
        recipe_img = request.FILES.get('recipe_image')

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_desc

        if recipe_img:
            queryset.recipe_image = recipe_img

        queryset.save()
        return redirect('/')

    return render(request, 'update_recipes.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username = username).exists():
            user = authenticate(username = username, password = password)
            if user is None:
                messages.error(request, 'Invalid Password')
                return redirect('/login/')
            else:
                login(request, user)
                return redirect('/')
            
        else:
            messages.error(request, 'Username doesnot exist')
            return redirect('/login/')

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login')

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.error(request, 'Username already exists')
            return redirect('/register/')

        user = User.objects.create(
            username = username
        )

        user.set_password(password)
        user.save()

        messages.error(request, 'Account created successfully')
        return redirect('/register/')

    return render(request, 'register.html')