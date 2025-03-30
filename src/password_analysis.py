import re
import math
import zxcvbn
from collections import Counter


class PasswordAnalyzer:
    def __init__(self):
        self.common_patterns = [
            r'12345',
            r'qwerty',
            r'password',
            r'admin',
            r'welcome'
        ]

        self.hashing_times = {
            'md5': 0.000001,
            'sha256': 0.00001,
            'bcrypt': 0.1,
            'argon2': 1.0
        }

    def calculate_entropy(self, password):

        if not password:
            return 0

        char_count = Counter(password)
        length = len(password)

        entropy = 0
        for count in char_count.values():
            probability = count / length
            entropy -= probability * math.log2(probability)

        return entropy * length

    def check_common_patterns(self, password):

        found_patterns = []
        for pattern in self.common_patterns:
            if re.search(pattern, password.lower()):
                found_patterns.append(pattern)

        return found_patterns

    def estimate_crack_time(self, password, algorithm='bcrypt'):

        result = zxcvbn.zxcvbn(password)

        multiplier = self.hashing_times.get(algorithm.lower(), self.hashing_times['bcrypt'])

        crack_time = result['crack_times_seconds']['offline_slow_hashing_1e4_per_second']
        crack_seconds = float(crack_time) * multiplier

        return {
            'crack_time_seconds': crack_seconds,
            'crack_time_display': result['crack_times_display']['offline_slow_hashing_1e4_per_second'],
            'score': result['score'],
            'feedback': result['feedback']
        }

    def analyze_password(self, password, algorithm='bcrypt'):

        entropy = self.calculate_entropy(password)
        common_patterns = self.check_common_patterns(password)
        crack_estimate = self.estimate_crack_time(password, algorithm)

        has_uppercase = any(c.isupper() for c in password)
        has_lowercase = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        return {
            'password': password,
            'length': len(password),
            'entropy': entropy,
            'common_patterns': common_patterns,
            'has_uppercase': has_uppercase,
            'has_lowercase': has_lowercase,
            'has_digit': has_digit,
            'has_special': has_special,
            'crack_time': crack_estimate,
        }

    def suggest_improvements(self, password):

        analysis = self.analyze_password(password)
        suggestions = []

        if len(password) < 12:
            suggestions.append("Increase password length to at least 12 characters")

        if not analysis['has_uppercase']:
            suggestions.append("Add uppercase letters")

        if not analysis['has_lowercase']:
            suggestions.append("Add lowercase letters")

        if not analysis['has_digit']:
            suggestions.append("Add digits")

        if not analysis['has_special']:
            suggestions.append("Add special characters")

        if analysis['common_patterns']:
            suggestions.append(f"Avoid common patterns (found: {', '.join(analysis['common_patterns'])})")

        if analysis['crack_time']['feedback']['warning']:
            suggestions.append(f"Warning: {analysis['crack_time']['feedback']['warning']}")

        for suggestion in analysis['crack_time']['feedback']['suggestions']:
            suggestions.append(suggestion)

        return suggestions


# Example usage
if __name__ == "__main__":
    analyzer = PasswordAnalyzer()
    test_password = "Password123"
    analysis = analyzer.analyze_password(test_password)
    print(f"Password: {test_password}")
    print(f"Entropy: {analysis['entropy']:.2f}")
    print(f"Crack time: {analysis['crack_time']['crack_time_display']}")
    print(f"Suggestions: {analyzer.suggest_improvements(test_password)}")