import re
import math
import zxcvbn
import string
from collections import Counter


class PasswordAnalyzer:
    def __init__(self):

        self.common_patterns = [
            r'12345\d*', r'qwerty\w*', r'password\d*', r'admin\d*', r'welcome\d*', r'abcd\w*', r'1234\d*', r'0123\d*',
            r'9876\d*', r'zxcvb\w*', r'asdfg\w*', r'letmein\d*', r'trustno\d*', r'monkey\d*', r'dragon\d*',r'master\d*',
            r'football\d*', r'baseball\d*', r'soccer\d*', r'hockey\d*', r'superman\d*', r'batman\d*', r'starwars\d*',
            r'abc123\w*', r'test\d*', r'guest\d*', r'login\d*', r'pass\w*', r'secret\d*', r'shadow\d*',
            r'january\d*', r'february\d*', r'march\d*', r'april\d*', r'may\d*', r'june\d*', r'july\d*',
            r'august\d*', r'september\d*', r'october\d*', r'november\d*', r'december\d*', r'winter\d*',
            r'spring\d*', r'summer\d*', r'fall\d*', r'autumn\d*', r'111+', r'222+', r'333+', r'444+',
            r'555+', r'666+', r'777+', r'888+', r'999+', r'000+', r'aaa+', r'p@ssw0rd', r'@dmin', r's3cur3',
            r'l0gin', r'w3lc0me', r'19\d\d', r'20\d\d', r'\d\d\d\d\d\d', r'yankees\d*', r'cowboys\d*',
            r'lakers\d*', r'patriots\d*', r'redsox\d*', r'arsenal\d*', r'chelsea\d*', r'liverpool\d*',
            r'admin123\d*', r'root123\d*', r'cisco\d*', r'oracle\d*', r'database\d*', r'server\d*',
            r'firewall\d*', r'system\d*', r'iloveyou\d*', r'ilove\w+', r'princessa\d*', r'princess\d*',
            r'sunshine\d*', r'beautiful\d*', r'whatever\d*', r'nothing\d*', r'qazwsx\w*', r'zxcvbn\w*',
            r'qwertyuiop\w*', r'asdfghjkl\w*', r'zxcvbnm\w*', r'microsoft\d*', r'google\d*', r'apple\d*',
            r'amazon\d*', r'facebook\d*', r'twitter\d*', r'linkedin\d*', r'netflix\d*', r'badword\d*',
            r'bond007', r'agent007', r'jordan23', r'passw0rd\d*', r'passwd\d*', r'p455w0rd\d*',
            r'pa55word\d*', r'first\w+name', r'maiden\w+name', r'pet\w+name', r'school\w+name',
            r'favorite\w+', r'changeme\d*', r'default\d*', r'temppass\d*'
        ]

        self.hashing_times = {
            'md5': 0.0000005,
            'sha1': 0.0000008,
            'sha256': 0.000005,
            'sha512': 0.000008,
            'bcrypt': 0.08,
            'pbkdf2_100000': 0.05,
            'argon2id': 0.9,
            'argon2i': 1.0,
            'argon2d': 0.85,
            'balloon': 1.2,
            'scrypt': 0.7,
            'yescrypt': 1.1,
            'gpu_optimized_md5': 0.00000001,
            'asic_sha256': 0.0000001,
            'quantum_resistant': 5.0
        }



    def calculate_entropy(self, password):
        if not password:
            return 0

        pool = 0

        if any(c.islower() for c in password):
            pool += 26

        if any(c.isupper() for c in password):
            pool += 26

        if any(c.isdigit() for c in password):
            pool += 10

        if any(c in string.punctuation for c in password):
            pool += len(string.punctuation)

        if pool == 0:
            return 0

        return len(password) * math.log2(pool)


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