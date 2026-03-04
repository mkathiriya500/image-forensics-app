import exifread
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import datetime
import hashlib
import os

class MetadataExtractor:
    def extract_all(self, image_path):
        """Extract all metadata from image"""
        metadata = {
            'file_info': self.get_file_info(image_path),
            'exif_data': self.extract_exif(image_path),
            'gps_data': self.extract_gps(image_path),
            'image_dimensions': self.get_image_dimensions(image_path)
        }
        return metadata
    
    def get_file_info(self, image_path):
        """Get basic file information"""
        stat = os.stat(image_path)
        return {
            'filename': os.path.basename(image_path),
            'file_size': stat.st_size,
            'created': datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'md5_hash': self.calculate_md5(image_path)
        }
    
    def calculate_md5(self, image_path):
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        with open(image_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def extract_exif(self, image_path):
        """Extract EXIF data from image"""
        exif_data = {}
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f)
                for tag, value in tags.items():
                    tag_name = tag.replace('EXIF ', '').replace('Image ', '')
                    exif_data[tag_name] = str(value)
        except Exception as e:
            exif_data['error'] = str(e)
        return exif_data
    
    def extract_gps(self, image_path):
        """Extract GPS coordinates from image"""
        gps_data = {}
        try:
            image = Image.open(image_path)
            exif = image._getexif()
            if exif:
                gps_info = {}
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "GPSInfo":
                        for t in value:
                            sub_tag = GPSTAGS.get(t, t)
                            gps_info[sub_tag] = value[t]
                if gps_info:
                    gps_data = {'raw': gps_info}
        except Exception as e:
            gps_data['error'] = str(e)
        return gps_data
    
    def get_image_dimensions(self, image_path):
        """Get image dimensions"""
        try:
            with Image.open(image_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode
                }
        except:
            return {}