
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from src.feature_extraction import PasswordFeatureExtractor
from src.data_processing import PasswordDataProcessor


class PasswordStrengthModel:
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        self.model_path = os.path.join(model_dir, 'password_strength_model.joblib')
        self.feature_extractor = PasswordFeatureExtractor()
        self.model = None

        os.makedirs(model_dir, exist_ok=True)

    def load_model(self):

        if os.path.exists(self.model_path):
            print(f"Loading model from {self.model_path}")
            self.model = joblib.load(self.model_path)
            return True
        else:
            print(f"No model found at {self.model_path}")
            return False

    def save_model(self):

        if self.model is not None:
            print(f"Saving model to {self.model_path}")
            joblib.dump(self.model, self.model_path)
            return True
        else:
            print("No model to save")
            return False

    def train(self, passwords, labels):
        print("Extracting features...")
        X = self.feature_extractor.extract_features_batch(passwords)
        y = np.array(labels)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        print("Training model...")
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.4f}")
        print("\nClassification report:")
        print(classification_report(y_test, y_pred))

        return accuracy

    def prepare_training_data_from_rockyou(self, sample_size=500000, random_seed=42):

        import pandas as pd
        from collections import Counter

        processor = PasswordDataProcessor()
        df = processor.load_rockyou_dataset()

        if df is None:
            print("Failed to load dataset")
            return None, None

        print(f"Loaded dataset with {len(df)} passwords")

        df['length'] = df['password'].apply(len)
        length_bins = [0, 6, 8, 10, 12, float('inf')]
        df['length_bin'] = pd.cut(df['length'], bins=length_bins, labels=False)

        actual_sample_size = min(sample_size, len(df))

        try:
            df_sample = df.groupby('length_bin', group_keys=False).apply(
                lambda x: x.sample(min(len(x), int(actual_sample_size * len(x) / len(df))), random_state=random_seed)
            )
        except:
            print("Falling back to random sampling")
            df_sample = df.sample(actual_sample_size, random_state=random_seed)

        passwords = df_sample['password'].tolist()

        common_passwords = set(processor.get_common_passwords(top_n=20000))

        pattern_regex = [
            r'^\d{6,8}$',
            r'^[a-z]+\d{1,4}$',
            r'^\d{1,4}[a-z]+$',
            r'^(19|20)\d{2}$',
            r'^qwerty',
            r'^asdf',
            r'^1234',
            r'^abcd',
        ]

        l33t_patterns = [
            (r'a', '@'), (r'a', '4'),
            (r'e', '3'), (r'i', '1'),
            (r'o', '0'), (r's', '$'),
            (r'l', '1'), (r't', '7')
        ]

        labels = []
        features = []

        for pwd in passwords:
            feature_dict = {
                'length': len(pwd),
                'has_upper': any(c.isupper() for c in pwd),
                'has_lower': any(c.islower() for c in pwd),
                'has_digit': any(c.isdigit() for c in pwd),
                'has_special': any(not c.isalnum() for c in pwd),
                'in_common_list': pwd in common_passwords,
            }

            if feature_dict['in_common_list']:
                labels.append(0)  # Very weak
                features.append(feature_dict)
                continue

            length = feature_dict['length']
            has_upper = feature_dict['has_upper']
            has_lower = feature_dict['has_lower']
            has_digit = feature_dict['has_digit']
            has_special = feature_dict['has_special']

            char_variety = sum([has_upper, has_lower, has_digit, has_special])

            char_counts = Counter(pwd)
            total_chars = len(pwd)
            entropy = sum(-(count / total_chars) * (count / total_chars) for count in char_counts.values())
            feature_dict['entropy'] = entropy

            sequential_count = 0
            for i in range(1, len(pwd)):
                if ord(pwd[i]) - ord(pwd[i - 1]) == 1:
                    sequential_count += 1
            feature_dict['sequential_chars'] = sequential_count

            if length < 6:
                labels.append(0)
            elif length < 8:
                if char_variety <= 1:
                    labels.append(0)
                else:
                    labels.append(1)
            elif length < 10:
                if char_variety == 1:
                    labels.append(1)
                elif char_variety == 2:
                    labels.append(2)
                else:
                    labels.append(2)
            elif length < 12:
                if char_variety <= 2:
                    labels.append(2)
                elif char_variety == 3:
                    labels.append(3)
                else:
                    labels.append(3)
            else:
                if char_variety <= 2:
                    labels.append(2)
                elif char_variety == 3:
                    labels.append(3)
                else:
                    labels.append(4)

            import re
            for pattern in pattern_regex:
                if re.search(pattern, pwd, re.IGNORECASE):
                    labels[-1] = max(0, labels[-1] - 1)
                    break

            features.append(feature_dict)

        label_counts = Counter(labels)
        print("Password strength distribution:")
        for label, count in sorted(label_counts.items()):
            print(f"Strength {label}: {count} passwords ({count / len(labels):.1%})")

        print(f"Prepared {len(passwords)} passwords with labels")
        return passwords, labels

    def predict_strength(self, password):

        if self.model is None:
            if not self.load_model():
                raise ValueError("No model available. Train or load a model first.")

        features = self.feature_extractor.extract_features(password)
        features = features.reshape(1, -1)

        strength_category = self.model.predict(features)[0]
        strength_proba = self.model.predict_proba(features)[0]

        strength_names = ['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong']

        return {
            'category': int(strength_category),
            'category_name': strength_names[strength_category],
            'probabilities': strength_proba.tolist(),
            'confidence': strength_proba[strength_category]
        }

if __name__ == "__main__":
    model = PasswordStrengthModel()

    if not model.load_model():
        print("Training new model...")
        passwords, labels = model.prepare_training_data_from_rockyou()

        if passwords and labels:
            model.train(passwords, labels)
            model.save_model()

    test_passwords = [
        "password",
        "Password123",
        "P@ssw0rd!",
        "fj39fjd93jf93j!",
        "CorrectHorseBatteryStaple"
    ]

    print("\nTesting model with sample passwords:")
    for pwd in test_passwords:
        result = model.predict_strength(pwd)
        print(f"Password: {pwd}")
        print(f"  Strength: {result['category_name']} (Category {result['category']})")
        print(f"  Confidence: {result['confidence']:.2f}")