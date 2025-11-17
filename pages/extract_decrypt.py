import streamlit as st
import os
import sys
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.dna_encryption import DNAEncryption, AES256DNAEncryption
from utils.lsb_steganography import LSBSteganography

st.title("🔓 Extract & Decrypt")
st.markdown("### Extract hidden data from stego-images and decrypt using DNA cipher")

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🖼️ Step 1: Upload Stego-Image")
    stego_image = st.file_uploader(
        "Choose the stego-image containing hidden data:",
        type=['png', 'jpg', 'jpeg', 'bmp'],
        help="This should be the image created in the Encrypt & Embed page"
    )
    
    if stego_image:
        st.image(stego_image, caption="Stego-Image", use_container_width=True)
    
    st.subheader("🔒 Step 2: Decryption Options")
    uses_aes = st.checkbox("🛡️ Image uses AES-256 Encryption", value=False,
                           help="Check this if the image was encrypted with AES-256")
    
    decryption_key = None
    if uses_aes:
        decryption_key = st.text_input(
            "Decryption Key (Base64)",
            type="password",
            placeholder="Enter the encryption key",
            help="Enter the same key used during encryption"
        )

with col2:
    st.subheader("🔄 Decryption Pipeline")
    
    if uses_aes:
        st.markdown("""
        **Enhanced Decryption Steps (AES-256 + DNA):**
        1. Extract LSB data from image pixels
        2. Detect end marker and stop extraction
        3. Convert binary to DNA sequence
        4. Apply reverse substitution (T→A, A→T, G→C, C→G)
        5. DNA → Binary → Base64 conversion
        6. AES-256 Decryption
        7. Original plaintext recovered
        """)
        st.success("🛡️ **AES-256 decryption mode**")
    else:
        st.markdown("""
        **Standard Decryption Steps:**
        1. Extract LSB data from image pixels
        2. Detect end marker and stop extraction
        3. Convert binary to DNA sequence
        4. Apply reverse substitution (T→A, A→T, G→C, C→G)
        5. DNA → Binary → Text conversion
        """)
    
    if stego_image:
        st.success("✅ Stego-image loaded successfully")

st.markdown("---")

if st.button("🔍 Extract and Decrypt", type="primary", use_container_width=True):
    if not stego_image:
        st.error("❌ Please upload a stego-image")
    elif uses_aes and not decryption_key:
        st.error("❌ Please provide the decryption key")
    else:
        with st.spinner("Extracting and decrypting data..."):
            temp_stego_path = None
            try:
                lsb_steg = LSBSteganography()
                
                if uses_aes:
                    import base64
                    try:
                        decoded_key = base64.b64decode(decryption_key)
                        dna_enc = AES256DNAEncryption(key=decoded_key)
                    except Exception as e:
                        st.error(f"❌ Invalid Base64 key format. Please check your decryption key.")
                        raise
                else:
                    dna_enc = DNAEncryption()
                
                temp_stego_path = "temp_stego_extract.png"
                Image.open(stego_image).save(temp_stego_path)
                
                with st.expander("🖼️ LSB Extraction Process", expanded=True):
                    extraction_result = lsb_steg.extract(temp_stego_path)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Extraction Time", f"{extraction_result['extraction_time']:.4f}s")
                    with col2:
                        st.metric("Binary Length", f"{extraction_result['binary_length']} bits")
                    
                    extracted_dna = extraction_result['extracted_data']
                    st.code(extracted_dna[:200] + "..." if len(extracted_dna) > 200 else extracted_dna)
                    st.success(f"✅ Extracted {len(extracted_dna)} DNA bases from image")
                
                with st.expander("🔬 DNA Decryption Process", expanded=True):
                    if uses_aes:
                        decryption_result = dna_enc.decrypt(extracted_dna, use_aes=True)
                        st.success("✅ AES-256 + DNA decryption completed successfully")
                    else:
                        decryption_result = dna_enc.decrypt(extracted_dna)
                        st.success("✅ DNA decryption completed successfully")
                    
                    st.metric("Decryption Time", f"{decryption_result['decryption_time']:.4f}s")
                
                st.markdown("---")
                st.subheader("📄 Decrypted Message")
                
                decrypted_text = decryption_result['decrypted_text']
                
                st.text_area(
                    "Original Secret Message:",
                    value=decrypted_text,
                    height=200,
                    disabled=True
                )
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Message Length", f"{len(decrypted_text)} characters")
                with col2:
                    st.metric("Total Extraction Time", f"{extraction_result['extraction_time']:.4f}s")
                with col3:
                    st.metric("Total Decryption Time", f"{decryption_result['decryption_time']:.4f}s")
                
                total_time = extraction_result['extraction_time'] + decryption_result['decryption_time']
                st.info(f"⏱️ Total processing time: {total_time:.4f} seconds")
                
                if 'decryption_history' not in st.session_state:
                    st.session_state.decryption_history = []
                
                st.session_state.decryption_history.append({
                    'message_length': len(decrypted_text),
                    'extraction_time': extraction_result['extraction_time'],
                    'decryption_time': decryption_result['decryption_time'],
                    'total_time': total_time
                })
                
                st.success("✅ Extraction and decryption completed successfully!")
                
                st.markdown("---")
                st.download_button(
                    label="💾 Download Decrypted Message",
                    data=decrypted_text,
                    file_name="decrypted_message.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ Error during extraction/decryption: {str(e)}")
                st.info("💡 Make sure you uploaded a valid stego-image created by this system")
            finally:
                if temp_stego_path and os.path.exists(temp_stego_path):
                    try:
                        os.remove(temp_stego_path)
                    except:
                        pass

st.markdown("---")
st.info("💡 **Tip**: The extraction process will automatically stop when it finds the end marker, ensuring accurate data retrieval.")
