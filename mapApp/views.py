from django.http import HttpResponse
from django.shortcuts import render
import folium
import geocoder 

from .models import Search
from .forms import SearchForm

# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data:
            address = form.cleaned_data['address']
            form.save()
    else:
            form = SearchForm()
            address = Search.objects.all().first()
            
    location = geocoder.osm(address)
    
    #lat = location['latitude']
    lat = location.lat
    lng = location.lng
    country = location.country
    
    # Create Map Object
    m = folium.Map(location=[6.5244, 3.3792], zoom_start=2)
    
    # In case of an error 
    if lat == None or lng == None:
        Search.objects.all().last().delete()
        return HttpResponse('Please enter a valid address')
    
    folium.Marker([lat, lng], 
                tooltip='Click for more',
                popup=country).add_to(m)
        
    # Get HTML Representation of map object
    map = m._repr_html_()
    context = {'map': map, 'form': form }
    return render(request, 'mapApp/main.html', context)