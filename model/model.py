import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the data

# Step 1: Load Data
data = pd.read_excel('model/dataset.xlsx')

df = pd.DataFrame(data)

# Drop non-numeric columns or encode them
# Drop columns not useful for modeling
df = df.drop(columns=['Email', 'School Id', 'School Name', 'Address'])

# Label encoding for categorical columns
label_encoders = {}
for column in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Define target and features
# Assuming we're predicting 'Any other Suggestions'
X = df.drop(columns=['Any other Suggestions'])
y = df['Any other Suggestions']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# Train a classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))


# Save the model
joblib.dump(clf, 'school_needs_model.pkl')

# Save label encoders
joblib.dump(label_encoders, 'label_encoders.pkl')