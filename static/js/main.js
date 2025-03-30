document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('passwordInput');
    const toggleButton = document.getElementById('togglePassword');
    const results = document.getElementById('results');
    const strengthProgress = document.getElementById('strengthProgress');
    const strengthCategory = document.getElementById('strengthCategory');
    const analysisDetails = document.getElementById('analysisDetails');
    const suggestions = document.getElementById('suggestions');
    const typingIndicator = document.getElementById('typingIndicator');
    const aiReasoning = document.getElementById('aiReasoning');
    const attackVectors = document.getElementById('attackVectors');
    const aiReasoningSection = document.getElementById('aiReasoningSection');
    const attackVectorsSection = document.getElementById('attackVectorsSection');

    let debounceTimer;
    const DEBOUNCE_DELAY = 600;

    toggleButton.addEventListener('click', function() {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleButton.textContent = 'Hide';
        } else {
            passwordInput.type = 'password';
            toggleButton.textContent = 'Show';
        }
        passwordInput.focus();
    });

    passwordInput.addEventListener('input', function() {
        const password = passwordInput.value;

        if (!password) {
            hideResults();
            typingIndicator.classList.add('hidden');
            return;
        }

        typingIndicator.classList.remove('hidden');

        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            analyzePassword(password);
        }, DEBOUNCE_DELAY);
    });

    function analyzePassword(password) {
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password: password })
        })
        .then(response => response.json())
        .then(data => {
            typingIndicator.classList.add('hidden');
            if (data.error) {
                console.error('Error:', data.error);
                return;
            }
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            typingIndicator.classList.add('hidden');
        });
    }

    function displayResults(data) {
        const analysis = data.analysis;

        if (Object.keys(analysis).length === 0) {
            hideResults();
            return;
        }

        let score = 0;
        let categoryName = 'Unknown';
        let colorClass = '';
        let bgClass = '';
        let percentText = '';

        if (analysis.strength_prediction) {
            score = analysis.strength_prediction.category * 25;
            categoryName = analysis.strength_prediction.category_name;
        } else if (analysis.crack_time) {
            const crackTimeSeconds = analysis.crack_time.crack_time_seconds;
            if (crackTimeSeconds < 1) score = 0;
            else if (crackTimeSeconds < 60) score = 15;
            else if (crackTimeSeconds < 3600) score = 30;
            else if (crackTimeSeconds < 86400) score = 45;
            else if (crackTimeSeconds < 604800) score = 60;
            else if (crackTimeSeconds < 2592000) score = 75;
            else score = 90;

            categoryName = analysis.crack_time.score <= 1 ? 'Weak' :
                          analysis.crack_time.score === 2 ? 'Medium' :
                          analysis.crack_time.score === 3 ? 'Strong' : 'Very Strong';
        }

        if (score < 25) {
            colorClass = 'bg-gradient-to-r from-red-500 to-red-600';
            bgClass = 'bg-red-50';
            strengthCategory.className = 'text-center text-xl sm:text-2xl font-bold text-red-600';
            percentText = `${score}%`;
        } else if (score < 50) {
            colorClass = 'bg-gradient-to-r from-orange-400 to-orange-500';
            bgClass = 'bg-orange-50';
            strengthCategory.className = 'text-center text-xl sm:text-2xl font-bold text-orange-600';
            percentText = `${score}%`;
        } else if (score < 75) {
            colorClass = 'bg-gradient-to-r from-yellow-400 to-yellow-500';
            bgClass = 'bg-yellow-50';
            strengthCategory.className = 'text-center text-xl sm:text-2xl font-bold text-yellow-600';
            percentText = `${score}%`;
        } else if (score < 90) {
            colorClass = 'bg-gradient-to-r from-green-400 to-green-500';
            bgClass = 'bg-green-50';
            strengthCategory.className = 'text-center text-xl sm:text-2xl font-bold text-green-600';
            percentText = `${score}%`;
        } else {
            colorClass = 'bg-gradient-to-r from-emerald-400 to-green-600';
            bgClass = 'bg-emerald-50';
            strengthCategory.className = 'text-center text-xl sm:text-2xl font-bold text-emerald-600';
            percentText = `${score}%`;
        }

        strengthProgress.className = `h-6 rounded-full pl-2 transition-all duration-700 ease-out shadow-sm ${colorClass}`;
        strengthProgress.style.width = `${score}%`;
        strengthProgress.innerHTML = `<span class="text-xs font-bold text-white drop-shadow-sm">${percentText}</span>`;
        strengthCategory.textContent = categoryName;

        let aiReasoningText = '';

        if (data.summary) {
            aiReasoningText += `${data.summary}\n\n`;
        }

        if (data.primary_weakness) {
            aiReasoningText += `${data.primary_weakness}\n\n`;
        }

        if (data.time_analysis) {
            aiReasoningText += `${data.time_analysis}\n\n`;
        }

        if (data.character_variety) {
            aiReasoningText += `${data.character_variety}\n\n`;
        }

        if (data.pattern_analysis) {
            aiReasoningText += `${data.pattern_analysis}\n\n`;
        }

        if (data.improved_suggestion) {
            aiReasoningText += `Improved suggestion: ${data.improved_suggestion}`;
        }

        if (aiReasoningText) {
            aiReasoning.textContent = aiReasoningText;
            aiReasoningSection.classList.remove('hidden');
        } else {
            aiReasoningSection.classList.add('hidden');
        }

        if (data.attack_vectors && data.attack_vectors.length > 0) {
            attackVectors.innerHTML = '';
            data.attack_vectors.forEach(attack => {
                let riskColorClass = '';
                let riskIcon = '';

                if (attack.type && attack.type.toLowerCase().includes('brute_force')) {
                    riskColorClass = 'border-red-400 bg-red-50/80 text-red-800';
                    riskIcon = `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>`;
                } else if (attack.type && attack.type.toLowerCase().includes('dictionary')) {
                    riskColorClass = 'border-orange-400 bg-orange-50/80 text-orange-800';
                    riskIcon = `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-orange-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>`;
                } else {
                    riskColorClass = 'border-yellow-400 bg-yellow-50/80 text-yellow-800';
                    riskIcon = `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>`;
                }

                attackVectors.innerHTML += `
                    <li class="p-3 rounded-lg border-l-4 ${riskColorClass} shadow-sm">
                        <div class="flex items-center">
                            ${riskIcon}
                            <h4 class="font-medium text-sm sm:text-base">${attack.name || 'Unknown Attack'}</h4>
                        </div>
                        <p class="mt-2 text-xs sm:text-sm">${attack.description || 'No description available'}</p>
                        <p class="mt-2 text-xs sm:text-sm font-medium">${attack.reasoning || ''}</p>
                    </li>
                `;
            });
            attackVectorsSection.classList.remove('hidden');
        } else {
            attackVectorsSection.classList.add('hidden');
        }

        analysisDetails.innerHTML = '';

        if ('length' in analysis) {
            addAnalysisRow('Password length', `${analysis.length} characters`);
        }

        if ('entropy' in analysis) {
            addAnalysisRow('Entropy', `${analysis.entropy.toFixed(2)} bits`);
        }

        if ('crack_time' in analysis && 'crack_time_display' in analysis.crack_time) {
            addAnalysisRow('Time to crack', analysis.crack_time.crack_time_display);
        }

        if ('has_uppercase' in analysis) {
            addAnalysisRow('Contains uppercase letters',
                formatYesNo(analysis.has_uppercase));
        }

        if ('has_lowercase' in analysis) {
            addAnalysisRow('Contains lowercase letters',
                formatYesNo(analysis.has_lowercase));
        }

        if ('has_digit' in analysis) {
            addAnalysisRow('Contains digits',
                formatYesNo(analysis.has_digit));
        }

        if ('has_special' in analysis) {
            addAnalysisRow('Contains special characters',
                formatYesNo(analysis.has_special));
        }

        if ('common_patterns' in analysis && analysis.common_patterns && analysis.common_patterns.length > 0) {
            addAnalysisRow('Common patterns found',
                `<span class="text-red-500 font-medium flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                    ${analysis.common_patterns.join(', ')}
                </span>`);
        }

        suggestions.innerHTML = '';
        if (data.improved_suggestion) {
            suggestions.innerHTML += `
                <li class="bg-green-50/80 p-3 rounded-lg text-green-800 border-l-4 border-green-500 shadow-sm">
                    <div class="flex items-start">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div>
                            <div class="font-medium">Suggested stronger password:</div>
                            <div class="mt-1 font-mono bg-white/70 px-3 py-1.5 rounded border border-green-200 text-sm">${data.improved_suggestion}</div>
                        </div>
                    </div>
                </li>
            `;
        }

        if (data.suggestions && data.suggestions.length > 0) {
            data.suggestions.forEach(suggestion => {
                suggestions.innerHTML += `
                    <li class="bg-indigo-50/80 p-3 rounded-lg text-indigo-800 border-l-4 border-indigo-500 mt-2 shadow-sm">
                        <div class="flex items-start">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-500 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <div class="text-xs sm:text-sm">${suggestion}</div>
                        </div>
                    </li>
                `;
            });
        } else if (!data.improved_suggestion) {
            suggestions.innerHTML = `
                <li class="bg-green-50/80 p-3 rounded-lg text-green-800 border-l-4 border-green-500 shadow-sm">
                    <div class="flex items-start">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                        <div class="font-medium">Your password looks good!</div>
                    </div>
                </li>
            `;
        }

        showResults();
    }

    function formatYesNo(value) {
        if (value) {
            return `<span class="text-green-500 font-medium flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                Yes
            </span>`;
        } else {
            return `<span class="text-red-500 font-medium flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                No
            </span>`;
        }
    }

    function addAnalysisRow(label, value) {
        analysisDetails.innerHTML += `
            <tr class="border-b border-gray-100">
                <td class="py-2.5 pl-3 pr-2 text-gray-700 text-xs sm:text-sm">${label}</td>
                <td class="py-2.5 px-3 font-medium text-xs sm:text-sm">${value}</td>
            </tr>
        `;
    }

    function showResults() {
        results.style.display = 'block';
        void results.offsetWidth;
        results.classList.remove('opacity-0', 'translate-y-4');
        results.classList.add('opacity-100', 'translate-y-0');
    }

    function hideResults() {
        results.classList.add('opacity-0', 'translate-y-4');
        results.classList.remove('opacity-100', 'translate-y-0');
        setTimeout(() => {
            results.style.display = 'none';
        }, 500);
    }
});