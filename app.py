import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Network Intrusion Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Advanced Custom CSS for Modern UI
st.markdown("""
    <style>
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #f093fb;
        --dark-bg: #0f1419;
        --light-bg: #1a1f2e;
        --card-bg: #16213e;
        --text-primary: #e0e0e0;
        --text-secondary: #b0b0b0;
        --success-color: #10b981;
        --danger-color: #ef4444;
        --warning-color: #f59e0b;
    }
    
    * {
        margin: 0;
        padding: 0;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 50%, #16213e 100%);
        color: var(--text-primary);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16213e 0%, #0f1419 100%);
        border-right: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: var(--text-primary);
    }
    
    .main {
        background: transparent;
    }
    
    h1, h2, h3, h4, h5, h6 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
        height: 45px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
        box-shadow: 0 6px 25px rgba(240, 147, 251, 0.6);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(240, 147, 251, 0.5);
        box-shadow: 0 12px 48px rgba(240, 147, 251, 0.2);
        transform: translateY(-5px);
    }
    
    .card {
        background: linear-gradient(135deg, rgba(22, 33, 62, 0.8) 0%, rgba(15, 20, 25, 0.8) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        border-color: rgba(240, 147, 251, 0.4);
        box-shadow: 0 12px 48px rgba(240, 147, 251, 0.15);
    }
    
    [data-testid="stMetricDelta"] {
        color: var(--success-color);
    }
    
    .stMetric {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
        border-left: 4px solid var(--success-color);
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .danger-box {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
        border-left: 4px solid var(--danger-color);
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
        border-left: 4px solid var(--warning-color);
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 8px;
        color: var(--text-secondary);
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
    }
    
    .stSelectbox, .stNumberInput, .stFileUploader {
        background: rgba(22, 33, 62, 0.5);
        border-radius: 10px;
    }
    
    [data-testid="stForm"] {
        background: linear-gradient(135deg, rgba(22, 33, 62, 0.6) 0%, rgba(15, 20, 25, 0.6) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
    }
    
    .stRadio {
        background: rgba(22, 33, 62, 0.5);
        border-radius: 10px;
        padding: 10px;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 20px;
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .divider {
        border-top: 2px solid rgba(102, 126, 234, 0.2);
        margin: 20px 0;
    }
    
    .footer {
        text-align: center;
        color: var(--text-secondary);
        padding: 20px;
        border-top: 1px solid rgba(102, 126, 234, 0.2);
        margin-top: 40px;
    }
    
    a {
        color: #667eea;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    a:hover {
        color: #f093fb;
    }
    
    .stat-number {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .feature-label {
        color: #667eea;
        font-weight: 600;
        font-size: 13px;
        margin-bottom: 8px;
        display: block;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .input-container {
        margin-bottom: 15px;
    }
    
    </style>
    """, unsafe_allow_html=True)

# Load Assets
@st.cache_resource
def load_assets():
    model = joblib.load('rf_model.joblib')
    scaler = joblib.load('scaler.joblib')
    selector = joblib.load('selector.joblib')
    label_encoders = joblib.load('label_encoders.joblib')
    feature_names = joblib.load('feature_names.joblib')
    return model, scaler, selector, label_encoders, feature_names

model, scaler, selector, label_encoders, feature_names = load_assets()

# Sidebar Navigation
with st.sidebar:
    st.markdown('<div class="sidebar-header">🛡️ NIDS</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    page = st.radio(
        "📍 Navigation",
        ["🏠 Home", "📊 Analytics", "📈 Performance", "🔍 Detection"],
        label_visibility="collapsed"
    )
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.markdown("### 👤 Developer")
    st.markdown("""
    <div class="info-box">
    <b>Hafsa Ibrahim</b><br>
    AI/ML Engineer
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/hafsa-ibrahim-ai-mi/)")
    with col2:
        st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/HafsaIbrahim5)")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.markdown("### 📊 Quick Stats")
    data = pd.read_csv('Train_data.csv')
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("📈 Records", f"{len(data):,}")
    with col_b:
        st.metric("🔧 Features", data.shape[1] - 1)

# Home Page
if page == "🏠 Home":
    col_header = st.columns([1, 2])
    with col_header[0]:
        st.markdown('<div style="font-size: 60px; text-align: center;">🛡️</div>', unsafe_allow_html=True)
    with col_header[1]:
        st.markdown("# Network Intrusion Detection System")
        st.markdown("### Advanced ML-Based Network Security Solution")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎯 Project Overview")
        st.markdown("""
        <div class="card">
        This cutting-edge system leverages **Machine Learning** to detect network intrusions in real-time. 
        It analyzes network traffic patterns and classifies connections as:
        
        - ✅ **Normal**: Legitimate network traffic
        - 🚨 **Anomaly**: Potential network attacks or suspicious activity
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🚀 Key Capabilities")
        st.markdown("""
        <div class="card">
        - 🤖 Advanced Random Forest Classification
        - 📊 Real-time Traffic Analysis
        - 📁 Batch Prediction Support
        - 📈 Interactive Visualizations
        - 🎨 Modern UI/UX Design
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col_stats = st.columns(4)
    data = pd.read_csv('Train_data.csv')
    
    with col_stats[0]:
        st.markdown(f"""
        <div class="metric-card">
        <div style="text-align: center;">
        <div style="font-size: 12px; color: var(--text-secondary);">Total Records</div>
        <div class="stat-number">{len(data):,}</div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stats[1]:
        st.markdown(f"""
        <div class="metric-card">
        <div style="text-align: center;">
        <div style="font-size: 12px; color: var(--text-secondary);">Features</div>
        <div class="stat-number">{data.shape[1] - 1}</div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stats[2]:
        normal_count = len(data[data['class'] == 'normal'])
        st.markdown(f"""
        <div class="metric-card">
        <div style="text-align: center;">
        <div style="font-size: 12px; color: var(--text-secondary);">Normal Traffic</div>
        <div class="stat-number">{normal_count:,}</div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stats[3]:
        anomaly_count = len(data[data['class'] == 'anomaly'])
        st.markdown(f"""
        <div class="metric-card">
        <div style="text-align: center;">
        <div style="font-size: 12px; color: var(--text-secondary);">Anomalies</div>
        <div class="stat-number">{anomaly_count:,}</div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.markdown("### 📋 Dataset Preview")
    st.dataframe(data.head(10), use_container_width=True)

# Analytics Page
elif page == "📊 Analytics":
    st.markdown("# 📊 Exploratory Data Analysis")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    data = pd.read_csv('Train_data.csv')
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Distribution", "🔗 Correlations", "📈 Features", "📉 Statistics"])
    
    with tab1:
        st.markdown("### Class Distribution")
        class_counts = data['class'].value_counts()
        
        col_dist = st.columns([2, 1])
        with col_dist[0]:
            fig = px.pie(
                values=class_counts.values, 
                names=class_counts.index,
                title='Traffic Classification',
                color_discrete_sequence=['#10b981', '#ef4444'],
                hole=0.4
            )
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_dist[1]:
            st.markdown("""
            <div class="metric-card">
            <b>Normal Traffic</b><br>
            <div class="stat-number">53.4%</div>
            <div style="font-size: 12px; color: #10b981;">✅ Legitimate</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="metric-card">
            <b>Anomalies</b><br>
            <div class="stat-number">46.6%</div>
            <div style="font-size: 12px; color: #ef4444;">🚨 Attacks</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Feature Correlation Matrix")
        numeric_data = data.select_dtypes(include=[np.number])
        corr = numeric_data.corr()
        
        fig = px.imshow(
            corr,
            text_auto=".1f",
            aspect="auto",
            color_continuous_scale='RdBu_r',
            title="Correlation Heatmap"
        )
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Feature Distribution Analysis")
        feature = st.selectbox("Select Feature", numeric_data.columns, label_visibility="collapsed")
        
        fig = px.histogram(
            data,
            x=feature,
            color="class",
            marginal="box",
            title=f"Distribution of {feature}",
            color_discrete_map={'normal': '#667eea', 'anomaly': '#f093fb'}
        )
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### Statistical Summary")
        st.dataframe(data.describe(), use_container_width=True)

# Performance Page
elif page == "📈 Performance":
    st.markdown("# 📈 Model Performance Metrics")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    data = pd.read_csv('Train_data.csv')
    data.rename(columns={'class': 'Class'}, inplace=True)
    
    for col, le in label_encoders.items():
        data[col] = le.transform(data[col])
    
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    X_scaled = scaler.transform(X)
    X_selected = selector.transform(X_scaled)
    
    from sklearn.model_selection import train_test_split
    _, X_test, _, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)
    
    y_pred = model.predict(X_test)
    
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <div style="font-size: 12px; color: var(--text-secondary);">Accuracy</div>
        <div class="stat-number">{acc:.2%}</div>
        <div style="font-size: 11px; color: #10b981;">✅ Excellent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <div style="font-size: 12px; color: var(--text-secondary);">Precision</div>
        <div class="stat-number">{prec:.2%}</div>
        <div style="font-size: 11px; color: #667eea;">High Reliability</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <div style="font-size: 12px; color: var(--text-secondary);">Recall</div>
        <div class="stat-number">{rec:.2%}</div>
        <div style="font-size: 11px; color: #764ba2;">Detection Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
        <div style="font-size: 12px; color: var(--text-secondary);">F1 Score</div>
        <div class="stat-number">{f1:.2%}</div>
        <div style="font-size: 11px; color: #f093fb;">Balanced</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### Confusion Matrix")
        cm = confusion_matrix(y_test, y_pred)
        fig = px.imshow(
            cm,
            text_auto=True,
            labels=dict(x="Predicted", y="Actual"),
            x=['Anomaly', 'Normal'],
            y=['Anomaly', 'Normal'],
            color_continuous_scale='Blues',
            title="Confusion Matrix"
        )
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col_b:
        st.markdown("### Classification Report")
        report = classification_report(y_test, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        st.dataframe(report_df.style.background_gradient(cmap='Blues'), use_container_width=True)

# Detection Page
elif page == "🔍 Detection":
    st.markdown("# 🔍 Real-time Intrusion Detection")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    mode = st.radio("Choose Detection Mode", ["🎯 Single Analysis", "📁 Batch Processing"], horizontal=True, label_visibility="collapsed")
    
    if mode == "🎯 Single Analysis":
        st.markdown("### Analyze Individual Connection")
        st.markdown("**Enter the network connection parameters below:**")
        
        with st.form("prediction_form", border=False):
            cols = st.columns(3)
            input_data = {}
            
            for i, feat in enumerate(feature_names):
                with cols[i % 3]:
                    st.markdown(f'<span class="feature-label">{feat}</span>', unsafe_allow_html=True)
                    if feat in label_encoders:
                        options = label_encoders[feat].classes_.tolist()
                        input_data[feat] = st.selectbox(
                            f"Select {feat}",
                            options,
                            key=f"select_{feat}",
                            label_visibility="collapsed"
                        )
                    else:
                        input_data[feat] = st.number_input(
                            f"Enter {feat}",
                            value=0.0,
                            key=f"number_{feat}",
                            label_visibility="collapsed"
                        )
            
            submit = st.form_submit_button("🔍 Analyze Traffic", use_container_width=True)
        
        if submit:
            df_input = pd.DataFrame([input_data])
            
            for col, le in label_encoders.items():
                if col in df_input.columns:
                    df_input[col] = le.transform(df_input[col])
            
            X_in_scaled = scaler.transform(df_input)
            X_in_selected = selector.transform(X_in_scaled)
            
            prediction = model.predict(X_in_selected)[0]
            prob = model.predict_proba(X_in_selected)[0]
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            if prediction == 1:
                st.markdown("""
                <div class="success-box">
                <h3>✅ NORMAL TRAFFIC DETECTED</h3>
                <p>This connection appears to be legitimate and safe.</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_result = st.columns(2)
                with col_result[0]:
                    st.markdown(f"""
                    <div class="metric-card">
                    <div style="text-align: center;">
                    <div style="font-size: 12px; color: var(--text-secondary);">Confidence Level</div>
                    <div class="stat-number">{prob[1]:.1%}</div>
                    </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_result[1]:
                    st.markdown(f"""
                    <div class="metric-card">
                    <div style="text-align: center;">
                    <div style="font-size: 12px; color: var(--text-secondary);">Risk Level</div>
                    <div style="font-size: 24px; color: #10b981;">🟢 LOW</div>
                    </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.balloons()
            else:
                st.markdown("""
                <div class="danger-box">
                <h3>🚨 INTRUSION ALERT!</h3>
                <p>This connection shows suspicious patterns consistent with a network attack.</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_result = st.columns(2)
                with col_result[0]:
                    st.markdown(f"""
                    <div class="metric-card">
                    <div style="text-align: center;">
                    <div style="font-size: 12px; color: var(--text-secondary);">Confidence Level</div>
                    <div class="stat-number">{prob[0]:.1%}</div>
                    </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_result[1]:
                    st.markdown(f"""
                    <div class="metric-card">
                    <div style="text-align: center;">
                    <div style="font-size: 12px; color: var(--text-secondary);">Risk Level</div>
                    <div style="font-size: 24px; color: #ef4444;">🔴 HIGH</div>
                    </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.warning("⚠️ Immediate action recommended. Review connection details and block if necessary.")
    
    else:
        st.markdown("### Batch Traffic Analysis")
        uploaded_file = st.file_uploader("📤 Upload CSV File", type="csv", label_visibility="collapsed")
        
        if uploaded_file is not None:
            test_df = pd.read_csv(uploaded_file)
            st.markdown("**Preview of Uploaded Data:**")
            st.dataframe(test_df.head(), use_container_width=True)
            
            if st.button("🚀 Process Batch", use_container_width=True):
                try:
                    process_df = test_df.copy()
                    for col, le in label_encoders.items():
                        if col in process_df.columns and col != 'Class':
                            process_df[col] = process_df[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else 0)
                    
                    for feat in feature_names:
                        if feat not in process_df.columns:
                            process_df[feat] = 0
                    
                    process_df = process_df[feature_names]
                    
                    X_batch_scaled = scaler.transform(process_df)
                    X_batch_selected = selector.transform(X_batch_scaled)
                    
                    predictions = model.predict(X_batch_scaled)
                    test_df['Prediction'] = ['Normal' if p == 1 else 'Anomaly' for p in predictions]
                    
                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                    st.markdown("### Results")
                    st.dataframe(test_df, use_container_width=True)
                    
                    csv = test_df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download Results", csv, "predictions.csv", "text/csv", use_container_width=True)
                    
                    normal_count = (test_df['Prediction'] == 'Normal').sum()
                    anomaly_count = (test_df['Prediction'] == 'Anomaly').sum()
                    
                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                    st.markdown("### Summary")
                    
                    col_summary = st.columns(3)
                    with col_summary[0]:
                        st.markdown(f"""
                        <div class="metric-card">
                        <div style="text-align: center;">
                        <div style="font-size: 12px; color: var(--text-secondary);">Total Records</div>
                        <div class="stat-number">{len(test_df)}</div>
                        </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_summary[1]:
                        st.markdown(f"""
                        <div class="metric-card">
                        <div style="text-align: center;">
                        <div style="font-size: 12px; color: var(--text-secondary);">Normal</div>
                        <div class="stat-number" style="color: #10b981;">{normal_count}</div>
                        </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_summary[2]:
                        st.markdown(f"""
                        <div class="metric-card">
                        <div style="text-align: center;">
                        <div style="font-size: 12px; color: var(--text-secondary);">Anomalies</div>
                        <div class="stat-number" style="color: #ef4444;">{anomaly_count}</div>
                        </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    fig = px.bar(
                        x=['Normal', 'Anomaly'],
                        y=[normal_count, anomaly_count],
                        color=['Normal', 'Anomaly'],
                        color_discrete_map={'Normal': '#10b981', 'Anomaly': '#ef4444'},
                        title="Batch Prediction Summary"
                    )
                    fig.update_layout(
                        template='plotly_dark',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e0e0e0'),
                        height=400,
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                except Exception as e:
                    st.error(f"❌ Error processing file: {e}")

# Footer
st.markdown("""
<div class="footer">
<p>🛡️ <b>Network Intrusion Detection System</b></p>
<p>© 2026 | Developed by <b>Hafsa Ibrahim</b></p>
<p>
<a href="https://www.linkedin.com/in/hafsa-ibrahim-ai-mi/">LinkedIn</a> • 
<a href="https://github.com/HafsaIbrahim5">GitHub</a>
</p>
<p style="font-size: 12px; color: var(--text-secondary);">Built with ❤️ using Python, Streamlit & Machine Learning</p>
</div>
""", unsafe_allow_html=True)
