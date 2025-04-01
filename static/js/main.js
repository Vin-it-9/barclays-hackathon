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

    let currentTypingAnimation = null;


    let debounceTimer;
    const DEBOUNCE_DELAY = 300;

    toggleButton.classList.add('transition-colors', 'duration-300', 'ease-in-out');

    toggleButton.addEventListener('click', function() {
        toggleButton.classList.add('scale-95');
        setTimeout(() => toggleButton.classList.remove('scale-95'), 150);
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleButton.textContent = 'Hide';
            toggleButton.classList.remove('bg-indigo-100', 'text-indigo-700');
            toggleButton.classList.add('bg-indigo-700', 'text-white');
        } else {
            passwordInput.type = 'password';
            toggleButton.textContent = 'Show';
            toggleButton.classList.remove('bg-indigo-700', 'text-white');
            toggleButton.classList.add('bg-indigo-100', 'text-indigo-700');
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
        typingIndicator.classList.add('animate-pulse');

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
            typingIndicator.classList.remove('animate-pulse');

            if (data.error) {
                console.error('Error:', data.error);
                return;
            }
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            typingIndicator.classList.add('hidden');
            typingIndicator.classList.remove('animate-pulse');
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
            colorClass = 'bg-gradient-to-r from-red-400 to-red-600 shadow-md shadow-red-200';
            bgClass = 'bg-red-50 bg-opacity-80';
            strengthCategory.className = 'text-center text-xl sm:text-2xl font-bold text-red-600 transition-all duration-500';
            percentText = `${score}%`;
        } else if (score < 50) {
            colorClass = 'bg-gradient-to-r from-orange-300 to-orange-500 shadow-md shadow-orange-200';
            bgClass = 'bg-orange-50 bg-opacity-80';
            strengthCategory.className = 'text-center text-xl sm:text-2xl font-bold text-orange-600 transition-all duration-500';
            percentText = `${score}%`;
        } else if (score < 75) {
            colorClass = 'bg-gradient-to-r from-yellow-300 to-yellow-500 shadow-md shadow-yellow-200';
            bgClass = 'bg-yellow-50 bg-opacity-80';
            strengthCategory.className = 'text-center text-xl sm:text-2xl font-bold text-yellow-600 transition-all duration-500';
            percentText = `${score}%`;
        } else if (score < 90) {
            colorClass = 'bg-gradient-to-r from-green-300 to-green-500 shadow-md shadow-green-200';
            bgClass = 'bg-green-50 bg-opacity-80';
            strengthCategory.className = 'text-center text-xl sm:text-2xl font-bold text-green-600 transition-all duration-500';
            percentText = `${score}%`;
        } else {
            colorClass = 'bg-gradient-to-r from-emerald-300 to-emerald-600 shadow-md shadow-emerald-200';
            bgClass = 'bg-emerald-50 bg-opacity-80';
            strengthCategory.className = 'text-center text-xl sm:text-2xl font-bold text-emerald-600 transition-all duration-500';
            percentText = `${score}%`;
        }

        strengthProgress.className = `h-7 rounded-full pl-3 transition-all duration-1000 ease-out relative ${colorClass} flex items-center`;
        strengthProgress.style.width = '0%'; // Start at 0 for animation
        strengthCategory.textContent = categoryName;

        setTimeout(() => {
            strengthProgress.style.width = `${score}%`;
            strengthProgress.innerHTML = `
                <span class="text-xs font-bold text-white drop-shadow-sm flex items-center">
                    ${percentText}
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 ml-1 ${score < 50 ? 'opacity-70' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${score < 50 ? 'M13 17h8m0 0V9m0 8l-8-8-4 4-6-6' : 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6'}" />
                    </svg>
                </span>`;
        }, 50);

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

         aiReasoning.textContent = '';
         aiReasoningSection.classList.remove('hidden');


          if (currentTypingAnimation) {
                clearTimeout(currentTypingAnimation);
                currentTypingAnimation = null;
              }

          let i = 0;
          const speed = 10;

          function typeWriter() {
                if (i < aiReasoningText.length) {
                aiReasoning.textContent += aiReasoningText.charAt(i);
                i++;
                currentTypingAnimation = setTimeout(typeWriter, speed);
            } else {
                currentTypingAnimation = null;
                }
          }

            typeWriter();
        } else {
      aiReasoningSection.classList.add('hidden');
    }

        if (data.attack_vectors && data.attack_vectors.length > 0) {
            attackVectors.innerHTML = '';

            data.attack_vectors.forEach((attack, index) => {
                let riskColorClass = '';
                let riskIcon = '';
                let riskBorderClass = '';
                let riskBgClass = '';

                if (attack.type && attack.type.toLowerCase().includes('brute_force')) {
                    riskColorClass = 'text-red-800';
                    riskBorderClass = 'border-red-400';
                    riskBgClass = 'bg-red-50/90';
                    riskIcon = `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>`;
                } else if (attack.type && attack.type.toLowerCase().includes('dictionary')) {
                    riskColorClass = 'text-orange-800';
                    riskBorderClass = 'border-orange-400';
                    riskBgClass = 'bg-orange-50/90';
                    riskIcon = `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-orange-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>`;
                } else {
                    riskColorClass = 'text-yellow-800';
                    riskBorderClass = 'border-yellow-400';
                    riskBgClass = 'bg-yellow-50/90';
                    riskIcon = `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>`;
                }

                const attackElement = document.createElement('li');
                attackElement.className = `p-4 rounded-lg  ${riskBorderClass} ${riskBgClass} ${riskColorClass} shadow-sm transition-all transform opacity-0 translate-y-4 hover:shadow-md hover:scale-[1.01] duration-300 ease-out`;
                attackElement.innerHTML = `
                    <div class="flex items-center">
                        ${riskIcon}
                        <h4 class="font-medium text-sm sm:text-base">${attack.name || 'Unknown Attack'}</h4>
                    </div>
                    <p class="mt-2 text-xs sm:text-sm">${attack.description || 'No description available'}</p>
                    <p class="mt-2 text-xs sm:text-sm font-medium">${attack.reasoning || ''}</p>
                `;

                attackVectors.appendChild(attackElement);

                setTimeout(() => {
                    attackElement.classList.remove('opacity-0', 'translate-y-4');
                }, 100 * index);
            });

            attackVectorsSection.classList.remove('hidden');
        } else {
            attackVectorsSection.classList.add('hidden');
        }

        analysisDetails.innerHTML = '';

        const tableHeader = document.createElement('tr');
        tableHeader.className = 'bg-gray-50/80';
        tableHeader.innerHTML = `
            <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Attribute</th>
            <th class="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Value</th>
        `;
        analysisDetails.appendChild(tableHeader);

        function addAnalysisRow(label, value) {
            const row = document.createElement('tr');
            row.className = 'border-t border-gray-100 hover:bg-gray-50/50 transition-colors duration-150';
            row.innerHTML = `
                <td class="py-3 pl-3 pr-2 text-gray-700 text-xs sm:text-sm">${label}</td>
                <td class="py-3 px-3 font-medium text-xs sm:text-sm">${value}</td>
            `;
            analysisDetails.appendChild(row);
        }

        if ('length' in analysis) {
            addAnalysisRow('Password length', `
                <span class="flex items-center">
                    <span class="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full mr-2">${analysis.length}</span>
                    characters
                </span>
            `);
        }

        if ('entropy' in analysis) {
            addAnalysisRow('Entropy', `
                <span class="flex items-center">
                    <span class="bg-purple-100 text-purple-800 text-xs font-medium px-2.5 py-0.5 rounded-full mr-2">${analysis.entropy.toFixed(2)}</span>
                    bits
                </span>
            `);
        }

        if ('crack_time' in analysis && 'crack_time_display' in analysis.crack_time) {
            addAnalysisRow('Time to crack', `
                <span class="font-mono bg-gray-100 text-gray-800 px-2 py-0.5 rounded">${analysis.crack_time.crack_time_display}</span>
            `);
        }

        function formatYesNo(value) {
            if (value) {
                return `
                    <span class="flex items-center text-green-600 font-medium">
                        <span class="inline-flex items-center justify-center w-5 h-5 mr-2 bg-green-100 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                            </svg>
                        </span>
                        <span>Yes</span>
                    </span>`;
            } else {
                return `
                    <span class="flex items-center text-red-500 font-medium">
                        <span class="inline-flex items-center justify-center w-5 h-5 mr-2 bg-red-100 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </span>
                        <span>No</span>
                    </span>`;
            }
        }

        if ('has_uppercase' in analysis) {
            addAnalysisRow('Contains uppercase letters', formatYesNo(analysis.has_uppercase));
        }

        if ('has_lowercase' in analysis) {
            addAnalysisRow('Contains lowercase letters', formatYesNo(analysis.has_lowercase));
        }

        if ('has_digit' in analysis) {
            addAnalysisRow('Contains digits', formatYesNo(analysis.has_digit));
        }

        if ('has_special' in analysis) {
            addAnalysisRow('Contains special characters', formatYesNo(analysis.has_special));
        }

        if ('common_patterns' in analysis && analysis.common_patterns && analysis.common_patterns.length > 0) {
            addAnalysisRow('Common patterns found', `
                <span class="text-red-600 font-medium flex items-center">
                    <span class="inline-flex items-center justify-center w-5 h-5 mr-2 bg-red-100 rounded-full">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                    </span>
                    ${analysis.common_patterns.join(', ')}
                </span>`
            );
        }

        suggestions.innerHTML = '';

        const suggestionContainer = document.createElement('div');
        suggestionContainer.className = 'space-y-3';

        if (data.improved_suggestion) {
            const suggestedPasswordEl = document.createElement('li');
            suggestedPasswordEl.className = 'bg-green-100 p-4 rounded-lg text-green-800  shadow-sm transform opacity-0 translate-y-4 transition-all duration-500 ease-out';
            suggestedPasswordEl.innerHTML = `
                <div class="flex items-start">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div>
                        <div class="font-medium">Suggested stronger password:</div>
                        <div class="mt-2 font-mono bg-white/80 px-3 py-2 rounded-md border border-green-200 text-sm shadow-inner">${data.improved_suggestion}</div>
                    </div>
                </div>
            `;
            suggestionContainer.appendChild(suggestedPasswordEl);
            setTimeout(() => {
                suggestedPasswordEl.classList.remove('opacity-0', 'translate-y-4');
            }, 100);
        }

        if (data.suggestions && data.suggestions.length > 0) {
            data.suggestions.forEach((suggestion, index) => {
                const suggestionEl = document.createElement('li');
                suggestionEl.className = 'bg-blue-100 p-4 rounded-lg text-indigo-800  shadow-sm transform opacity-0 translate-y-4 transition-all duration-500 ease-out';
                suggestionEl.innerHTML = `
                    <div class="flex items-start">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-500 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="text-xs sm:text-sm">${suggestion}</div>
                    </div>
                `;
                suggestionContainer.appendChild(suggestionEl);
                setTimeout(() => {
                    suggestionEl.classList.remove('opacity-0', 'translate-y-4');
                }, 150 + (100 * index));
            });
        } else if (!data.improved_suggestion) {
            const goodPasswordEl = document.createElement('li');
            goodPasswordEl.className = 'bg-green-100 p-4 rounded-lg text-green-800  shadow-sm transform opacity-0 translate-y-4 transition-all duration-500 ease-out';
            goodPasswordEl.innerHTML = `
                <div class="flex items-start">
                    <div class="flex-shrink-0 h-5 w-5 relative mr-2">
                        <span class="animate-ping absolute h-full w-full rounded-full bg-green-400 opacity-75"></span>
                        <svg xmlns="http://www.w3.org/2000/svg" class="relative h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                    </div>
                    <div class="font-medium">Your password looks good!</div>
                </div>
            `;
            suggestionContainer.appendChild(goodPasswordEl);

            setTimeout(() => {
                goodPasswordEl.classList.remove('opacity-0', 'translate-y-4');
            }, 100);
        }
        suggestions.appendChild(suggestionContainer);
        showResults();
    }

    function showResults() {
        results.style.display = 'block';

        results.classList.add('animate-results-appear');

        if (!document.querySelector('#custom-animations')) {
            const styleEl = document.createElement('style');
            styleEl.id = 'custom-animations';
            styleEl.textContent = `
                @keyframes resultsAppear {
                    0% {
                        opacity: 0;
                        transform: translateY(20px) scale(0.98);
                        box-shadow: 0 0px 0px rgba(0,0,0,0.05);
                    }
                    50% {
                        box-shadow: 0 15px 20px rgba(0,0,0,0.05);
                    }
                    100% {
                        opacity: 1;
                        transform: translateY(0) scale(1);
                        box-shadow: 0 10px 15px rgba(0,0,0,0.05);
                    }
                }
                .animate-results-appear {
                    animation: resultsAppear 0.5s ease-out forwards;
                }
                
                @keyframes resultsDisappear {
                    0% {
                        opacity: 1;
                        transform: translateY(0) scale(1);
                    }
                    100% {
                        opacity: 0;
                        transform: translateY(20px) scale(0.98);
                    }
                }
                .animate-results-disappear {
                    animation: resultsDisappear 0.4s ease-in forwards;
                }
                
                @keyframes typing-dots {
                    0% { content: ""; }
                    25% { content: "."; }
                    50% { content: ".."; }
                    75% { content: "..."; }
                    100% { content: ""; }
                }
                .typing-dots::after {
                    content: "";
                    animation: typing-dots 1.5s infinite;
                }
                
                .transition-height {
                    transition: max-height 0.5s ease-out;
                }
            `;
            document.head.appendChild(styleEl);
        }

        const allTypingIndicators = document.querySelectorAll('.typing-indicator');
        allTypingIndicators.forEach(indicator => {
            indicator.classList.add('typing-dots');
        });

        const sections = results.querySelectorAll('section');
        sections.forEach((section, index) => {
            section.classList.add('transform', 'opacity-0', 'translate-y-4');

            setTimeout(() => {
                section.classList.add('transition-all', 'duration-500', 'ease-out');
                section.classList.remove('opacity-0', 'translate-y-4');
                section.classList.add('hover:shadow-md', 'rounded-lg', 'transition-shadow', 'duration-300');
            }, 100 + (index * 75));
        });
    }

    function hideResults() {
        results.classList.remove('animate-results-appear');
        results.classList.add('animate-results-disappear');

        setTimeout(() => {
            results.style.display = 'none';
            results.classList.remove('animate-results-disappear');
        }, 400);
    }

    function setupAccordions() {
        const accordionHeaders = document.querySelectorAll('.accordion-header');

        accordionHeaders.forEach(header => {
            header.addEventListener('click', () => {
                const content = header.nextElementSibling;
                const icon = header.querySelector('.accordion-icon');

                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                    icon.classList.remove('rotate-180');
                } else {
                    content.style.maxHeight = content.scrollHeight + 'px';
                    icon.classList.add('rotate-180');
                }
            });
        });
    }

    if (document.querySelector('.accordion-header')) {
        setupAccordions();
    }

    function createRipple(event) {
        const button = event.currentTarget;

        const circle = document.createElement('span');
        const diameter = Math.max(button.clientWidth, button.clientHeight);
        const radius = diameter / 2;

        circle.style.width = circle.style.height = `${diameter}px`;
        circle.style.left = `${event.clientX - button.getBoundingClientRect().left - radius}px`;
        circle.style.top = `${event.clientY - button.getBoundingClientRect().top - radius}px`;
        circle.classList.add('ripple');

        const ripple = button.querySelector('.ripple');

        if (ripple) {
            ripple.remove();
        }

        button.appendChild(circle);
    }

    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', createRipple);
    });

    if (!document.querySelector('#ripple-styles')) {
        const rippleStyles = document.createElement('style');
        rippleStyles.id = 'ripple-styles';
        rippleStyles.textContent = `
            .btn {
                position: relative;
                overflow: hidden;
            }
            
            .ripple {
                position: absolute;
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s linear;
                background-color: rgba(255, 255, 255, 0.7);
            }
            
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(rippleStyles);
    }
});