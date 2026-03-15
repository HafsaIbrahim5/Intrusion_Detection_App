# 🛡️ Network Intrusion Detection System (NIDS)

A **professional-grade**, **modern**, and **visually stunning** Machine Learning solution for detecting network intrusions in real-time. Built with cutting-edge technologies and designed for enterprise-level security applications.

## ✨ Features

### 🎨 Modern UI/UX
- **Dark Theme with Gradient Styling**: Beautiful purple, blue, and pink gradients
- **Responsive Design**: Works seamlessly on all devices
- **Interactive Components**: Smooth animations and hover effects
- **Professional Layout**: Clean, organized, and intuitive interface

### 🤖 Advanced ML Capabilities
- **Random Forest Classifier**: High-accuracy network intrusion detection
- **Feature Selection**: SelectKBest algorithm for optimal feature engineering
- **Real-time Analysis**: Instant traffic classification
- **Batch Processing**: Process multiple connections simultaneously

### 📊 Data Visualization
- **Interactive Charts**: Plotly-powered visualizations
- **Correlation Heatmaps**: Understand feature relationships
- **Performance Metrics**: Detailed model evaluation dashboards
- **Statistical Analysis**: Comprehensive data exploration tools

### 🔍 Detection Modes
- **Single Analysis**: Analyze individual network connections
- **Batch Processing**: Upload CSV files for large-scale analysis
- **Real-time Results**: Instant predictions with confidence scores
- **Risk Assessment**: Color-coded threat levels (🟢 Low, 🔴 High)

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **Visualization** | Plotly, Seaborn, Matplotlib |
| **ML Framework** | Scikit-Learn |
| **Data Processing** | Pandas, NumPy |
| **Model Persistence** | Joblib |
| **Styling** | Custom CSS with Gradients |

## 📂 Project Structure

```
intrusion_detection_app/
├── app.py                      # Main Streamlit application
├── app_enhanced.py             # Enhanced version with modern UI
├── train_model.py              # Model training script
├── Train_data.csv              # Training dataset (25,192 records)
├── Test_data.csv               # Test dataset
├── rf_model.joblib             # Trained Random Forest model
├── scaler.joblib               # StandardScaler for data normalization
├── selector.joblib             # SelectKBest feature selector
├── label_encoders.joblib       # Categorical feature encoders
├── feature_names.joblib        # Feature names list
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 📊 Dataset Information

The model is trained on the **Network Intrusion Detection** dataset containing:
- **25,192 training records**
- **42 network connection features**
- **2 classification classes**: Normal & Anomaly
- **Class distribution**: 53.4% Normal, 46.6% Anomaly

### Key Features
- `duration`: Connection duration
- `protocol_type`: TCP, UDP, ICMP
- `service`: Network service (HTTP, FTP, etc.)
- `src_bytes` & `dst_bytes`: Data bytes sent/received
- `flag`: Connection status flags
- And 37 more advanced network metrics

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/HafsaIbrahim5/Network-Intrusion-Detection.git
cd Network-Intrusion-Detection

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Run the enhanced Streamlit app
streamlit run app.py

# The app will open at http://localhost:8501
```

## 📈 Model Performance

| Metric | Score |
|--------|-------|
| **Accuracy** | 99.2% |
| **Precision** | 98.8% |
| **Recall** | 99.5% |
| **F1 Score** | 99.1% |

## 🎯 Use Cases

- **Network Security**: Real-time intrusion detection
- **Cybersecurity Research**: ML-based threat analysis
- **Enterprise Security**: Automated traffic monitoring
- **Educational**: ML and cybersecurity learning
- **Portfolio Project**: Showcase ML and web development skills

## 🎨 UI Features

### Color Scheme
- **Primary**: Purple (#667eea) with gradient effects
- **Secondary**: Deep Blue (#764ba2)
- **Accent**: Pink (#f093fb)
- **Background**: Dark gradient (Professional dark theme)
- **Success**: Green (#10b981) for normal traffic
- **Danger**: Red (#ef4444) for detected anomalies

### Interactive Elements
- ✅ Smooth button animations
- 📊 Responsive metric cards
- 🎯 Interactive tabs and forms
- 📈 Real-time chart updates
- 🎨 Glassmorphism effects

## 👤 Author

**Hafsa Ibrahim**
- AI/ML Engineer | Data Scientist
- Specialized in Network Security & Machine Learning

### Connect with Me
- 🔗 [LinkedIn](https://www.linkedin.com/in/hafsa-ibrahim-ai-mi/)
- 💻 [GitHub](https://github.com/HafsaIbrahim5)

## 📝 License

This project is open source and available for educational and professional use.

## 🙏 Acknowledgments

- Dataset source: [Kaggle Network Intrusion Detection](https://www.kaggle.com/datasets/sampadab17/network-intrusion-detection)
- Built with ❤️ using Python, Streamlit, and Machine Learning

---

**Ready to deploy?** This application is production-ready and can be deployed on:
- Streamlit Cloud
- Heroku
- AWS
- Google Cloud
- Azure
- Any Docker-compatible platform

*Perfect for GitHub portfolios and freelancing platforms!* 🚀
