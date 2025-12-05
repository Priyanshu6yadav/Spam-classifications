/* ==========================================
   SPAM CLASSIFIER - JAVASCRIPT
   AJAX Prediction & Dynamic UI Management
   ========================================== */

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    updateCharacterCount();
});

/**
 * Setup event listeners for form and inputs
 */
function setupEventListeners() {
    const form = document.getElementById('spamForm');
    const messageInput = document.getElementById('message');

    // Form submission
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        classifyMessage();
    });

    // Character count update
    messageInput.addEventListener('input', updateCharacterCount);

    // Prevent form submission on Enter key if exceeds max length
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            form.dispatchEvent(new Event('submit'));
        }
    });

    // Add floating animation to icon on load
    addFloatAnimation();
}

/**
 * Add floating animation to shield icon
 */
function addFloatAnimation() {
    const icon = document.querySelector('i.fa-shield-alt');
    if (icon) {
        icon.classList.add('float-icon');
    }
}

/**
 * Update the character count display
 */
function updateCharacterCount() {
    const messageInput = document.getElementById('message');
    const charCount = document.getElementById('charCount');
    
    const count = messageInput.value.length;
    charCount.textContent = count;
    
    // Change color based on character count
    if (count > 4500) {
        charCount.classList.add('text-red-500');
        charCount.classList.remove('text-cyan-400');
    } else {
        charCount.classList.remove('text-red-500');
        charCount.classList.add('text-cyan-400');
    }
}

/**
 * Main classification function
 * Sends the message to the backend and handles the response
 */
async function classifyMessage() {
    const message = document.getElementById('message').value.trim();
    const submitBtn = document.getElementById('submitBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsContainer = document.getElementById('resultsContainer');
    const errorContainer = document.getElementById('errorContainer');
    const infoContainer = document.getElementById('infoContainer');

    // Validation
    if (!message) {
        showError('Please enter a message to classify.');
        return;
    }

    if (message.length > 5000) {
        showError('Message is too long. Please limit to 5000 characters.');
        return;
    }

    try {
        // Show loading state
        submitBtn.disabled = true;
        loadingSpinner.classList.remove('hidden');
        resultsContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        infoContainer.classList.add('hidden');

        // Make API request
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Hide loading spinner
        loadingSpinner.classList.add('hidden');

        if (data.error) {
            // Show error message
            showError(data.message);
        } else {
            // Display results
            displayResults(data);
            resultsContainer.classList.remove('hidden');
        }

    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please try again later.');
        loadingSpinner.classList.add('hidden');
    } finally {
        submitBtn.disabled = false;
    }
}

/**
 * Display classification results
 * @param {Object} data - Response data from backend
 */
function displayResults(data) {
    const statusBadge = document.getElementById('statusBadge');
    const spamConfidence = document.getElementById('spamConfidence');
    const hamConfidence = document.getElementById('hamConfidence');
    const spamBar = document.getElementById('spamBar');
    const hamBar = document.getElementById('hamBar');
    const analysisText = document.getElementById('analysisText');

    const isSpam = data.status === 'spam';

    // Update status badge
    if (isSpam) {
        statusBadge.className = 'p-6 rounded-2xl text-center font-bold text-xl border-2 danger-badge';
        statusBadge.innerHTML = '<i class="fas fa-exclamation-triangle mr-3"></i>🚨 SPAM DETECTED';
    } else {
        statusBadge.className = 'p-6 rounded-2xl text-center font-bold text-xl border-2 success-badge';
        statusBadge.innerHTML = '<i class="fas fa-check-circle mr-3"></i>💬 LEGITIMATE MESSAGE';
    }

    // Update confidence values
    spamConfidence.textContent = data.spam_confidence.toFixed(1);
    hamConfidence.textContent = data.ham_confidence.toFixed(1);

    // Animate progress bars
    spamBar.style.width = data.spam_confidence + '%';
    hamBar.style.width = data.ham_confidence + '%';

    // Update analysis text
    analysisText.textContent = generateAnalysisText(data);

    // Add smooth transitions
    spamBar.style.transition = 'width 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
    hamBar.style.transition = 'width 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
}

/**
 * Generate AI analysis text based on classification
 * @param {Object} data - Response data from backend
 * @returns {string} Analysis text
 */
function generateAnalysisText(data) {
    const isSpam = data.status === 'spam';
    const confidence = data.confidence;
    
    let analysis = '';
    
    if (isSpam) {
        if (confidence >= 95) {
            analysis = 'This message exhibits very strong characteristics of spam with extremely high confidence. It contains typical spam patterns and is highly likely to be malicious or unwanted content.';
        } else if (confidence >= 85) {
            analysis = 'This message shows strong spam indicators with high confidence. It likely contains suspicious patterns, promotional content, or phishing attempts.';
        } else if (confidence >= 70) {
            analysis = 'This message has moderate to high spam indicators. While it shows spam characteristics, there\'s a chance it could be a legitimate message with some unusual patterns.';
        } else {
            analysis = 'This message appears to be spam, but with moderate confidence. It contains some spam-like patterns mixed with potentially legitimate content.';
        }
    } else {
        if (confidence >= 95) {
            analysis = 'This message is almost certainly legitimate. It exhibits strong characteristics of authentic, non-spam communication with excellent confidence levels.';
        } else if (confidence >= 85) {
            analysis = 'This message is highly likely to be legitimate. It shows clear patterns of genuine communication with high confidence.';
        } else if (confidence >= 70) {
            analysis = 'This message appears to be legitimate with good confidence. While it shows mostly genuine communication patterns, there are some unusual elements.';
        } else {
            analysis = 'This message is likely legitimate, but with moderate confidence. It has mostly genuine patterns with some ambiguous characteristics.';
        }
    }
    
    return analysis;
}

/**
 * Display error message
 * @param {string} errorMessage - Error message to display
 */
function showError(errorMessage) {
    const errorContainer = document.getElementById('errorContainer');
    const errorText = document.getElementById('errorText');
    const resultsContainer = document.getElementById('resultsContainer');
    const infoContainer = document.getElementById('infoContainer');

    errorText.textContent = errorMessage;
    errorContainer.classList.remove('hidden');
    resultsContainer.classList.add('hidden');
    infoContainer.classList.add('hidden');
}

/**
 * Clear error message
 */
function clearError() {
    const errorContainer = document.getElementById('errorContainer');
    const infoContainer = document.getElementById('infoContainer');

    errorContainer.classList.add('hidden');
    infoContainer.classList.remove('hidden');
}

/**
 * Clear results and reset form
 */
function clearResults() {
    const messageInput = document.getElementById('message');
    const resultsContainer = document.getElementById('resultsContainer');
    const infoContainer = document.getElementById('infoContainer');

    messageInput.value = '';
    messageInput.focus();
    resultsContainer.classList.add('hidden');
    infoContainer.classList.remove('hidden');
    updateCharacterCount();
}

/**
 * Validate message format before submission
 * @param {string} message - Message to validate
 * @returns {boolean} True if valid, false otherwise
 */
function validateMessage(message) {
    if (!message || message.trim().length === 0) {
        return false;
    }
    
    if (message.length > 5000) {
        return false;
    }
    
    // Additional validation: check for common non-text characters
    // This is optional and can be customized
    
    return true;
}

/**
 * Format confidence value for display
 * @param {number} value - Confidence value (0-100)
 * @returns {string} Formatted confidence string
 */
function formatConfidence(value) {
    return value.toFixed(1) + '%';
}

/**
 * Add visual feedback on button click
 */
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('button');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Prevent multiple ripples
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
        });
    });
});

/**
 * Add keyboard shortcut support
 */
document.addEventListener('keydown', (e) => {
    // Ctrl+Enter to submit
    if (e.ctrlKey && e.key === 'Enter') {
        const form = document.getElementById('spamForm');
        const messageInput = document.getElementById('message');
        
        if (messageInput === document.activeElement) {
            classifyMessage();
        }
    }
    
    // Escape to clear
    if (e.key === 'Escape') {
        const resultsContainer = document.getElementById('resultsContainer');
        if (!resultsContainer.classList.contains('hidden')) {
            clearResults();
        }
    }
});

/**
 * Add theme toggle support (optional)
 */
function toggleTheme() {
    document.body.classList.toggle('dark-mode');
}

/**
 * Log classification statistics (for analytics)
 */
function logClassification(data) {
    console.log('Classification logged:', {
        timestamp: new Date().toISOString(),
        status: data.status,
        confidence: data.confidence,
        spamConfidence: data.spam_confidence,
        hamConfidence: data.ham_confidence
    });
}

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        classifyMessage,
        displayResults,
        clearResults,
        validateMessage,
        generateAnalysisText
    };
}
