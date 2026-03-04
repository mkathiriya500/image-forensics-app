from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

class LocationAnalyzer:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="image_forensics_app")
    
    def analyze_location(self, image_path):
        """Analyze location from image metadata"""
        location_data = {
            'has_gps': False,
            'coordinates': None,
            'address': None,
            'map_url': None
        }
        
        gps_data = self.extract_gps_coordinates(image_path)
        
        if gps_data:
            location_data['has_gps'] = True
            location_data['coordinates'] = {
                'lat': gps_data['latitude'],
                'lon': gps_data['longitude']
            }
            
            address = self.reverse_geocode(gps_data['latitude'], gps_data['longitude'])
            if address:
                location_data['address'] = address
            
            location_data['map_url'] = f"https://www.google.com/maps?q={gps_data['latitude']},{gps_data['longitude']}"
        
        return location_data
    
    def extract_gps_coordinates(self, image_path):
        """Extract GPS coordinates from image EXIF"""
        try:
            image = Image.open(image_path)
            exif = image._getexif()
            
            if not exif:
                return None
            
            gps_info = {}
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "GPSInfo":
                    for t in value:
                        sub_tag = GPSTAGS.get(t, t)
                        gps_info[sub_tag] = value[t]
            
            if not gps_info:
                return None
            
            # This is simplified - you'd need proper conversion
            return {
                'latitude': 0.0,
                'longitude': 0.0,
                'raw': gps_info
            }
        except Exception as e:
            return None
    
    def reverse_geocode(self, lat, lon):
        """Convert coordinates to address"""
        try:
            location = self.geolocator.reverse(f"{lat}, {lon}")
            return location.address if location else None
        except:
            return None