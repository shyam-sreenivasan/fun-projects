import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import kagglehub
import os

# Download dataset
path = kagglehub.dataset_download("rakeshkapilavai/extrovert-vs-introvert-behavior-data")
print("Path to dataset files:", path)

# Load dataset
df = pd.read_csv(os.path.join(path, 'personality_dataset.csv'))

# Preview
print(df.head())
print("Columns:", df.columns)

# Label encode the target column
label_encoder = LabelEncoder()
df['Personality'] = label_encoder.fit_transform(df['Personality'])  # Introvert=0, Extrovert=1

# Label encode categorical feature columns
categorical_columns = df.select_dtypes(include='object').columns

for col in categorical_columns:
    df[col] = LabelEncoder().fit_transform(df[col])

# Separate features and target
X = df.drop('Personality', axis=1)
y = df['Personality']

# Print encoded features
print("Encoded feature columns:")
print(X.head())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Predict and evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
