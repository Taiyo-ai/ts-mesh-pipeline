from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="rajesh-PPP_Philippines")
location = geolocator.geocode("175 5th Avenue NYC")
print(location.address)
print()
print((location.latitude, location.longitude))
print()
print(location.raw)
