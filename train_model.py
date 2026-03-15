import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load data
data = pd.read_csv('Train_data.csv')
data.rename(columns={'class': 'Class'}, inplace=True)

# Encoding
object_columns = data.select_dtypes(include=['object']).columns
label_encoders = {}
for col in object_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Split features and target
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Feature selection
selector = SelectKBest(score_func=f_regression, k=25)
X_selected = selector.fit_transform(X_scaled, y)

# Train model
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

# Save everything
joblib.dump(rf_classifier, 'rf_model.joblib')
joblib.dump(scaler, 'scaler.joblib')
joblib.dump(selector, 'selector.joblib')
joblib.dump(label_encoders, 'label_encoders.joblib')
joblib.dump(X.columns.tolist(), 'feature_names.joblib')

print("Model and assets saved successfully!")
