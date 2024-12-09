from django.shortcuts import render, redirect

from .models import *

# Create your views here.

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

def delete_recipe(request, id):
    queryset = recipe.objects.get(id = id)
    queryset.delete()
    return redirect('/')

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
 