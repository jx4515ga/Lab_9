from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages




# Create your views here.
@login_required
def place_list(request):

    if request.method == 'POST':
        # Create a new place

        form = NewPlaceForm(request.POST) # Creating a form from data  in the request
        place = form.save(commit=False) # Creating a model object from form 
        place.user = request.user
        if form.is_valid(): # Validation against the DB constraits 
            place.save()  # save places entered to DB
            return redirect('place_list') # Reloads home page


    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # used to create html
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_from': new_place_form})

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        #place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else: 
            return HttpResponseForbidden()
    return redirect('place_list')

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    #return render(request, 'travel_wishlist/place_detail.html', {'place':place})

    if place.user != request.user:
        return HttpResponseForbidden() 





    if request.method == "POST":
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip Information updated!')
        else:
            message.error(request, form.errors)


        return redirect('place_details', place_pk=place_pk)

    else:
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, "review_form": review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})



@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden() 


