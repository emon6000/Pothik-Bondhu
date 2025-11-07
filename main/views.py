from django.shortcuts import render
from django.http import JsonResponse 
from django.conf import settings
from .models import District
import json
import requests
from django.views.decorators.csrf import csrf_exempt

def home(request):
    """
    Renders the homepage and passes the 64-district list
    to the frontend for our autocomplete.
    """
    districts = District.objects.all().order_by('name')
    district_names = [district.name for district in districts]
    context = {
        'district_names_json': json.dumps(district_names)
    }
    return render(request, 'home.html', context)

@csrf_exempt
def api_plan_journey(request):
    
    data = json.loads(request.body)
    start_location_name = data.get('start')
    end_location_name = data.get('end')
    
    print(f"API CALLED: Start is {start_location_name}, End is {end_location_name}")

    def normalize_district_name(name):
        if not name: return None
        name = (
            name.replace(" District", "").replace(" Zila", "")
                .replace(" Division", "").replace(" Metropolitan", "")
                .replace(" Sadar Upazila", "").replace(" Adarsha Sadar Upazila", "")
        )
        name_lower = name.lower()
        if name_lower == "comilla": return "Cumilla"
        if name_lower == "barisal": return "Barishal"
        if name_lower == "nawabganj": return "Chapai Nawabganj"
        if name_lower == "jessore": return "Jashore"
        return name

    def get_coords_from_name(location_name):
        headers = { 'User-Agent': 'PothikBondhu/1.0 (pothik.bondhu.app; abdullahemon.me@gmail.com)' }
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': location_name,
            'format': 'json', 'limit': 1, 'countrycodes': 'bd',
            'addressdetails': 1, 'accept-language': 'en'
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            result = response.json()
            if result:
                lat = result[0]['lat']
                lon = result[0]['lon']
                print(f"Coordinates for {location_name}: {lat}, {lon}")
                return f"{lon},{lat}", lat, lon
            else:
                return None, None, None
        except Exception as e:
            print(f"Error in get_coords_from_name: {e}")
            return None, None, None

    def get_district_from_coords(lon, lat):
        headers = { 'User-Agent': 'PothikBondhu/1.0 (pothik.bondhu.app; abdullahemon.me@gmail.com)' }
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': lat, 'lon': lon, 'format': 'json',
            'addressdetails': 1, 'accept-language': 'en'
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            address = data.get('address', {})
            district_name_raw = address.get('state_district', address.get('county', address.get('state')))
            district_name_normalized = normalize_district_name(district_name_raw) # Use our cleaner
            print(f"Coords {lon},{lat} are in District: {district_name_normalized} (Raw: {district_name_raw})")
            return district_name_normalized
        except Exception as e:
            print(f"Reverse geocode error: {e}")
            return None

    def get_route(start_coords, end_coords):
        coords_string = f"{start_coords};{end_coords}"
        url = f"http://router.project-osrm.org/route/v1/driving/{coords_string}"
        params = { 'overview': 'full', 'geometries': 'geojson', 'steps': 'true' }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data and data.get('routes'):
                print("Route found successfully!")
                return data['routes'][0]
            else: return None
        except Exception as e:
            print(f"Error getting route from OSRM: {e}"); return None

    def get_weather(lat, lon):
        print(f"Getting weather for {lat}, {lon}")
        api_key = settings.WEATHER_API_KEY 
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = { 'lat': lat, 'lon': lon, 'appid': api_key, 'units': 'metric' }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return {
                "temp": data['main']['temp'],
                "feels_like": data['main']['feels_like'],
                "description": data['weather'][0]['description'].capitalize()
            }
        except Exception as e:
            print(f"Weather API error: {e}"); return None

    
    start_coords, start_lat, start_lon = get_coords_from_name(start_location_name)
    end_coords, end_lat, end_lon = get_coords_from_name(end_location_name)

    if not start_coords or not end_coords:
        return JsonResponse({'error': 'Could not find coordinates. Please select a valid district from the list.'}, status=400)

    route_data = get_route(start_coords, end_coords)

    if not route_data:
        return JsonResponse({'error': 'A route could not be found between these locations.'}, status=400)

    all_districts = []
    
    start_district = get_district_from_coords(start_lon, start_lat)
    if start_district: all_districts.append(start_district)
    
    coordinates = route_data['geometry']['coordinates']
    if len(coordinates) > 4:
        sample_indices = [
            int(len(coordinates) * 0.25),
            int(len(coordinates) * 0.50),
            int(len(coordinates) * 0.75)
        ]
        for index in sample_indices:
            lon, lat = coordinates[index]
            district_name = get_district_from_coords(lon, lat)
            if district_name and district_name not in all_districts:
                all_districts.append(district_name)

    end_district = get_district_from_coords(end_lon, end_lat)
    if end_district and end_district not in all_districts:
        all_districts.append(end_district)
        
    print(f"Final normalized district list: {all_districts}")
    
    journey_steps = []
    
    for district_name in all_districts:
        step_data = {"district": district_name}
        
        try:
            district_db = District.objects.get(name=district_name)
            step_data['top_sights'] = district_db.top_sights
            step_data['famous_food'] = district_db.famous_food
            print(f"Found '{district_name}' in our database.")
        except District.DoesNotExist:
            print(f"District '{district_name}' not in our database.")
            step_data['top_sights'] = "N/A"
            step_data['famous_food'] = "N/A"
        
        print(f"Getting coords for {district_name} to fetch weather...")
        _, lat, lon = get_coords_from_name(district_name)
        if lat and lon:
            step_data['weather'] = get_weather(lat, lon)
        else:
            step_data['weather'] = None
        
        journey_steps.append(step_data)

    response_data = {
        "message": "Full journey plan successful!",
        "route_geometry": route_data.get('geometry'),
        "route_distance": route_data.get('distance'),
        "route_duration": route_data.get('duration'),
        "journey_steps": journey_steps
    }

    return JsonResponse(response_data)