import streamlit as st
import pydicom
from PIL import Image
import numpy as np
import io

st.title("🩺 DICOM Viewer")
st.markdown("### View and analyze medical imaging files (CT/MRI scans)")

st.markdown("---")

st.info("📋 **DICOM** (Digital Imaging and Communications in Medicine) is the standard format for medical images")

uploaded_file = st.file_uploader(
    "Upload a DICOM file (.dcm)",
    type=['dcm'],
    help="Upload CT, MRI, or other DICOM medical imaging files"
)

if uploaded_file is not None:
    try:
        dicom_data = pydicom.dcmread(io.BytesIO(uploaded_file.read()))
        
        st.success("✅ DICOM file loaded successfully!")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🖼️ Image Visualization")
            
            pixel_array = dicom_data.pixel_array
            
            if len(pixel_array.shape) == 2:
                normalized_image = ((pixel_array - pixel_array.min()) / 
                                  (pixel_array.max() - pixel_array.min()) * 255).astype(np.uint8)
                
                img = Image.fromarray(normalized_image)
                st.image(img, caption="DICOM Image", use_container_width=True)
                
                st.markdown("#### Image Statistics")
                col_a, col_b, col_c, col_d = st.columns(4)
                with col_a:
                    st.metric("Min Pixel Value", f"{pixel_array.min()}")
                with col_b:
                    st.metric("Max Pixel Value", f"{pixel_array.max()}")
                with col_c:
                    st.metric("Mean", f"{pixel_array.mean():.2f}")
                with col_d:
                    st.metric("Std Dev", f"{pixel_array.std():.2f}")
                
            else:
                st.info(f"ℹ️ Multi-dimensional image with shape: {pixel_array.shape}")
                
                if len(pixel_array.shape) == 3:
                    slice_idx = st.slider("Select Slice", 0, pixel_array.shape[0] - 1, 0)
                    slice_data = pixel_array[slice_idx]
                    
                    normalized_slice = ((slice_data - slice_data.min()) / 
                                       (slice_data.max() - slice_data.min()) * 255).astype(np.uint8)
                    
                    img = Image.fromarray(normalized_slice)
                    st.image(img, caption=f"Slice {slice_idx}", use_container_width=True)
        
        with col2:
            st.subheader("📊 Metadata")
            
            metadata_items = [
                ("Patient Name", "PatientName"),
                ("Patient ID", "PatientID"),
                ("Study Date", "StudyDate"),
                ("Modality", "Modality"),
                ("Body Part", "BodyPartExamined"),
                ("Institution", "InstitutionName"),
                ("Manufacturer", "Manufacturer"),
                ("Rows", "Rows"),
                ("Columns", "Columns"),
            ]
            
            for label, tag in metadata_items:
                try:
                    value = getattr(dicom_data, tag, "N/A")
                    st.text(f"{label}: {value}")
                except:
                    st.text(f"{label}: N/A")
            
            st.markdown("---")
            
            st.subheader("🔍 Image Properties")
            st.text(f"Shape: {pixel_array.shape}")
            st.text(f"Data Type: {pixel_array.dtype}")
            st.text(f"Size: {pixel_array.nbytes / 1024:.2f} KB")
        
        st.markdown("---")
        
        with st.expander("📋 Full DICOM Header Information"):
            st.text(str(dicom_data))
        
        with st.expander("🎨 Windowing Controls (Advanced)"):
            st.markdown("Adjust window level and width for better visualization")
            
            default_center = int(pixel_array.mean())
            default_width = int(pixel_array.std() * 2)
            
            window_center = st.slider("Window Center", 
                                      int(pixel_array.min()), 
                                      int(pixel_array.max()), 
                                      default_center)
            window_width = st.slider("Window Width", 1, 
                                     int(pixel_array.max() - pixel_array.min()), 
                                     default_width)
            
            min_val = window_center - window_width // 2
            max_val = window_center + window_width // 2
            
            if len(pixel_array.shape) == 2:
                windowed = np.clip(pixel_array, min_val, max_val)
                windowed_normalized = ((windowed - min_val) / (max_val - min_val) * 255).astype(np.uint8)
                windowed_img = Image.fromarray(windowed_normalized)
                st.image(windowed_img, caption="Windowed Image", use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error loading DICOM file: {str(e)}")
        st.info("💡 Make sure you uploaded a valid DICOM (.dcm) file")

else:
    st.markdown("""
    ### 📝 Instructions
    
    1. **Upload a DICOM file** using the file uploader above
    2. **View the medical image** with automatic normalization
    3. **Inspect metadata** including patient info, study details, and imaging parameters
    4. **Use windowing controls** to adjust image contrast and brightness
    5. **Navigate slices** for multi-slice CT/MRI scans
    
    ---
    
    ### 🔍 Supported Features
    
    - ✅ CT (Computed Tomography) scans
    - ✅ MRI (Magnetic Resonance Imaging) scans  
    - ✅ X-Ray images
    - ✅ Multi-slice volume data
    - ✅ Metadata extraction
    - ✅ Window level/width adjustment
    
    ---
    
    ### 📌 Sample DICOM Files
    
    You can find sample DICOM files for testing at:
    - [DICOM Library](https://www.dicomlibrary.com/)
    - [Medical Imaging Samples](https://www.rubomedical.com/dicom_files/)
    """)

st.markdown("---")
st.caption("⚠️ **Privacy Notice**: This is a demonstration tool. Do not upload actual patient data without proper authorization and compliance with HIPAA regulations.")
