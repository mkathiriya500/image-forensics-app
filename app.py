import streamlit as st
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent))

# Check which modules are available
try:
    from modules.reverse_image_search import ReverseImageSearcher
    REVERSE_SEARCH_AVAILABLE = True
except ImportError as e:
    REVERSE_SEARCH_AVAILABLE = False
    st.warning(f"Reverse search module not available: {e}")

try:
    from modules.metadata_extractor import MetadataExtractor
    METADATA_EXTRACTOR_AVAILABLE = True
except ImportError:
    METADATA_EXTRACTOR_AVAILABLE = False

try:
    from modules.location_analyzer import LocationAnalyzer
    LOCATION_ANALYZER_AVAILABLE = True
except ImportError:
    LOCATION_ANALYZER_AVAILABLE = False

# These might fail - handle gracefully
try:
    from modules.face_analyzer import FaceAnalyzer
    FACE_ANALYZER_AVAILABLE = True
except ImportError:
    FACE_ANALYZER_AVAILABLE = False

try:
    from modules.video_analyzer import VideoAnalyzer
    VIDEO_ANALYZER_AVAILABLE = True
except ImportError:
    VIDEO_ANALYZER_AVAILABLE = False