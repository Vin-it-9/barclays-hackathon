"""
GenAI-powered password reasoning and suggestion engine.
"""
import re
import random
import string
from typing import Dict, List, Any


class PasswordAIReasoner:

    def __init__(self):
        self.attack_vectors = {
            "dictionary": {
                "description": "Dictionary attacks use lists of common words and passwords to quickly guess credentials",
                "vulnerable_if": ["contains common words", "matches known passwords", "uses predictable patterns"]
            },
            "brute_force": {
                "description": "Systematically checks all possible character combinations until finding the correct password",
                "vulnerable_if": ["short length", "limited character set", "low entropy"]
            },
            "credential_stuffing": {
                "description": "Attackers use leaked username/password pairs from one service to access other services",
                "vulnerable_if": ["password has appeared in data breaches", "password is reused across sites"]
            },
            "targeted_guessing": {
                "description": "Using personal information to make educated password guesses",
                "vulnerable_if": ["contains personal info like names or dates", "includes interests or hobbies"]
            },
            "hybrid": {
                "description": "Combines dictionary words with modifications and character substitutions",
                "vulnerable_if": ["common words with numbers appended",
                                  "predictable character substitutions (a→@, e→3)"]
            },
            "rainbow_table": {
                "description": "Using precomputed tables to reverse cryptographic hash functions",
                "vulnerable_if": ["hashed without salt", "uses weak hashing algorithms"]
            }
        }

    def _determine_attack_vectors(self, analysis: Dict[str, Any]) -> List[Dict[str, str]]:

        vectors = []
        password = analysis["password"]

        if analysis["common_patterns"] or analysis["crack_time"]["score"] < 3:
            vectors.append({
                "type": "dictionary",
                "name": "Dictionary Attack",
                "description": self.attack_vectors["dictionary"]["description"],
                "reasoning": f"Your password contains common patterns ({', '.join(analysis['common_patterns']) if analysis['common_patterns'] else 'weak patterns'}) "
                             f"that make it vulnerable to dictionary-based attacks."
            })

        if analysis["length"] < 12 or analysis["entropy"] < 3.0:
            vectors.append({
                "type": "brute_force",
                "name": "Brute Force Attack",
                "description": self.attack_vectors["brute_force"]["description"],
                "reasoning": f"Your {analysis['length']}-character password has insufficient complexity (entropy: {analysis['entropy']:.1f}), "
                             f"making it feasible to crack through brute force in {analysis['crack_time']['crack_time_display']}."
            })

        if analysis["crack_time"]["score"] < 2 or any(
                p in password.lower() for p in ["password", "123", "admin", "welcome"]):
            vectors.append({
                "type": "credential_stuffing",
                "name": "Credential Stuffing",
                "description": self.attack_vectors["credential_stuffing"]["description"],
                "reasoning": "Your password has characteristics commonly found in breached password databases."
            })


        year_pattern = re.compile(r"(19|20)\d{2}")
        if year_pattern.search(password) or len(re.findall(r"\d{1,4}", password)) > 1:
            vectors.append({
                "type": "targeted_guessing",
                "name": "Targeted Guessing",
                "description": self.attack_vectors["targeted_guessing"]["description"],
                "reasoning": "Your password appears to contain dates or numbers that could be personal information."
            })

        patterns = []
        if analysis["has_uppercase"] and not any(c.isupper() for c in password[1:]):
            patterns.append("capital first letter")
        if analysis["has_digit"] and all(c.isdigit() for c in password[-2:]):
            patterns.append("numbers at end")
        if any(c.isalpha() for c in password) and any(c.isdigit() for c in password):
            common_subs = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "$"}
            for char, sub in common_subs.items():
                if char in password.lower() and sub in password:
                    patterns.append(f"predictable substitution ({char}->{sub})")

        if patterns:
            vectors.append({
                "type": "hybrid",
                "name": "Hybrid Attack",
                "description": self.attack_vectors["hybrid"]["description"],
                "reasoning": f"Your password uses predictable patterns ({', '.join(patterns)}) that hybrid attacks specifically target."
            })

        if analysis["length"] <= 8 and analysis["entropy"] < 2.5:
            vectors.append({
                "type": "rainbow_table",
                "name": "Rainbow Table Attack",
                "description": self.attack_vectors["rainbow_table"]["description"],
                "reasoning": "Simple passwords like yours are likely included in pre-computed rainbow tables."
            })

        return vectors


    # no need to update the above code with the new password analysis method

    def generate_personalized_suggestion(self, password: str) -> str:

        import re
        import random
        import string

        if not password:
            return "Use a combination of uppercase, lowercase, numbers, and special characters in a long password."

        suggestion = list(password)

        substitutions = {
            'a': '@', 'A': '@',
            'b': '8', 'B': '8',
            'e': '3', 'E': '3',
            'g': '9', 'G': '9',
            'i': '1', 'I': '1',
            'l': '1', 'L': '1',
            'o': '0', 'O': '0',
            's': '5', 'S': '5',
            't': '7', 'T': '7',
            'z': '2', 'Z': '2'
        }

        word_matches = list(re.finditer(r'[a-zA-Z]+', password))
        number_matches = list(re.finditer(r'\d+', password))

        if word_matches:
            first_word = word_matches[0].group()
            first_pos = word_matches[0].start()

            if first_word[0].lower() in substitutions:
                suggestion[first_pos] = substitutions[first_word[0].lower()]

        for match in word_matches:
            word = match.group()
            start = match.start()

            if len(word) >= 3:

                for i in range(len(word)):
                    if suggestion[start + i].isalpha():
                        suggestion[start + i] = suggestion[start + i].lower()

                if len(word) >= 5:
                    if start + 2 < len(suggestion):
                        suggestion[start + 2] = suggestion[start + 2].upper()
                    if start + 3 < len(suggestion):
                        suggestion[start + 3] = suggestion[start + 3].upper()

                elif len(word) == 3 or len(word) == 4:
                    middle = start + len(word) // 2
                    if suggestion[middle].isalpha():
                        suggestion[middle] = suggestion[middle].upper()

        for match in word_matches:
            word = match.group()
            start = match.start()
            for i in range(len(word)):
                pos = start + i
                if pos < len(suggestion) and suggestion[pos].lower() in 'aeiou' and suggestion[
                    pos].lower() in substitutions:
                    if suggestion[pos].lower() == 'e' or random.random() > 0.6:
                        suggestion[pos] = substitutions[suggestion[pos].lower()]

        if number_matches:
            first_num = number_matches[0]
            num_start = first_num.start()
            if num_start > 0 and suggestion[num_start - 1].isalnum():
                suggestion.insert(num_start, '#')
                insertion_offset = 1
            else:
                insertion_offset = 0
        else:
            insertion_offset = 0

        result = ''.join(suggestion)

        ending_special = len(result) >= 1 and not result[-1].isalnum()
        ending_capital = len(result) >= 1 and result[-1].isupper()

        if not (ending_special and ending_capital):
            if number_matches:
                result += '*' + random.choice('QWERTYUPADFGHJKLZXCVBNM')
            else:
                result += random.choice('#*!$') + random.choice('QWERTYUPASDFGHJKLZXCVBNM')

        if len(result) < 10:

            needed = 10 - len(result)
            extension = []

            if not any(c.isdigit() for c in result):
                extension.append(random.choice('123456789'))

            if not any(c.isupper() for c in result):
                extension.append(random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ'))

            if not any(not c.isalnum() for c in result):
                extension.append(random.choice('!@#$%^&*?'))

            # Fill remaining with mixed characters
            while len(extension) < needed:
                extension.append(random.choice('abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789!@#$%^&*?'))

            result += ''.join(extension)



        return result

    def generate_detailed_reasoning(self, analysis: Dict[str, Any]) -> Dict[str, Any]:

        attack_vectors = self._determine_attack_vectors(analysis)

        improved_password = self.generate_personalized_suggestion(analysis["password"])

        if analysis["crack_time"]["score"] <= 1:
            primary_weakness = "critically weak"
            weakness_detail = "Your password could be cracked almost instantly with basic hacking tools."
        elif analysis["crack_time"]["score"] == 2:
            primary_weakness = "moderately weak"
            weakness_detail = "Your password would resist basic attacks but could be cracked with dedicated effort."
        elif analysis["crack_time"]["score"] == 3:
            primary_weakness = "reasonably strong"
            weakness_detail = "Your password has good strength but could still be improved."
        else:
            primary_weakness = "very strong"
            weakness_detail = "Your password demonstrates excellent security properties."

        pattern_detail = ""
        if analysis["common_patterns"]:
            pattern_detail = f"Your password contains common patterns ({', '.join(analysis['common_patterns'])}) " \
                             f"that significantly weaken it."

        variety_factors = []
        if not analysis["has_uppercase"]:
            variety_factors.append("uppercase letters")
        if not analysis["has_lowercase"]:
            variety_factors.append("lowercase letters")
        if not analysis["has_digit"]:
            variety_factors.append("numbers")
        if not analysis["has_special"]:
            variety_factors.append("special characters")

        variety_reasoning = ""
        if variety_factors:
            variety_reasoning = f"Your password is missing {', '.join(variety_factors)}, " \
                                f"which limits its complexity and makes it easier to guess."

        time_reasoning = f"Using the bcrypt hashing algorithm, your password would take approximately " \
                         f"{analysis['crack_time']['crack_time_display']} to crack."

        detailed_reasoning = {
            "summary": f"Your password is {primary_weakness}.",
            "primary_weakness": weakness_detail,
            "attack_vectors": attack_vectors,
            "pattern_analysis": pattern_detail if pattern_detail else None,
            "character_variety": variety_reasoning if variety_reasoning else None,
            "time_analysis": time_reasoning,
            "improved_suggestion": improved_password
        }

        return detailed_reasoning


# Example usage
if __name__ == "__main__":
    from password_analysis import PasswordAnalyzer

    analyzer = PasswordAnalyzer()
    reasoner = PasswordAIReasoner()

    test_password = "Vinit@2559"
    analysis = analyzer.analyze_password(test_password)
    reasoning = reasoner.generate_detailed_reasoning(analysis)

    print(f"Password: {test_password}")
    print(f"Summary: {reasoning['summary']}")
    print(f"Primary weakness: {reasoning['primary_weakness']}")
    print(f"Attack vectors:")
    for vector in reasoning['attack_vectors']:
        print(f"  - {vector['name']}: {vector['reasoning']}")
    print(f"Improved suggestion: {reasoning['improved_suggestion']}")