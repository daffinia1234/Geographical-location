from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from geopy.geocoders import Nominatim
from .models import Location
from .serializers import LocationSerializer


class LocationList(APIView):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            address = serializer.validated_data.get('address')
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.geocode(address)
            if location:
                serializer.save(latitude=location.latitude, longitude=location.longitude)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"error": "Address not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
