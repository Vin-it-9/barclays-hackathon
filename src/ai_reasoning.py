"""
GenAI-powered password reasoning and suggestion engine.
"""
import re
import random
from typing import Dict, List, Any


class PasswordAIReasoner:
    def __init__(self):
        self.attack_vectors = {
            "dictionary": {
                "description": "Dictionary attacks use lists of common words to guess passwords",
                "vulnerable_if": ["common words", "simple modifications of words", "predictable patterns"]
            },
            "brute_force": {
                "description": "Brute force attacks try every possible combination of characters",
                "vulnerable_if": ["short length", "limited character set"]
            },
            "rule_based": {
                "description": "Rule-based attacks apply common password creation patterns",
                "vulnerable_if": ["letter-to-symbol substitutions", "capital first letter", "number at end"]
            },
            "credential_stuffing": {
                "description": "Reusing passwords across multiple sites puts all your accounts at risk",
                "vulnerable_if": ["password has appeared in data breaches"]
            }
        }

    def _determine_attack_vectors(self, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Determine likely attack vectors for the password."""
        vectors = []

        # Check for dictionary attack vulnerability
        if analysis["crack_time"]["score"] < 3:
            vectors.append({
                "type": "dictionary",
                "name": "Dictionary Attack",
                "description": self.attack_vectors["dictionary"]["description"],
                "reasoning": "Your password may be vulnerable to dictionary attacks because it appears to contain "
                             "common patterns or modifications of known words."
            })

        # Check for brute force vulnerability
        if analysis["length"] < 10 or (analysis["entropy"] / analysis["length"]) < 3.0:
            vectors.append({
                "type": "brute_force",
                "name": "Brute Force Attack",
                "description": self.attack_vectors["brute_force"]["description"],
                "reasoning": f"Your {analysis['length']}-character password has insufficient complexity, making it feasible "
                             f"to crack through brute force methods in {analysis['crack_time']['crack_time_display']}."
            })

        # Check for rule-based attack vulnerability
        patterns = []
        if analysis["has_uppercase"] and not any(c.isupper() for c in analysis["password"][1:]):
            patterns.append("capital first letter")
        if analysis["has_digit"] and all(c.isdigit() for c in analysis["password"][-2:]):
            patterns.append("numbers at end")

        if patterns:
            vectors.append({
                "type": "rule_based",
                "name": "Pattern-Based Attack",
                "description": self.attack_vectors["rule_based"]["description"],
                "reasoning": f"Your password follows common patterns ({', '.join(patterns)}) that hackers specifically check for."
            })

        return vectors

    def generate_personalized_suggestion(self, password: str) -> str:
        """Generate a personalized password suggestion based on the original."""
        if not password:
            return "Use a combination of uppercase, lowercase, numbers, and special characters in a long password."

        # Keep some character structure but enhance it
        suggestion = list(password)

        # Apply transformations
        for i in range(len(suggestion)):
            # Randomly capitalize some lowercase letters
            if suggestion[i].islower() and random.random() > 0.7:
                suggestion[i] = suggestion[i].upper()
            # Change some letters to similar-looking symbols
            elif suggestion[i] == 'a' or suggestion[i] == 'A':
                if random.random() > 0.5:
                    suggestion[i] = '@'
            elif suggestion[i] == 'e' or suggestion[i] == 'E':
                if random.random() > 0.5:
                    suggestion[i] = '3'
            elif suggestion[i] == 'i' or suggestion[i] == 'I':
                if random.random() > 0.5:
                    suggestion[i] = '!'
            elif suggestion[i] == 'o' or suggestion[i] == 'O':
                if random.random() > 0.5:
                    suggestion[i] = '0'
            elif suggestion[i] == 's' or suggestion[i] == 'S':
                if random.random() > 0.5:
                    suggestion[i] = '$'

        # Add special characters at random positions if none exist
        if not any(not c.isalnum() for c in suggestion):
            special_chars = ['!', '@', '#', '$', '%', '&', '*', '?']
            positions = random.sample(range(len(suggestion)), min(2, len(suggestion)))
            for pos in positions:
                suggestion[pos] = random.choice(special_chars)

        # Add length if too short
        if len(suggestion) < 12:
            extra_chars = ['!', '@', '#', '$', '%', '&', '*', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            suggestion.extend(random.choices(extra_chars, k=12 - len(suggestion)))

        return ''.join(suggestion)

    def generate_detailed_reasoning(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed reasoning about password strength."""

        # Determine likely attack vectors
        attack_vectors = self._determine_attack_vectors(analysis)

        # Generate personalized password suggestion
        improved_password = self.generate_personalized_suggestion(analysis["password"])

        # Generate primary weakness explanation
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

        # Detail specific patterns found
        pattern_detail = ""
        if analysis["common_patterns"]:
            pattern_detail = f"Your password contains common patterns ({', '.join(analysis['common_patterns'])}) " \
                             f"that significantly weaken it."

        # Generate reasoning about character variety
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

        # Summarize time-to-crack with different algorithms
        time_reasoning = f"Using the bcrypt hashing algorithm, your password would take approximately " \
                         f"{analysis['crack_time']['crack_time_display']} to crack."

        # Assemble detailed reasoning
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

    test_password = "Pict@3782"
    analysis = analyzer.analyze_password(test_password)
    reasoning = reasoner.generate_detailed_reasoning(analysis)

    print(f"Password: {test_password}")
    print(f"Summary: {reasoning['summary']}")
    print(f"Primary weakness: {reasoning['primary_weakness']}")
    print(f"Attack vectors:")
    for vector in reasoning['attack_vectors']:
        print(f"  - {vector['name']}: {vector['reasoning']}")
    print(f"Improved suggestion: {reasoning['improved_suggestion']}")