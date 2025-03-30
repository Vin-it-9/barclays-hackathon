import re
import numpy as np
from collections import Counter


class PasswordFeatureExtractor:
    def __init__(self):
        self.feature_names = [
            'length',
            'uppercase_count',
            'lowercase_count',
            'digit_count',
            'special_count',
            'entropy',
            'unique_char_ratio',
            'has_sequence',
            'has_repeated_chars',
            'keyboard_pattern_count',
        ]

    def extract_features(self, password):

        if not password:
            return np.zeros(len(self.feature_names))

        features = []

        features.append(len(password))
        features.append(sum(1 for c in password if c.isupper()))
        features.append(sum(1 for c in password if c.islower()))
        features.append(sum(1 for c in password if c.isdigit()))
        features.append(sum(1 for c in password if not c.isalnum()))

        char_count = Counter(password)
        length = len(password)
        entropy = 0
        for count in char_count.values():
            probability = count / length
            entropy -= probability * np.log2(probability) if probability > 0 else 0
        entropy *= length
        features.append(entropy)

        features.append(len(char_count) / length)

        has_sequence = 0
        for i in range(len(password) - 2):
            if (ord(password[i]) + 1 == ord(password[i + 1]) and
                    ord(password[i + 1]) + 1 == ord(password[i + 2])):
                has_sequence = 1
                break
        features.append(has_sequence)

        has_repeated = 0
        for i in range(len(password) - 2):
            if password[i] == password[i + 1] == password[i + 2]:
                has_repeated = 1
                break
        features.append(has_repeated)

        keyboard_rows = [
            "qwertyuiop",
            "asdfghjkl",
            "zxcvbnm",
            "1234567890"
        ]

        pattern_count = 0
        for row in keyboard_rows:
            for i in range(len(row) - 2):
                pattern = row[i:i + 3].lower()
                if pattern in password.lower():
                    pattern_count += 1
        features.append(pattern_count)

        return np.array(features)

    def extract_features_batch(self, passwords):
        return np.array([self.extract_features(pwd) for pwd in passwords])


if __name__ == "__main__":
    extractor = PasswordFeatureExtractor()
    test_password = "Password123"
    features = extractor.extract_features(test_password)

    for name, value in zip(extractor.feature_names, features):
        print(f"{name}: {value}")