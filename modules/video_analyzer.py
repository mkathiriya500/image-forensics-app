import os
from datetime import datetime

class VideoAnalyzer:
    def analyze_video(self, video_path):
        """Analyze video file - simplified version"""
        results = {
            'basic_info': self.get_basic_info(video_path),
            'message': 'Video analysis limited - OpenCV not available'
        }
        return results
    
    def get_basic_info(self, video_path):
        """Get basic video information without OpenCV"""
        try:
            # Get file info only
            file_stat = os.stat(video_path)
            
            return {
                'filename': os.path.basename(video_path),
                'file_size': file_stat.st_size,
                'created': datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                'note': 'Full video analysis requires OpenCV which is not installed'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def extract_keyframes(self, video_path, max_keyframes=5):
        """Keyframe extraction disabled"""
        return []
    
    def detect_scene_changes(self, video_path, threshold=30.0):
        """Scene change detection disabled"""
        return []