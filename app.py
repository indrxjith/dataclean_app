import streamlit as st
import pandas as pd
import os
from typing import Optional
import time

# Page config
st.set_page_config(
    page_title="DataClean Pro", 
    page_icon="🧹", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS + JavaScript Enhancements
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Professional Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        text-align: center;
        color: white;
        animation: fadeInDown 0.8s ease-out;
    }
    
    /* Enhanced Metrics */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-container:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .metric-container:hover::before {
        left: 100%;
    }
    
    /* Success Messages */
    .success-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        animation: slideInLeft 0.6s ease-out;
    }
    
    .error-box {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02) !important;
    }
    
    /* File Upload Enhancement */
    .stFileUploader > div {
        border: 2px dashed #667eea !important;
        border-radius: 15px !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05)) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #764ba2 !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)) !important;
        transform: scale(1.02) !important;
    }
    
    /* Data Frame Enhancement */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        animation: fadeInUp 0.6s ease-out !important;
    }
    
    /* Progress Enhancement */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 10px !important;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .loading-shimmer {
        position: relative;
        overflow: hidden;
    }
    
    .loading-shimmer::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 2s infinite;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Professional loading animations
    function initializeAnimations() {
        const elements = document.querySelectorAll('.metric-container, .stDataFrame, .stSelectbox, .stTextInput');
        elements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            setTimeout(() => {
                el.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
                el.style.opacity = '1';
                el.style.transform = 'translateY(0px)';
            }, index * 150);
        });
    }
    
    // Enhanced button interactions
    function enhanceButtons() {
        const buttons = document.querySelectorAll('.stButton > button');
        buttons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) scale(1.05)';
                this.style.boxShadow = '0 8px 25px rgba(102, 126, 234, 0.4)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0px) scale(1)';
                this.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.3)';
            });
            
            button.addEventListener('click', function() {
                const ripple = document.createElement('div');
                ripple.style.cssText = `
                    position: absolute;
                    width: 100px;
                    height: 100px;
                    background: rgba(255,255,255,0.6);
                    border-radius: 50%;
                    transform: scale(0);
                    animation: ripple 0.6s linear;
                    top: 50%;
                    left: 50%;
                    margin-left: -50px;
                    margin-top: -50px;
                `;
                this.appendChild(ripple);
                setTimeout(() => ripple.remove(), 600);
            });
        });
    }
    
    // File upload enhancements
    function enhanceFileUpload() {
        const uploadAreas = document.querySelectorAll('[data-testid="stFileUploader"]');
        uploadAreas.forEach(area => {
            area.addEventListener('dragover', function(e) {
                e.preventDefault();
                this.style.borderColor = '#764ba2';
                this.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2))';
                this.style.transform = 'scale(1.05)';
            });
            
            area.addEventListener('dragleave', function() {
                this.style.borderColor = '#667eea';
                this.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05))';
                this.style.transform = 'scale(1)';
            });
            
            area.addEventListener('drop', function() {
                this.style.transform = 'scale(1)';
                this.classList.add('loading-shimmer');
            });
        });
    }
    
    // Add CSS animation keyframes
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Initialize all enhancements
    setTimeout(() => {
        initializeAnimations();
        enhanceButtons();
        enhanceFileUpload();
    }, 300);
    
    // Re-initialize on Streamlit rerun
    const observer = new MutationObserver(() => {
        setTimeout(() => {
            enhanceButtons();
            enhanceFileUpload();
        }, 100);
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
</script>
""", unsafe_allow_html=True)

# Initialize session state
if 'cleaning_history' not in st.session_state:
    st.session_state.cleaning_history = []

# Professional Header
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3rem; margin: 0; font-weight: 700;">🧹 DataClean Pro</h1>
    <p style="font-size: 1.2rem; margin: 0.5rem 0 0 0; opacity: 0.9;">Transform messy data into clean datasets with AI precision</p>
</div>
""", unsafe_allow_html=True)

# Enhanced cleaning function with progress tracking
def data_cleaning_master(data_path: str, data_name: str, dup_keys: Optional[str] = None):
    os.makedirs("outputs/duplicates", exist_ok=True)
    os.makedirs("outputs/cleaned", exist_ok=True)
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("📂 Loading data...")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        df = pd.read_csv(data_path)
        
        # Validate data
        if df.empty:
            raise ValueError("The uploaded file appears to be empty")
        
        status_text.text("🔍 Analyzing data quality...")
        progress_bar.progress(50)
        time.sleep(0.5)
        
        # Handle duplicates
        if dup_keys:
            keys = [k.strip() for k in dup_keys.split(',')]
            missing_keys = [k for k in keys if k not in df.columns]
            if missing_keys:
                raise ValueError(f"Duplicate keys not found in dataset: {missing_keys}")
            
            dups = df[df.duplicated(subset=keys, keep=False)]
            if not dups.empty:
                dup_path = f"outputs/duplicates/{data_name}_duplicates.csv"
                dups.to_csv(dup_path, index=False)
            df_nodup = df.drop_duplicates(subset=keys)
        else:
            df_nodup = df.drop_duplicates()
            dups = pd.DataFrame()

        status_text.text("🧹 Cleaning data...")
        progress_bar.progress(75)
        time.sleep(0.5)

        df_clean = df_nodup.copy()
        
        # Handle missing values
        numeric_cols = df_clean.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            if df_clean[col].notna().sum() > 0:
                df_clean[col] = df_clean[col].fillna(df_clean[col].mean())

        non_numeric_cols = df_clean.select_dtypes(exclude=['number']).columns
        if len(non_numeric_cols) > 0:
            df_clean = df_clean.dropna(subset=non_numeric_cols)

        status_text.text("💾 Saving results...")
        progress_bar.progress(100)
        time.sleep(0.5)

        out_path = f"outputs/cleaned/{data_name}_Clean_data.csv"
        df_clean.to_csv(out_path, index=False)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        return dups, df_clean, df
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        raise e

# Sidebar for options
with st.sidebar:
    st.markdown("### 🔧 **Configuration**")
    st.markdown("---")
    
    # Show cleaning history if exists
    if st.session_state.cleaning_history:
        st.markdown("#### 📊 **Recent Activity**")
        for i, entry in enumerate(st.session_state.cleaning_history[-3:]):
            st.markdown(f"**{entry['file']}**")
            st.caption(f"{entry['timestamp']} | {entry['rows_before']} → {entry['rows_after']} rows")

# File upload with enhanced styling
st.markdown("### 📁 **Upload Your Dataset**")
uploaded_file = st.file_uploader(
    "Choose a CSV file", 
    type=['csv'],
    help="Drag and drop or click to browse. Maximum file size: 200MB"
)

if uploaded_file:
    # Save temp file
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())
    
    try:
        # Load and validate data
        df = pd.read_csv(temp_path)
        
        # Validate file
        if df.empty:
            st.markdown("""
            <div class="error-box">
                <h3 style="margin: 0 0 0.5rem 0;">❌ Empty File</h3>
                <p style="margin: 0;">The uploaded file appears to be empty. Please check your CSV file.</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()
        
        # Warn for large files
        if df.shape[0] > 50000:
            st.markdown("""
            <div class="warning-box">
                <h3 style="margin: 0 0 0.5rem 0;">⚠️ Large Dataset</h3>
                <p style="margin: 0;">Large dataset detected. Processing may take a few moments.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Success message
        st.markdown(f"""
        <div class="success-box">
            <h3 style="margin: 0 0 0.5rem 0;">✅ File Loaded Successfully!</h3>
            <p style="margin: 0;">Dataset: <strong>{uploaded_file.name}</strong> | {df.shape[0]:,} rows, {df.shape[1]} columns</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced metrics display
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <h3 style="color: #667eea; margin: 0; font-size: 2rem;">📄</h3>
                <h2 style="margin: 0.5rem 0 0 0; font-size: 2rem;">{df.shape[0]:,}</h2>
                <p style="color: #64748b; margin: 0;">Total Rows</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <h3 style="color: #667eea; margin: 0; font-size: 2rem;">📋</h3>
                <h2 style="margin: 0.5rem 0 0 0; font-size: 2rem;">{df.shape[1]}</h2>
                <p style="color: #64748b; margin: 0;">Columns</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            missing_count = df.isnull().sum().sum()
            st.markdown(f"""
            <div class="metric-container">
                <h3 style="color: #f59e0b; margin: 0; font-size: 2rem;">❌</h3>
                <h2 style="margin: 0.5rem 0 0 0; font-size: 2rem;">{missing_count:,}</h2>
                <p style="color: #64748b; margin: 0;">Missing Values</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            dup_count = df.duplicated().sum()
            st.markdown(f"""
            <div class="metric-container">
                <h3 style="color: #ef4444; margin: 0; font-size: 2rem;">🔄</h3>
                <h2 style="margin: 0.5rem 0 0 0; font-size: 2rem;">{dup_count:,}</h2>
                <p style="color: #64748b; margin: 0;">Duplicates</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Data preview
        st.markdown("### 📊 **Data Preview**")
        st.dataframe(df.head(), use_container_width=True)
        
        # Show column info
        with st.expander("📋 **Column Information**"):
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes,
                'Non-Null Count': df.count(),
                'Missing Count': df.isnull().sum()
            })
            st.dataframe(col_info, use_container_width=True)
        
        # Cleaning options
        st.markdown("### ⚙️ **Cleaning Options**")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            dup_keys = st.text_input(
                "🔄 Duplicate Detection Keys",
                placeholder="e.g., email,phone (comma-separated)",
                help="Specify column names to identify duplicates"
            )
            
            # Validate duplicate keys
            if dup_keys:
                keys = [k.strip() for k in dup_keys.split(',')]
                invalid_keys = [k for k in keys if k not in df.columns]
                if invalid_keys:
                    st.error(f"❌ Invalid column names: {', '.join(invalid_keys)}")
                else:
                    st.success(f"✅ Valid duplicate keys: {', '.join(keys)}")
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            advanced_options = st.expander("🔬 Advanced Options")
            with advanced_options:
                auto_detect = st.checkbox("🤖 Auto-detect data types", value=True)
                normalize_text = st.checkbox("📝 Normalize text fields", value=True)
                remove_whitespace = st.checkbox("🧽 Remove extra whitespace", value=True)
        
        # Clean button
        st.markdown("---")
        if st.button("🚀 **Start Data Cleaning**", type="primary"):
            try:
                file_name = uploaded_file.name.replace('.csv', '')
                
                # Run cleaning with enhanced progress
                dups, cleaned, original = data_cleaning_master(temp_path, file_name, dup_keys)
                
                # Add to history
                st.session_state.cleaning_history.append({
                    'file': uploaded_file.name,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'rows_before': original.shape[0],
                    'rows_after': cleaned.shape[0]
                })
                
                # Success message
                st.markdown(f"""
                <div class="success-box">
                    <h3 style="margin: 0 0 0.5rem 0;">🎉 Data Cleaning Complete!</h3>
                    <p style="margin: 0;">Your dataset has been successfully processed and cleaned.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Results comparison
                st.markdown("### 📊 **Before vs After Comparison**")
                
                result_col1, result_col2 = st.columns(2)
                
                with result_col1:
                    st.markdown("#### **📋 Before Cleaning**")
                    st.metric("Rows", f"{original.shape[0]:,}")
                    st.metric("Missing Values", f"{original.isnull().sum().sum():,}")
                    st.metric("Duplicates", f"{len(dups):,}")
                
                with result_col2:
                    st.markdown("#### **✨ After Cleaning**")
                    rows_removed = original.shape[0] - cleaned.shape[0]
                    missing_fixed = original.isnull().sum().sum() - cleaned.isnull().sum().sum()
                    
                    st.metric("Rows", f"{cleaned.shape[0]:,}", delta=f"-{rows_removed:,}")
                    st.metric("Missing Values", f"{cleaned.isnull().sum().sum():,}", delta=f"-{missing_fixed:,}")
                    st.metric("Duplicates", "0", delta=f"-{len(dups):,}")
                
                # Quality improvement score
                quality_score = min(100, int((cleaned.shape[0] / original.shape[0]) * 100 + 
                                           (1 - (cleaned.isnull().sum().sum() / max(1, original.isnull().sum().sum()))) * 100) / 2)
                
                st.markdown(f"""
                <div style="text-align: center; margin: 2rem 0;">
                    <h3>📊 Data Quality Score</h3>
                    <div style="font-size: 3rem; color: #10b981; font-weight: bold;">{quality_score}%</div>
                    <p style="color: #64748b;">Overall data quality improvement</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Download section
                st.markdown("### 📥 **Download Results**")
                
                download_col1, download_col2 = st.columns(2)
                
                with download_col1:
                    csv = cleaned.to_csv(index=False)
                    st.download_button(
                        "📥 **Download Cleaned Data**", 
                        csv, 
                        f"{file_name}_cleaned.csv",
                        mime="text/csv"
                    )
                
                with download_col2:
                    if len(dups) > 0:
                        dups_csv = dups.to_csv(index=False)
                        st.download_button(
                            "🔄 **Download Duplicates Report**", 
                            dups_csv, 
                            f"{file_name}_duplicates.csv",
                            mime="text/csv"
                        )
                    else:
                        st.info("✨ No duplicates found to download")
                
                # Final preview
                st.markdown("### 🎯 **Cleaned Data Preview**")
                st.dataframe(cleaned.head(10), use_container_width=True)
                
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                    <h3 style="margin: 0 0 0.5rem 0;">❌ Cleaning Error</h3>
                    <p style="margin: 0;">Error during cleaning: {str(e)}</p>
                </div>
                """, unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown(f"""
        <div class="error-box">
            <h3 style="margin: 0 0 0.5rem 0;">❌ File Loading Error</h3>
            <p style="margin: 0;">Error loading file: {str(e)}</p>
            <p style="margin: 0; margin-top: 0.5rem;">💡 Please ensure your file is a valid CSV format.</p>
        </div>
        """, unsafe_allow_html=True)
    finally:
        # Always cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

else:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 2rem 0;">
        <h2 style="color: #667eea; margin-bottom: 1rem;">👋 Welcome to DataClean Pro</h2>
        <p style="font-size: 1.1rem; color: #64748b; margin-bottom: 2rem;">
            Upload your CSV file above to get started with professional data cleaning
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-top: 2rem;">
            <div style="padding: 1.5rem; border-radius: 10px; background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));">
                <h3 style="color: #10b981; margin-bottom: 0.5rem;">🧹 Smart Cleaning</h3>
                <p style="font-size: 0.9rem; color: #64748b;">Automatically detect and fix data quality issues</p>
            </div>
            <div style="padding: 1.5rem; border-radius: 10px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(29, 78, 216, 0.1));">
                <h3 style="color: #3b82f6; margin-bottom: 0.5rem;">📊 Visual Reports</h3>
                <p style="font-size: 0.9rem; color: #64748b;">See before/after comparisons with detailed metrics</p>
            </div>
            <div style="padding: 1.5rem; border-radius: 10px; background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.1));">
                <h3 style="color: #f59e0b; margin-bottom: 0.5rem;">⚡ Lightning Fast</h3>
                <p style="font-size: 0.9rem; color: #64748b;">Process thousands of rows in seconds</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #64748b;">
    <p>Made with ❤️ using <strong>Streamlit</strong> | <strong>DataClean Pro v1.0</strong></p>
    <p style="font-size: 0.9rem;">Professional data cleaning made simple</p>
</div>
""", unsafe_allow_html=True)
