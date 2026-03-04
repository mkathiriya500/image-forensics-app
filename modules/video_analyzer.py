import cv2
import os
from datetime import datetime

class VideoAnalyzer:
    def analyze_video(self, video_path):
        """Analyze video file"""
        results = {
            'basic_info': self.get_basic_info(video_path),
            'metadata': self.extract_metadata(video_path),
            'keyframes': self.extract_keyframes(video_path),
            'scene_changes': self.detect_scene_changes(video_path)
        }
        return results
    
    def get_basic_info(self, video_path):
        """Get basic video information"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            return {'error': 'Could not open video'}
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0
        
        cap.release()
        
        # Get file info
        file_stat = os.stat(video_path)
        
        return {
            'filename': os.path.basename(video_path),
            'file_size': file_stat.st_size,
            'duration': duration,
            'fps': fps,
            'frame_count': frame_count,
            'resolution': f"{width}x{height}",
            'width': width,
            'height': height,
            'created': datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        }
    
    def extract_metadata(self, video_path):
        """Extract video metadata"""
        cap = cv2.VideoCapture(video_path)
        
        metadata = {
            'codec': int(cap.get(cv2.CAP_PROP_FOURCC)),
            'brightness': cap.get(cv2.CAP_PROP_BRIGHTNESS),
            'contrast': cap.get(cv2.CAP_PROP_CONTRAST),
            'saturation': cap.get(cv2.CAP_PROP_SATURATION)
        }
        
        cap.release()
        return metadata
    
    def extract_keyframes(self, video_path, max_keyframes=5):
        """Extract keyframes from video"""
        cap = cv2.VideoCapture(video_path)
        keyframes = []
        frame_count = 0
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        while len(keyframes) < max_keyframes:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Extract keyframe every 2 seconds
            if frame_count % int(fps * 2) == 0:
                # Convert frame to JPEG
                _, buffer = cv2.imencode('.jpg', frame)
                
                keyframes.append({
                    'frame_number': frame_count,
                    'timestamp': frame_count / fps,
                    'image': buffer.tobytes()
                })
            
            frame_count += 1
        
        cap.release()
        return keyframes
    
    def detect_scene_changes(self, video_path, threshold=30.0):
        """Detect scene changes in video"""
        cap = cv2.VideoCapture(video_path)
        scene_changes = []
        prev_frame = None
        frame_count = 0
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if prev_frame is not None:
                # Calculate frame difference
                diff = cv2.absdiff(frame, prev_frame)
                mean_diff = diff.mean()
                
                if mean_diff > threshold:
                    scene_changes.append({
                        'frame': frame_count,
                        'timestamp': frame_count / fps,
                        'difference': float(mean_diff)
                    })
            
            prev_frame = frame.copy()
            frame_count += 1
        
        cap.release()
        return scene_changes