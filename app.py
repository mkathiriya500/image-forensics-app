import streamlit as st
import os
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules.reverse_image_search import ReverseImageSearcher
from modules.metadata_extractor import MetadataExtractor
from modules.face_analyzer import FaceAnalyzer
from modules.video_analyzer import VideoAnalyzer
from modules.location_analyzer import LocationAnalyzer
from utils.config import load_config, save_config
from utils.helpers import cleanup_temp_files, setup_directories

# Page configuration
st.set_page_config(
    page_title="Image & Video Forensics Tool",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open('static/css/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

class ImageVideoForensicsApp:
    def __init__(self):
        # Initialize components
        self.searcher = ReverseImageSearcher()
        self.metadata = MetadataExtractor()
        self.face_analyzer = FaceAnalyzer()
        self.video_analyzer = VideoAnalyzer()
        self.location = LocationAnalyzer()
        
        # Load configuration
        self.config = load_config()
        
        # Setup directories
        setup_directories()
    
    def run(self):
        # Sidebar
        with st.sidebar:
            self.render_sidebar()
        
        # Main content
        self.render_main_content()
    
    def render_sidebar(self):
        st.image("https://via.placeholder.com/300x100?text=Forensics+Tool", use_column_width=True)
        st.title("🔍 Navigation")
        
        # Analysis mode selector
        self.analysis_mode = st.radio(
            "Select Mode",
            ["Single Image", "Single Video", "Batch Processing", "Settings"],
            key="navigation"
        )
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Today's Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Files Processed", "0", "0")
        with col2:
            st.metric("Matches Found", "0", "0")
        
        st.markdown("---")
        
        # About section
        with st.expander("ℹ️ About"):
            st.markdown("""
            **Version:** 1.0.0  
            **Tools Integrated:**
            - Google Images
            - Yandex Images
            - TinEye
            - PimEyes
            - Ghiro
            - CARNET AI
            - TalkWalk
            - Hootsuite
            """)
    
    def render_main_content(self):
        if self.analysis_mode == "Single Image":
            self.render_image_analysis()
        elif self.analysis_mode == "Single Video":
            self.render_video_analysis()
        elif self.analysis_mode == "Batch Processing":
            self.render_batch_processing()
        else:
            self.render_settings()
    
    def render_image_analysis(self):
        st.title("🖼️ Single Image Analysis")
        st.markdown("Upload an image to analyze its metadata, perform reverse searches, and more.")
        
        # Create tabs for different upload methods
        tab1, tab2, tab3 = st.tabs(["📤 Upload File", "🔗 URL", "📋 Clipboard"])
        
        with tab1:
            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
                help="Maximum file size: 200MB"
            )
            
            if uploaded_file:
                self.process_uploaded_image(uploaded_file)
        
        with tab2:
            image_url = st.text_input("Enter image URL:")
            if image_url and st.button("Fetch & Analyze"):
                self.process_image_url(image_url)
        
        with tab3:
            st.info("Paste image from clipboard (Ctrl+V)")
            # Clipboard functionality would require JavaScript
    
    def process_uploaded_image(self, uploaded_file):
        # Save uploaded file
        temp_path = f"temp/{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Display image and analysis options
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
            # Analysis options
            st.markdown("### 🔎 Analysis Options")
            
            analysis_config = {
                'metadata': st.checkbox("📊 Extract Metadata", value=True),
                'reverse_search': st.checkbox("🔍 Reverse Image Search", value=True),
                'face_recognition': st.checkbox("👤 Face Recognition", value=False),
                'location': st.checkbox("📍 Location Analysis", value=True),
                'object_detection': st.checkbox("🎯 Object Detection", value=False),
                'social_search': st.checkbox("🌐 Social Media Search", value=False)
            }
            
            if st.button("🚀 Start Analysis", type="primary", use_column_width=True):
                with st.spinner("Analyzing image... This may take a few moments..."):
                    results = self.analyze_image(temp_path, analysis_config)
                    self.display_results(results)
        
        with col2:
            # Preview of what will be analyzed
            st.markdown("### 📋 Analysis Summary")
            st.info("""
            **What will be analyzed:**
            - EXIF metadata (camera, date, settings)
            - GPS coordinates if available
            - Reverse image search on multiple engines
            - Face detection and recognition
            - Location verification
            - Social media presence
            """)
        
        # Cleanup
        cleanup_temp_files([temp_path])
    
    def analyze_image(self, image_path, config):
        """Perform analysis based on configuration"""
        results = {}
        
        if config['metadata']:
            results['metadata'] = self.metadata.extract_all(image_path)
        
        if config['reverse_search']:
            results['reverse_search'] = self.searcher.search_all_engines(
                image_path,
                engines=['google', 'yandex', 'tineye']
            )
        
        if config['face_recognition']:
            results['face_analysis'] = self.face_analyzer.search_pimeyes(image_path)
            results['face_detection'] = self.face_analyzer.detect_faces(image_path)
        
        if config['location']:
            results['location'] = self.location.analyze_location(image_path)
        
        return results
    
    def display_results(self, results):
        st.markdown("---")
        st.header("📊 Analysis Results")
        
        # Create tabs for different result categories
        tabs = st.tabs([
            "📋 Summary", 
            "📍 Location", 
            "📷 Metadata", 
            "🔍 Search Results", 
            "👤 Face Analysis",
            "📈 Export"
        ])
        
        with tabs[0]:  # Summary
            self.display_summary(results)
        
        with tabs[1]:  # Location
            self.display_location(results)
        
        with tabs[2]:  # Metadata
            self.display_metadata(results)
        
        with tabs[3]:  # Search Results
            self.display_search_results(results)
        
        with tabs[4]:  # Face Analysis
            self.display_face_analysis(results)
        
        with tabs[5]:  # Export
            self.display_export_options(results)
    
    def display_summary(self, results):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'metadata' in results:
                st.metric("Camera Make", results['metadata'].get('camera_make', 'N/A'))
        
        with col2:
            if 'metadata' in results:
                st.metric("Camera Model", results['metadata'].get('camera_model', 'N/A'))
        
        with col3:
            if 'metadata' in results:
                date_taken = results['metadata'].get('datetime', 'Unknown')
                st.metric("Date Taken", date_taken[:10] if date_taken != 'Unknown' else 'Unknown')
        
        with col4:
            if 'reverse_search' in results:
                total_matches = sum(
                    len(v.get('matches', [])) 
                    for v in results['reverse_search'].values()
                )
                st.metric("Online Matches", total_matches)
        
        # Quick insights
        st.markdown("### 🔍 Quick Insights")
        
        insights = []
        if 'location' in results and results['location'].get('has_gps'):
            insights.append("✅ GPS coordinates found in image")
        if 'face_detection' in results:
            faces = results['face_detection'].get('total_faces', 0)
            insights.append(f"👤 {faces} face(s) detected in image")
        if 'metadata' in results:
            if results['metadata'].get('exif_data'):
                insights.append("📷 EXIF metadata available")
        
        for insight in insights:
            st.markdown(f"- {insight}")
    
    def display_location(self, results):
        if 'location' in results and results['location'].get('coordinates'):
            coords = results['location']['coordinates']
            
            # Create map
            import folium
            from streamlit_folium import st_folium
            
            m = folium.Map(location=[coords['lat'], coords['lon']], zoom_start=15)
            
            # Add marker
            folium.Marker(
                [coords['lat'], coords['lon']],
                popup='📍 Image Location',
                tooltip='Click for details',
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
            
            # Add circle for accuracy
            folium.Circle(
                [coords['lat'], coords['lon']],
                radius=100,
                color='red',
                fill=True,
                fillOpacity=0.1
            ).add_to(m)
            
            # Display map
            st_folium(m, width=700, height=500)
            
            # Location details
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📍 Coordinates:**")
                st.code(f"Latitude: {coords['lat']}\nLongitude: {coords['lon']}")
                
                st.markdown("**🗺️ Maps Links:**")
                st.markdown(f"[Google Maps](https://www.google.com/maps?q={coords['lat']},{coords['lon']})")
                st.markdown(f"[OpenStreetMap](https://www.openstreetmap.org/?mlat={coords['lat']}&mlon={coords['lon']})")
            
            with col2:
                if results['location'].get('address'):
                    st.markdown("**🏠 Address:**")
                    st.info(results['location']['address'])
        else:
            st.warning("No location data found in image metadata")
    
    def display_metadata(self, results):
        if 'metadata' in results:
            # Create expandable sections for different metadata categories
            with st.expander("📁 File Information", expanded=True):
                file_info = results['metadata'].get('file_info', {})
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Filename:** {file_info.get('filename', 'N/A')}")
                    st.markdown(f"**File Size:** {file_info.get('file_size', 0)} bytes")
                with col2:
                    st.markdown(f"**Created:** {file_info.get('created', 'N/A')}")
                    st.markdown(f"**MD5 Hash:** `{file_info.get('md5_hash', 'N/A')}`")
            
            with st.expander("📷 Camera Information", expanded=True):
                exif = results['metadata'].get('exif_data', {})
                camera_info = {
                    'Make': exif.get('Make', 'N/A'),
                    'Model': exif.get('Model', 'N/A'),
                    'Software': exif.get('Software', 'N/A'),
                    'DateTime': exif.get('DateTime', 'N/A')
                }
                for key, value in camera_info.items():
                    st.markdown(f"**{key}:** {value}")
            
            with st.expander("⚙️ Image Settings"):
                dimensions = results['metadata'].get('image_dimensions', {})
                st.markdown(f"**Dimensions:** {dimensions.get('width', 'N/A')}x{dimensions.get('height', 'N/A')}")
                st.markdown(f"**Format:** {dimensions.get('format', 'N/A')}")
                st.markdown(f"**Color Mode:** {dimensions.get('mode', 'N/A')}")
            
            with st.expander("🔧 EXIF Data (Raw)"):
                st.json(results['metadata'].get('exif_data', {}))
        else:
            st.warning("No metadata available")
    
    def display_search_results(self, results):
        if 'reverse_search' in results:
            for engine, data in results['reverse_search'].items():
                with st.expander(f"🔍 {engine.title()} Results"):
                    if 'error' in data:
                        st.error(f"Error: {data['error']}")
                    else:
                        matches = data.get('matches', [])
                        st.markdown(f"**Found {len(matches)} matches**")
                        
                        for i, match in enumerate(matches[:10]):  # Show top 10
                            st.markdown(f"{i+1}. [{match.get('title', 'Link')}]({match.get('url', '#')})")
        else:
            st.info("Reverse search not performed")
    
    def display_face_analysis(self, results):
        if 'face_detection' in results:
            faces = results['face_detection']
            st.markdown(f"**Total Faces Detected:** {faces.get('total_faces', 0)}")
            
            for i, face in enumerate(faces.get('faces', [])):
                with st.expander(f"Face #{i+1}"):
                    if 'thumbnail' in face:
                        st.image(face['thumbnail'], caption=f"Face {i+1}")
                    
                    bbox = face.get('bbox', {})
                    st.markdown(f"**Position:** x={bbox.get('x')}, y={bbox.get('y')}")
                    st.markdown(f"**Size:** {bbox.get('width')}x{bbox.get('height')}")
        
        if 'face_analysis' in results:
            with st.expander("🔍 PimEyes Search Results"):
                st.json(results['face_analysis'])
    
    def display_export_options(self, results):
        st.markdown("### 📥 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export as JSON
            if st.button("📄 Export as JSON", use_column_width=True):
                import json
                from datetime import datetime
                
                # Add timestamp
                results['exported_at'] = datetime.now().isoformat()
                
                # Convert to JSON string
                json_str = json.dumps(results, indent=2, default=str)
                
                # Create download button
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            # Generate report
            if st.button("📑 Generate Report", use_column_width=True):
                report = self.generate_report(results)
                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        # Share options
        st.markdown("### 📤 Share Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🐦 Twitter"):
                st.info("Twitter sharing requires API integration")
        
        with col2:
            if st.button("📘 Facebook"):
                st.info("Facebook sharing requires API integration")
        
        with col3:
            if st.button("📱 Hootsuite"):
                st.info("Hootsuite integration coming soon")
    
    def generate_report(self, results):
        """Generate a text report from results"""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("IMAGE FORENSICS ANALYSIS REPORT")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        # Summary
        report_lines.append("SUMMARY")
        report_lines.append("-" * 30)
        
        if 'metadata' in results:
            file_info = results['metadata'].get('file_info', {})
            report_lines.append(f"File: {file_info.get('filename', 'Unknown')}")
            report_lines.append(f"Size: {file_info.get('file_size', 0)} bytes")
        
        if 'location' in results and results['location'].get('coordinates'):
            coords = results['location']['coordinates']
            report_lines.append(f"GPS: {coords['lat']}, {coords['lon']}")
        
        report_lines.append("")
        
        # Metadata section
        if 'metadata' in results:
            report_lines.append("METADATA")
            report_lines.append("-" * 30)
            exif = results['metadata'].get('exif_data', {})
            for key, value in list(exif.items())[:20]:  # Limit to 20 items
                report_lines.append(f"{key}: {value}")
        
        return "\n".join(report_lines)
    
    def render_video_analysis(self):
        st.title("🎬 Single Video Analysis")
        st.markdown("Upload a video to extract keyframes, analyze metadata, and more.")
        
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'],
            help="Maximum file size: 500MB"
        )
        
        if uploaded_file:
            temp_path = f"temp/{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.video(uploaded_file)
            
            if st.button("🔍 Analyze Video", type="primary"):
                with st.spinner("Analyzing video... This may take a few minutes..."):
                    results = self.video_analyzer.analyze_video(temp_path)
                    self.display_video_results(results)
            
            cleanup_temp_files([temp_path])
    
    def display_video_results(self, results):
        st.markdown("---")
        st.header("📊 Video Analysis Results")
        
        # Basic info
        col1, col2, col3, col4 = st.columns(4)
        basic_info = results.get('basic_info', {})
        
        with col1:
            st.metric("Duration", f"{basic_info.get('duration', 0):.2f}s")
        with col2:
            st.metric("Resolution", basic_info.get('resolution', 'N/A'))
        with col3:
            st.metric("FPS", f"{basic_info.get('fps', 0):.2f}")
        with col4:
            st.metric("Frames", basic_info.get('frame_count', 0))
        
        # Keyframes
        if 'keyframes' in results and results['keyframes']:
            st.markdown("### 🎞️ Keyframes")
            cols = st.columns(3)
            for i, frame in enumerate(results['keyframes'][:6]):
                with cols[i % 3]:
                    st.image(frame['image'], caption=f"Frame at {frame['timestamp']:.1f}s")
        
        # Scene changes
        if 'scene_changes' in results and results['scene_changes']:
            with st.expander("🎬 Scene Changes"):
                for scene in results['scene_changes'][:10]:
                    st.markdown(f"- Frame {scene['frame']} at {scene['timestamp']:.1f}s")
        
        # Metadata
        if 'metadata' in results:
            with st.expander("📷 Video Metadata"):
                st.json(results['metadata'])
    
    def render_batch_processing(self):
        st.title("📁 Batch Processing")
        st.markdown("Upload multiple files for batch analysis")
        
        uploaded_files = st.file_uploader(
            "Choose multiple files",
            type=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov'],
            accept_multiple_files=True
        )
        
        if uploaded_files and st.button("🚀 Process Batch", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Processing {file.name}...")
                
                temp_path = f"temp/{file.name}"
                with open(temp_path, "wb") as f:
                    f.write(file.getbuffer())
                
                if file.type.startswith('image'):
                    result = self.analyze_image(temp_path, {
                        'metadata': True,
                        'reverse_search': True,
                        'location': True
                    })
                else:
                    result = self.video_analyzer.analyze_video(temp_path)
                
                results.append({
                    'filename': file.name,
                    'type': 'image' if file.type.startswith('image') else 'video',
                    'result': result
                })
                
                cleanup_temp_files([temp_path])
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("✅ Processing complete!")
            
            # Display summary
            st.markdown("### 📊 Batch Summary")
            st.json({
                'total_files': len(results),
                'images': sum(1 for r in results if r['type'] == 'image'),
                'videos': sum(1 for r in results if r['type'] == 'video')
            })
            
            # Export batch results
            if st.button("📥 Export All Results"):
                import json
                from datetime import datetime
                
                json_str = json.dumps(results, indent=2, default=str)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    def render_settings(self):
        st.title("⚙️ Settings")
        
        tabs = st.tabs(["🔑 API Keys", "🎨 Appearance", "📊 Analysis Defaults", "💾 Storage"])
        
        with tabs[0]:
            st.markdown("### API Configuration")
            st.warning("⚠️ API keys are stored locally and never shared")
            
            # PimEyes API
            pimeyes_key = st.text_input(
                "PimEyes API Key",
                type="password",
                value=self.config.get('pimeyes_api_key', ''),
                help="Required for face recognition features"
            )
            
            # CARNET AI
            carnet_key = st.text_input(
                "CARNET AI API Key",
                type="password",
                value=self.config.get('carnet_api_key', ''),
                help="For advanced AI analysis"
            )
            
            # Social Media APIs
            twitter_key = st.text_input(
                "Twitter API Key",
                type="password",
                value=self.config.get('twitter_api_key', '')
            )
            
            if st.button("💾 Save API Keys"):
                self.config['pimeyes_api_key'] = pimeyes_key
                self.config['carnet_api_key'] = carnet_key
                self.config['twitter_api_key'] = twitter_key
                save_config(self.config)
                st.success("API keys saved successfully!")
        
        with tabs[1]:
            st.markdown("### Appearance Settings")
            
            theme = st.selectbox(
                "Theme",
                ["Light", "Dark", "System Default"],
                index=1
            )
            
            st.markdown("Coming soon: Custom color schemes and layouts")
        
        with tabs[2]:
            st.markdown("### Default Analysis Settings")
            
            st.checkbox("Always extract metadata", value=True)
            st.checkbox("Always perform reverse search", value=True)
            st.checkbox("Always analyze location", value=True)
            st.checkbox("Auto-detect faces", value=False)
            
            st.number_input(
                "Reverse search timeout (seconds)",
                min_value=5,
                max_value=60,
                value=30
            )
        
        with tabs[3]:
            st.markdown("### Storage Settings")
            
            st.markdown(f"**Temp directory:** `{os.path.abspath('temp')}`")
            st.markdown(f"**Output directory:** `{os.path.abspath('output')}`")
            
            # Cleanup options
            if st.button("🧹 Clean Temp Files"):
                count = cleanup_temp_files()
                st.success(f"Cleaned {count} temporary files")
            
            # Max storage
            st.slider(
                "Max temp storage (MB)",
                min_value=100,
                max_value=5000,
                value=1000,
                step=100
            )

# Run the app
if __name__ == "__main__":
    app = ImageVideoForensicsApp()
    app.run()