from flask import Flask, render_template, request, jsonify
from src.password_analysis import PasswordAnalyzer
from src.model import PasswordStrengthModel
from src.ai_reasoning import PasswordAIReasoner

app = Flask(__name__)
analyzer = PasswordAnalyzer()
model = PasswordStrengthModel()
reasoner = PasswordAIReasoner()

try:
    model.load_model()
    model_loaded = True
except:
    model_loaded = False
    print("Warning: Could not load ML model. Some features may be limited.")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    data = request.get_json()
    if not data or 'password' not in data:
        return jsonify({'error': 'No password provided'}), 400

    password = data['password']

    analysis = analyzer.analyze_password(password)
    suggestions = analyzer.suggest_improvements(password)

    if model_loaded:
        try:
            strength_prediction = model.predict_strength(password)
            analysis['strength_prediction'] = strength_prediction
        except Exception as e:
            print(f"Error predicting strength: {e}")
            analysis['strength_prediction'] = None

    ai_reasoning = reasoner.generate_detailed_reasoning(analysis)

    response = {
        'analysis': analysis,
        'suggestions': suggestions,
        'attack_vectors': ai_reasoning.get('attack_vectors', []),
        'summary': ai_reasoning.get('summary', ''),
        'primary_weakness': ai_reasoning.get('primary_weakness', ''),
        'time_analysis': ai_reasoning.get('time_analysis', ''),
        'character_variety': ai_reasoning.get('character_variety', ''),
        'improved_suggestion': ai_reasoning.get('improved_suggestion', ''),
        'pattern_analysis': ai_reasoning.get('pattern_analysis', '')
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)