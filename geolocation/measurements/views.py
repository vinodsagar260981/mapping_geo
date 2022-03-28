from django.shortcuts import render, get_object_or_404
from .models import Measurements
from .forms import MeasurementsModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo, get_center_coordinates, get_zoom
import folium

# Create your views here.
def calculate_distance(request):
    distance=None
    destination =None
    
    data_obj = Measurements.objects.get(id=1)
    form = MeasurementsModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurements')
    
    ip="0.0.0.0.0" #use your IP for ur location
    country, city, lat, lon = get_geo(ip)
    # print("location country", country)
    # print("location city", city)
    # print("location lat, lon", lat, lon)
    
    location = geolocator.geocode(city)
    # print("#", location)
    
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)
    
    m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=8)
    
    folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                  icon=folium.Icon(color='purple')).add_to(m)
    
    if form.is_valid():
        instance = form.save(commit=False)
        destination_one = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_one)
        # print(destination)
        dest_lati = destination.latitude
        dest_long = destination.longitude
        
        pointB = (dest_lati, dest_long)
        
        distance = round(geodesic(pointA, pointB).km, 2)
        
        m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, dest_lati, dest_long), zoom_start=get_zoom(distance))
    
        folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                  icon=folium.Icon(color='purple')).add_to(m)
        
        folium.Marker([dest_lati, dest_long], tooltip='click here for more', popup=destination,
                  icon=folium.Icon(color='red', icon="cloud")).add_to(m)
        
        #draw the line 
        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
        m.add_child(line)
        
        instance.location = location
        instance.distance = distance
        instance.save()
        
    m = m._repr_html_()
        
        
    context = {
        'distance': distance,
        'destination':destination,
        'form': form,
        'map': m
    }
    
    return render(request, 'measurements/distance.html', context)
    