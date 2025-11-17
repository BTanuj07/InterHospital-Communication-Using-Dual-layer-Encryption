import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.title("📊 Analytics Dashboard")
st.markdown("### Performance Metrics and System Statistics")

st.markdown("---")

if 'encryption_history' not in st.session_state:
    st.session_state.encryption_history = []

if 'decryption_history' not in st.session_state:
    st.session_state.decryption_history = []

if len(st.session_state.encryption_history) > 0 or len(st.session_state.decryption_history) > 0:
    
    tabs = st.tabs(["📈 Encryption Metrics", "📉 Decryption Metrics", "🔬 Quality Analysis", "⚡ Performance"])
    
    with tabs[0]:
        st.subheader("Encryption & Embedding Statistics")
        
        if len(st.session_state.encryption_history) > 0:
            enc_df = pd.DataFrame(st.session_state.encryption_history)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Operations", len(st.session_state.encryption_history))
            with col2:
                st.metric("Avg Encryption Time", f"{enc_df['encryption_time'].mean():.4f}s")
            with col3:
                st.metric("Avg Embedding Time", f"{enc_df['embedding_time'].mean():.4f}s")
            with col4:
                st.metric("Avg Message Length", f"{enc_df['message_length'].mean():.0f} chars")
            
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(
                y=enc_df['encryption_time'],
                mode='lines+markers',
                name='Encryption Time',
                line=dict(color='#FF6B6B')
            ))
            fig_time.add_trace(go.Scatter(
                y=enc_df['embedding_time'],
                mode='lines+markers',
                name='Embedding Time',
                line=dict(color='#4ECDC4')
            ))
            fig_time.update_layout(
                title="Processing Time Over Operations",
                xaxis_title="Operation Number",
                yaxis_title="Time (seconds)",
                hovermode='x unified'
            )
            st.plotly_chart(fig_time, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_msg = px.bar(
                    enc_df,
                    y='message_length',
                    title="Message Lengths",
                    labels={'message_length': 'Characters', 'index': 'Operation'},
                    color='message_length',
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig_msg, use_container_width=True)
            
            with col2:
                fig_dna = px.bar(
                    enc_df,
                    y='dna_length',
                    title="DNA Sequence Lengths",
                    labels={'dna_length': 'DNA Bases', 'index': 'Operation'},
                    color='dna_length',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_dna, use_container_width=True)
            
        else:
            st.info("📝 No encryption operations recorded yet. Use the Encrypt & Embed page to generate data.")
    
    with tabs[1]:
        st.subheader("Decryption & Extraction Statistics")
        
        if len(st.session_state.decryption_history) > 0:
            dec_df = pd.DataFrame(st.session_state.decryption_history)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Operations", len(st.session_state.decryption_history))
            with col2:
                st.metric("Avg Extraction Time", f"{dec_df['extraction_time'].mean():.4f}s")
            with col3:
                st.metric("Avg Decryption Time", f"{dec_df['decryption_time'].mean():.4f}s")
            with col4:
                st.metric("Avg Total Time", f"{dec_df['total_time'].mean():.4f}s")
            
            fig_dec = go.Figure()
            fig_dec.add_trace(go.Bar(
                y=dec_df['extraction_time'],
                name='Extraction Time',
                marker_color='#95E1D3'
            ))
            fig_dec.add_trace(go.Bar(
                y=dec_df['decryption_time'],
                name='Decryption Time',
                marker_color='#F38181'
            ))
            fig_dec.update_layout(
                title="Decryption Process Breakdown",
                xaxis_title="Operation Number",
                yaxis_title="Time (seconds)",
                barmode='stack'
            )
            st.plotly_chart(fig_dec, use_container_width=True)
            
            fig_total = px.line(
                dec_df,
                y='total_time',
                title="Total Processing Time Trend",
                labels={'total_time': 'Time (seconds)', 'index': 'Operation'},
                markers=True
            )
            st.plotly_chart(fig_total, use_container_width=True)
            
        else:
            st.info("📝 No decryption operations recorded yet. Use the Extract & Decrypt page to generate data.")
    
    with tabs[2]:
        st.subheader("Image Quality Metrics")
        
        if len(st.session_state.encryption_history) > 0:
            enc_df = pd.DataFrame(st.session_state.encryption_history)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Avg PSNR", f"{enc_df['psnr'].mean():.2f} dB", 
                         help="Peak Signal-to-Noise Ratio - Higher is better")
            with col2:
                st.metric("Avg SSIM", f"{enc_df['ssim'].mean():.4f}",
                         help="Structural Similarity Index - Closer to 1.0 is better")
            
            fig_psnr = go.Figure()
            fig_psnr.add_trace(go.Scatter(
                y=enc_df['psnr'],
                mode='lines+markers',
                name='PSNR',
                fill='tozeroy',
                line=dict(color='#6C5CE7', width=3)
            ))
            fig_psnr.add_hline(y=40, line_dash="dash", line_color="green", 
                              annotation_text="Excellent (>40 dB)")
            fig_psnr.add_hline(y=30, line_dash="dash", line_color="orange",
                              annotation_text="Good (>30 dB)")
            fig_psnr.update_layout(
                title="PSNR Values Across Operations",
                xaxis_title="Operation Number",
                yaxis_title="PSNR (dB)"
            )
            st.plotly_chart(fig_psnr, use_container_width=True)
            
            fig_ssim = go.Figure()
            fig_ssim.add_trace(go.Scatter(
                y=enc_df['ssim'],
                mode='lines+markers',
                name='SSIM',
                fill='tozeroy',
                line=dict(color='#00B894', width=3)
            ))
            fig_ssim.update_layout(
                title="SSIM Values Across Operations",
                xaxis_title="Operation Number",
                yaxis_title="SSIM (0-1)"
            )
            st.plotly_chart(fig_ssim, use_container_width=True)
            
            st.markdown("#### Quality Interpretation")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **PSNR (Peak Signal-to-Noise Ratio)**
                - > 40 dB: Excellent quality
                - 30-40 dB: Good quality
                - < 30 dB: Noticeable degradation
                """)
            with col2:
                st.markdown("""
                **SSIM (Structural Similarity Index)**
                - > 0.95: Excellent similarity
                - 0.90-0.95: Good similarity
                - < 0.90: Noticeable differences
                """)
        else:
            st.info("📝 No quality metrics available. Perform encryption operations to generate quality data.")
    
    with tabs[3]:
        st.subheader("Performance Comparison")
        
        if len(st.session_state.encryption_history) > 0 and len(st.session_state.decryption_history) > 0:
            enc_df = pd.DataFrame(st.session_state.encryption_history)
            dec_df = pd.DataFrame(st.session_state.decryption_history)
            
            avg_enc_total = (enc_df['encryption_time'] + enc_df['embedding_time']).mean()
            avg_dec_total = dec_df['total_time'].mean()
            
            fig_compare = go.Figure(data=[
                go.Bar(name='Encryption + Embedding', x=['Average Time'], y=[avg_enc_total], marker_color='#FF6B6B'),
                go.Bar(name='Extraction + Decryption', x=['Average Time'], y=[avg_dec_total], marker_color='#4ECDC4')
            ])
            fig_compare.update_layout(
                title="Encryption vs Decryption Performance",
                yaxis_title="Time (seconds)",
                barmode='group'
            )
            st.plotly_chart(fig_compare, use_container_width=True)
            
            efficiency_data = {
                'Process': ['Encryption', 'Embedding', 'Extraction', 'Decryption'],
                'Avg Time (ms)': [
                    enc_df['encryption_time'].mean() * 1000,
                    enc_df['embedding_time'].mean() * 1000,
                    dec_df['extraction_time'].mean() * 1000,
                    dec_df['decryption_time'].mean() * 1000
                ]
            }
            efficiency_df = pd.DataFrame(efficiency_data)
            
            fig_pie = px.pie(
                efficiency_df,
                values='Avg Time (ms)',
                names='Process',
                title='Time Distribution Across Processes'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        else:
            st.info("📝 Perform both encryption and decryption operations to see performance comparisons.")
    
    st.markdown("---")
    
    if st.button("🗑️ Clear All Analytics Data", type="secondary"):
        st.session_state.encryption_history = []
        st.session_state.decryption_history = []
        st.rerun()

else:
    st.info("📊 No analytics data available yet")
    
    st.markdown("""
    ### 🚀 Get Started
    
    Analytics will be automatically generated as you use the system:
    
    1. **Encrypt & Embed** - Create stego-images to generate encryption metrics
    2. **Extract & Decrypt** - Process stego-images to generate decryption metrics
    3. **Return here** - View comprehensive analytics and performance data
    
    ---
    
    ### 📈 Available Metrics
    
    **Encryption Metrics:**
    - Processing time (encryption + embedding)
    - Message and DNA sequence lengths
    - PSNR and SSIM quality metrics
    
    **Decryption Metrics:**
    - Extraction and decryption times
    - Total processing time
    - Success rates
    
    **Quality Analysis:**
    - Image quality preservation (PSNR)
    - Structural similarity (SSIM)
    - Visual degradation assessment
    
    **Performance:**
    - Process-by-process breakdown
    - Comparative analysis
    - Efficiency trends
    """)
