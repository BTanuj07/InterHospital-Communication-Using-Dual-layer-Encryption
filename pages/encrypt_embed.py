import streamlit as st
import os
import sys
from io import BytesIO
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.dna_encryption import DNAEncryption, AES256DNAEncryption
from utils.lsb_steganography import LSBSteganography
from utils.metrics import ImageMetrics

st.title("🔐 Encrypt & Embed")
st.markdown("### Secure your medical data using DNA encryption and LSB steganography")

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Step 1: Enter Secret Message")
    secret_message = st.text_area(
        "Enter the medical data or message to encrypt:",
        height=120,
        placeholder="e.g., Patient ID: 12345, Diagnosis: ..., Treatment: ..."
    )
    
    st.subheader("🔒 Step 2: Encryption Options")
    use_aes = st.checkbox("🛡️ Enable AES-256 Encryption (Military-Grade Security)", value=False, 
                          help="Add an additional AES-256 encryption layer before DNA encoding")
    
    encryption_key = None
    if use_aes:
        col_a, col_b = st.columns([3, 1])
        with col_a:
            encryption_key = st.text_input(
                "Encryption Key (Base64, 44 characters)",
                type="password",
                placeholder="Leave empty to auto-generate",
                help="Enter a Base64-encoded key (44 chars) or leave empty to auto-generate"
            )
        with col_b:
            if st.button("🔑 Generate", help="Generate random key"):
                import base64
                import os
                st.session_state.generated_key = base64.b64encode(os.urandom(32)).decode('utf-8')
        
        if 'generated_key' in st.session_state:
            encryption_key = st.session_state.generated_key
            st.info(f"🔑 Generated Key: `{encryption_key}`")
    
    st.subheader("🖼️ Step 3: Upload Cover Image")
    cover_image = st.file_uploader(
        "Choose an image to hide the data in:",
        type=['png', 'jpg', 'jpeg', 'bmp'],
        help="This image will carry the hidden encrypted message"
    )
    
    if cover_image:
        st.image(cover_image, caption="Cover Image", use_container_width=True)

with col2:
    st.subheader("🔄 Processing Pipeline")
    
    if use_aes:
        st.markdown("""
        **Enhanced Encryption Steps (AES-256 + DNA):**
        1. Text → AES-256 Encryption
        2. Encrypted Data → Base64 Encoding
        3. Base64 → Binary Conversion
        4. Binary → DNA Encoding (00→A, 01→T, 10→C, 11→G)
        5. DNA Symmetric Substitution (A↔T, C↔G)
        6. LSB Embedding into image pixels
        """)
        st.success("🛡️ **Military-grade security enabled!**")
    else:
        st.markdown("""
        **Standard Encryption Steps:**
        1. Text → Binary Conversion
        2. Binary → DNA Encoding (00→A, 01→T, 10→C, 11→G)
        3. DNA Symmetric Substitution (A↔T, C↔G)
        4. LSB Embedding into image pixels
        5. Add end marker for extraction
        """)
    
    if secret_message and cover_image:
        st.success(f"✅ Message length: {len(secret_message)} characters")
        st.info(f"📦 Binary size: {len(secret_message) * 8} bits")

st.markdown("---")

if st.button("🚀 Encrypt and Embed", type="primary", use_container_width=True):
    if not secret_message:
        st.error("❌ Please enter a secret message")
    elif not cover_image:
        st.error("❌ Please upload a cover image")
    elif use_aes and not encryption_key:
        st.error("❌ Please provide an encryption key or generate one")
    else:
        with st.spinner("Processing encryption and embedding..."):
            temp_cover_path = None
            temp_stego_path = None
            try:
                if use_aes:
                    import base64
                    try:
                        decoded_key = base64.b64decode(encryption_key) if encryption_key else None
                        dna_enc = AES256DNAEncryption(key=decoded_key)
                        actual_key = dna_enc.get_key_base64()
                    except Exception as e:
                        st.error(f"❌ Invalid Base64 key format. Please check your key or generate a new one.")
                        raise
                else:
                    dna_enc = DNAEncryption()
                    actual_key = None
                
                lsb_steg = LSBSteganography()
                
                with st.expander("🔬 DNA Encryption Process", expanded=True):
                    if use_aes:
                        encryption_result = dna_enc.encrypt(secret_message, use_aes=True)
                        st.success(f"🔐 AES-256 + DNA encryption applied")
                        st.code(f"Encryption Key (Base64): {actual_key}", language="text")
                        st.warning("⚠️ **IMPORTANT**: Save this key! You'll need it for decryption.")
                    else:
                        encryption_result = dna_enc.encrypt(secret_message)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Original Length", f"{encryption_result['original_length']} chars")
                    with col2:
                        st.metric("Binary Length", f"{encryption_result['binary_length']} bits")
                    with col3:
                        st.metric("DNA Length", f"{encryption_result['dna_length']} bases")
                    
                    st.code(encryption_result['encrypted_dna'][:200] + "..." if len(encryption_result['encrypted_dna']) > 200 else encryption_result['encrypted_dna'])
                    st.caption(f"⏱️ Encryption time: {encryption_result['encryption_time']:.4f} seconds")
                
                temp_cover_path = "temp_cover.png"
                Image.open(cover_image).save(temp_cover_path)
                
                with st.expander("🖼️ LSB Steganography Process", expanded=True):
                    embedding_result = lsb_steg.embed(temp_cover_path, encryption_result['encrypted_dna'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Payload Size", f"{embedding_result['payload_size']} chars")
                    with col2:
                        st.metric("Binary Size", f"{embedding_result['binary_size']} bits")
                    with col3:
                        st.metric("Embedding Time", f"{embedding_result['embedding_time']:.4f}s")
                    
                    st.success(f"✅ Data successfully embedded into image of size {embedding_result['image_size']}")
                
                stego_image = embedding_result['stego_image']
                temp_stego_path = "temp_stego.png"
                stego_image.save(temp_stego_path)
                
                with st.expander("📊 Quality Analysis", expanded=True):
                    psnr = ImageMetrics.calculate_psnr(temp_cover_path, temp_stego_path)
                    ssim = ImageMetrics.calculate_ssim(temp_cover_path, temp_stego_path)
                    
                    if psnr is not None and ssim is not None:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("PSNR", f"{psnr:.2f} dB", help="Higher is better (>40 dB is excellent)")
                        with col2:
                            st.metric("SSIM", f"{ssim:.4f}", help="Closer to 1.0 is better")
                        
                        if psnr > 40:
                            st.success("✅ Excellent image quality maintained!")
                        elif psnr > 30:
                            st.info("ℹ️ Good image quality")
                        else:
                            st.warning("⚠️ Image quality may be noticeably degraded")
                    else:
                        st.warning("⚠️ Could not calculate quality metrics")
                
                st.markdown("---")
                st.subheader("🔍 Image Quality Comparison")
                
                diff_stats = ImageMetrics.calculate_difference_stats(temp_cover_path, temp_stego_path)
                heatmap_image = ImageMetrics.create_difference_heatmap(temp_cover_path, temp_stego_path)
                
                if diff_stats:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Pixels", f"{diff_stats['total_pixels']:,}")
                    with col2:
                        st.metric("Changed Pixels", f"{diff_stats['changed_pixels']:,}")
                    with col3:
                        st.metric("Change %", f"{diff_stats['change_percentage']:.4f}%")
                    with col4:
                        st.metric("Max Diff", f"{diff_stats['max_difference']:.2f}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.image(cover_image, caption="Original Cover Image", use_container_width=True)
                
                with col2:
                    st.image(stego_image, caption="Stego-Image (with hidden data)", use_container_width=True)
                
                with col3:
                    if heatmap_image:
                        st.image(heatmap_image, caption="Pixel Difference Heatmap", use_container_width=True)
                    else:
                        st.warning("Could not generate heatmap")
                
                st.markdown("---")
                st.subheader("📥 Download Stego-Image")
                
                buf = BytesIO()
                stego_image.save(buf, format='PNG')
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="💾 Download Stego-Image",
                    data=byte_im,
                    file_name="stego_image.png",
                    mime="image/png",
                    type="primary",
                    use_container_width=True
                )
                
                if 'encryption_history' not in st.session_state:
                    st.session_state.encryption_history = []
                
                st.session_state.encryption_history.append({
                    'message_length': len(secret_message),
                    'encryption_time': encryption_result['encryption_time'],
                    'embedding_time': embedding_result['embedding_time'],
                    'psnr': psnr if psnr else 0,
                    'ssim': ssim if ssim else 0,
                    'dna_length': encryption_result['dna_length'],
                    'used_aes': use_aes
                })
                
                st.success("✅ Encryption and embedding completed successfully!")
                
            except Exception as e:
                st.error(f"❌ Error during processing: {str(e)}")
            finally:
                if temp_cover_path and os.path.exists(temp_cover_path):
                    try:
                        os.remove(temp_cover_path)
                    except:
                        pass
                if temp_stego_path and os.path.exists(temp_stego_path):
                    try:
                        os.remove(temp_stego_path)
                    except:
                        pass

st.markdown("---")
st.info("💡 **Tip**: Use high-quality images with sufficient resolution for better steganography results. The image should have enough pixels to accommodate your message.")
