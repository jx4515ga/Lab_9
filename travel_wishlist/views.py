from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.
def place_list(request):

    if request.method == 'POST':
        # Create a new place

        form = NewPlaceForm(request.POST) # Creating a form from data  in the request
        place = form.save() # Creating a model object from form 
        if form.is_valid(): # Validation against the DB constraits 
            place.save()  # save places entered to DB
            return redirect('place_list') # Reloads home page


    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # used to create html
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_from': new_place_form})


def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


def place_was_visited(request, place_pk):
    if request.method == 'POST':
        #place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()
    return redirect('place_list')



