# 🔐 SecurePass Analyzer

[![Python](https://img.shields.io/badge/Python-43.2%25-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-19.7%25-F7DF1E?style=flat&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML](https://img.shields.io/badge/HTML-18.4%25-E34F26?style=flat&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)


> An intelligent password strength analysis tool with AI-powered security enhancement recommendations developed for the Barclays Hackathon 2025.

![Password Security Banner](https://via.placeholder.com/800x200?text=SecurePass+Analyzer)

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Password Enhancement Algorithm](#-password-enhancement-algorithm)
- [Security Analysis Metrics](#-security-analysis-metrics)
- [API Reference](#-api-reference)
- [Frontend Components](#-frontend-components)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## 🔍 Overview

SecurePass Analyzer is a comprehensive password security tool that evaluates password strength using advanced algorithms and provides intelligent, personalized recommendations for creating stronger passwords. Unlike traditional password checkers, our solution maintains memorability while significantly enhancing security through targeted transformations.

This project was developed for the Barclays Hackathon 2025, addressing the critical need for improved password security in online banking and financial applications.

## ✨ Key Features

- **Comprehensive Password Analysis**: Evaluates entropy, character variety, common patterns, and estimated crack time
- **AI-Powered Suggestions**: Generates personalized password improvements that maintain memorability
- **Attack Vector Assessment**: Identifies specific vulnerabilities in passwords
- **Visual Strength Indicator**: Provides clear feedback on password security level
- **Pattern Recognition**: Detects common substitutions, sequences, and dictionary words
- **Detailed Security Reasoning**: Explains vulnerabilities in plain language
- **Web Interface**: Responsive design with real-time strength evaluation
- **Advanced Transformation Engine**: Creates secure variations like "Summer2024" → "5uMM3r#2024*Q"

## 🛠️ Technology Stack

- **Backend**: Python
  - Password analysis algorithms
  - Security metrics calculation
  - AI reasoning engine
  - RESTful API with Flask
  
- **Frontend**: JavaScript & HTML
  - Real-time password strength visualization
  - Interactive user interface
  - AJAX for asynchronous server interactions
  
## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Vin-it-9/barclays-hackathon.git
cd barclays-hackathon

# Create and activate virtual environment
password_strength_analyzer\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/app.py
```

### Web Interface

1. Start the server:
   ```bash
   python app.py
   ```

2. Open your browser to `http://localhost:5000`

3. Enter a password to receive detailed analysis and suggestions

### API Endpoint

```python
import requests

response = requests.post('http://localhost:5000/analyze', 
                         json={'password': 'Summer2024'})
results = response.json()
print(f"Strength: {results['strength']}")
print(f"Suggestion: {results['improved_suggestion']}")
```

## 🔐 Password Enhancement Algorithm

Our password enhancement algorithm uses targeted transformations to improve security while maintaining memorability:

1. **Strategic Character Substitution**: Replaces letters with similar-looking symbols (S→5, E→3)
2. **Pattern-Aware Capitalization**: Creates distinctive patterns like "uMM3r" for better memorability
3. **Special Character Insertion**: Adds symbols at strategic positions, particularly before numbers
4. **Security-Level Calibration**: Adjusts transformations to target the "months to crack" security level
5. **Entropy Management**: Controls the number and type of substitutions to achieve optimal security

Example transformation:
```
Original: Summer2024
Enhanced: 5uMM3r#2024*Q
```

## 📊 Security Analysis Metrics

The analyzer evaluates passwords using multiple dimensions:

| Metric | Description |
|--------|-------------|
| **Entropy** | Measures password randomness and unpredictability |
| **Character Variety** | Assesses usage of different character types |
| **Common Patterns** | Detects sequences, repetitions, and keyboard patterns |
| **Dictionary Vulnerability** | Identifies common words and their variations |
| **Crack Time Estimation** | Calculates time needed to break using different attack methods |
| **Attack Vectors** | Identifies specific vulnerabilities (brute force, dictionary, etc.) |

## 📚 API Reference

### Password Analysis Endpoint

```
POST /analyze
```

Request body:
```json
{
  "password": "Summer2024"
}
```

Response:
```json
{
    "analysis": {
        "common_patterns": [
            "summer\\d*",
            "20\\d\\d"
        ],
        "crack_time": {
            "crack_time_display": "3 minutes",
            "crack_time_seconds": 16.1984,
            "feedback": {
                "suggestions": [
                    "Add another word or two. Uncommon words are better.",
                    "Capitalization doesn't help very much."
                ],
                "warning": "This is similar to a commonly used password."
            },
            "score": 2
        },
        "entropy": 59.54196310386875,
        "has_digit": true,
        "has_lowercase": true,
        "has_special": false,
        "has_uppercase": true,
        "length": 10,
        "password": "Summer2024",
        "strength_prediction": {
            "category": 3,
            "category_name": "Strong",
            "confidence": 1.0,
            "probabilities": [
                0.0,
                0.0,
                0.0,
                1.0,
                0.0
            ]
        }
    },
    "attack_vectors": [
        {
            "description": "Dictionary attacks use lists of common words and passwords to quickly guess credentials",
            "name": "Dictionary Attack",
            "reasoning": "Your password contains common patterns (summer\\d*, 20\\d\\d) that make it vulnerable to dictionary-based attacks.",
            "type": "dictionary"
        },
        {
            "description": "Systematically checks all possible character combinations until finding the correct password",
            "name": "Brute Force Attack",
            "reasoning": "Your 10-character password has insufficient complexity (entropy: 59.5), making it feasible to crack through brute force in 3 minutes.",
            "type": "brute_force"
        },
        {
            "description": "Using personal information to make educated password guesses",
            "name": "Targeted Guessing",
            "reasoning": "Your password appears to contain dates or numbers that could be personal information.",
            "type": "targeted_guessing"
        },
        {
            "description": "Combines dictionary words with modifications and character substitutions",
            "name": "Hybrid Attack",
            "reasoning": "Your password uses predictable patterns (capital first letter, numbers at end) that hybrid attacks specifically target.",
            "type": "hybrid"
        }
    ],
    "character_variety": "Your password is missing special characters, which limits its complexity and makes it easier to guess.",
    "improved_suggestion": "5uMM3r#2024*K",
    "pattern_analysis": "Your password contains common patterns (summer\\d*, 20\\d\\d) that significantly weaken it.",
    "primary_weakness": "Your password would resist basic attacks but could be cracked with dedicated effort.",
    "suggestions": [
        "Increase password length to at least 12 characters",
        "Add special characters",
        "Avoid common patterns (found: summer\\d*, 20\\d\\d)",
        "Warning: This is similar to a commonly used password.",
        "Add another word or two. Uncommon words are better.",
        "Capitalization doesn't help very much."
    ],
    "summary": "Your password is moderately weak.",
    "time_analysis": "Using the bcrypt hashing algorithm, your password would take approximately 3 minutes to crack."
}
```

## 🎨 Frontend Components

- **Strength Meter**: Visual indicator showing password security level
- **Real-time Analysis**: Updates as the user types
- **Improvement Suggestions**: Shows enhanced password options
- **Vulnerability Breakdown**: Details specific weaknesses
- **Copy Button**: Easy transfer of suggested passwords
- **Security Tips**: Contextual advice based on analysis

## 📁 Project Structure

```
barclays-hackathon/
├── data/
│   ├── rockyou.txt                    # Password dataset
├── models/
│   ├── password_strength_model.joblib  # Trained model
├── src/                        
│   ├── password_analysis.py  # Core password analysis engine
│   ├── ai_reasoning.py       # Enhanced GenAi suggestion generation
│   ├── data_processing.py    # Data cleaning & transformation
│   ├── feature_extraction.py # Extracting password features
│   ├── model.py              # ML model handling    
├── static/
│   ├── JS/
         ├── main.js          # javascript
├── templates/    
    ├── index.html            # HTML templates
├── scripts/                  # Deployment and utility scripts
├── requirements.txt          # Dependencies
├── train_model.py            # Model training script config
├── Procfile                  # Deployment instruction
├── app.py                    # Flask file
├── explore_dataset.py        # Exploratory data analysis
```

