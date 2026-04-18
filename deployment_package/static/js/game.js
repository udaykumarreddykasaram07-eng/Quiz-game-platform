// ========================================
// QUIZ GAME JAVASCRIPT
// ========================================

// Global variables
let currentQuestionIndex = 0;
let timerInterval = null;
let seconds = 0;
let userAnswers = {};
let questions = [];

// Initialize quiz on page load
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the play quiz page
    if (document.getElementById('quiz-form')) {
        initializeQuiz();
    }
    
    // Add event listeners for answer selection
    addAnswerEventListeners();
});

// Initialize quiz
function initializeQuiz() {
    // Start timer
    startTimer();
    
    // Get all questions
    const questionBoxes = document.querySelectorAll('.question-box');
    questions = Array.from(questionBoxes);
    
    // Hide all questions except first
    questions.forEach((box, index) => {
        if (index > 0) {
            box.style.display = 'none';
        }
    });
    
    // Show current question number
    updateQuestionCounter();
    
    // Add keyboard shortcuts
    addKeyboardShortcuts();
}

// Start timer
function startTimer() {
    timerInterval = setInterval(() => {
        seconds++;
        updateTimerDisplay();
    }, 1000);
}

// Update timer display
function updateTimerDisplay() {
    const timerElement = document.getElementById('timer');
    if (timerElement) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
}

// Update question counter
function updateQuestionCounter() {
    const counterElement = document.getElementById('current-question');
    if (counterElement) {
        counterElement.textContent = currentQuestionIndex + 1;
    }
}

// Next question
function nextQuestion() {
    // Validate answer
    const currentQuestionBox = questions[currentQuestionIndex];
    const questionId = currentQuestionBox.dataset.questionId;
    const selectedOption = document.querySelector(`input[name="q${questionId}"]:checked`);
    
    if (!selectedOption && currentQuestionIndex < questions.length - 1) {
        alert('Please select an answer before proceeding!');
        return;
    }
    
    // Save answer
    if (selectedOption) {
        userAnswers[questionId] = selectedOption.value;
    }
    
    // Hide current question
    currentQuestionBox.style.display = 'none';
    
    // Show next question
    currentQuestionIndex++;
    
    if (currentQuestionIndex < questions.length) {
        questions[currentQuestionIndex].style.display = 'block';
        updateQuestionCounter();
        
        // Show/hide previous button
        updateNavigationButtons();
        
        // Scroll to top
        window.scrollTo(0, 0);
        
        // Add animation
        questions[currentQuestionIndex].classList.add('slide-in-right');
        setTimeout(() => {
            questions[currentQuestionIndex].classList.remove('slide-in-right');
        }, 500);
    } else {
        // Last question - submit quiz
        document.getElementById('quiz-form').submit();
    }
}

// Previous question
function prevQuestion() {
    if (currentQuestionIndex > 0) {
        // Hide current question
        questions[currentQuestionIndex].style.display = 'none';
        
        // Show previous question
        currentQuestionIndex--;
        questions[currentQuestionIndex].style.display = 'block';
        
        updateQuestionCounter();
        updateNavigationButtons();
        
        // Scroll to top
        window.scrollTo(0, 0);
        
        // Add animation
        questions[currentQuestionIndex].classList.add('slide-in-left');
        setTimeout(() => {
            questions[currentQuestionIndex].classList.remove('slide-in-left');
        }, 500);
    }
}

// Update navigation buttons
function updateNavigationButtons() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    if (prevBtn) {
        if (currentQuestionIndex === 0) {
            prevBtn.style.display = 'none';
        } else {
            prevBtn.style.display = 'inline-block';
        }
    }
    
    if (nextBtn) {
        if (currentQuestionIndex === questions.length - 1) {
            nextBtn.innerHTML = '<i class="fas fa-check"></i> Submit Quiz';
        } else {
            nextBtn.innerHTML = 'Next Question <i class="fas fa-arrow-right"></i>';
        }
    }
}

// Add event listeners for answer selection
function addAnswerEventListeners() {
    // Add click event to all option labels
    document.querySelectorAll('.option').forEach(option => {
        option.addEventListener('click', function() {
            // Find the radio input inside this label
            const radio = this.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
                
                // Add visual feedback
                this.parentElement.querySelectorAll('.option').forEach(opt => {
                    opt.classList.remove('selected');
                });
                this.classList.add('selected');
                
                // Show checkmark animation
                showCheckmarkAnimation(this);
            }
        });
    });
}

// Show checkmark animation
function showCheckmarkAnimation(element) {
    // Create checkmark element
    const checkmark = document.createElement('div');
    checkmark.className = 'checkmark-animation';
    checkmark.innerHTML = '<i class="fas fa-check"></i>';
    element.appendChild(checkmark);
    
    // Animate and remove
    setTimeout(() => {
        checkmark.style.opacity = '0';
        setTimeout(() => {
            checkmark.remove();
        }, 300);
    }, 800);
}

// Add keyboard shortcuts
function addKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // '1', '2', '3', '4' keys to select options
        if (e.key >= '1' && e.key <= '4') {
            const optionIndex = parseInt(e.key) - 1;
            const currentQuestionBox = questions[currentQuestionIndex];
            const options = currentQuestionBox.querySelectorAll('.option input[type="radio"]');
            
            if (options[optionIndex]) {
                options[optionIndex].checked = true;
                
                // Trigger click on parent label
                const label = options[optionIndex].closest('.option');
                if (label) {
                    label.click();
                }
            }
        }
        
        // 'ArrowRight' or 'Enter' to go to next question
        if (e.key === 'ArrowRight' || e.key === 'Enter') {
            e.preventDefault();
            nextQuestion();
        }
        
        // 'ArrowLeft' to go to previous question
        if (e.key === 'ArrowLeft') {
            e.preventDefault();
            prevQuestion();
        }
    });
}

// Validate form before submission
function validateQuizForm() {
    const form = document.getElementById('quiz-form');
    if (!form) return true;
    
    // Check if all questions are answered
    const allQuestionsAnswered = Array.from(questions).every((questionBox, index) => {
        const questionId = questionBox.dataset.questionId;
        const selectedOption = document.querySelector(`input[name="q${questionId}"]:checked`);
        return selectedOption !== null;
    });
    
    if (!allQuestionsAnswered) {
        alert('Please answer all questions before submitting!');
        return false;
    }
    
    return true;
}

// Progress bar functionality
function updateProgressBar() {
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
        progressBar.style.width = `${progress}%`;
    }
}

// Auto-save answers (optional feature)
function autoSaveAnswers() {
    setInterval(() => {
        if (Object.keys(userAnswers).length > 0) {
            localStorage.setItem('quizAnswers', JSON.stringify(userAnswers));
            console.log('Answers auto-saved');
        }
    }, 30000); // Save every 30 seconds
}

// Restore saved answers
function restoreSavedAnswers() {
    const saved = localStorage.getItem('quizAnswers');
    if (saved) {
        userAnswers = JSON.parse(saved);
        console.log('Answers restored');
    }
}

// Clear saved answers
function clearSavedAnswers() {
    localStorage.removeItem('quizAnswers');
}

// Submit quiz with confirmation
function submitQuizWithConfirmation() {
    if (confirm('Are you sure you want to submit your quiz? You cannot change your answers after submission.')) {
        clearSavedAnswers();
        document.getElementById('quiz-form').submit();
    }
}

// Time warning (when time is running out)
function checkTimeWarning() {
    setInterval(() => {
        const timerElement = document.getElementById('timer');
        if (timerElement) {
            const timeText = timerElement.textContent;
            const minutes = parseInt(timeText.split(':')[0]);
            
            if (minutes >= 10) {
                timerElement.style.color = '#ef4444'; // Red
                timerElement.classList.add('pulse');
            } else if (minutes >= 5) {
                timerElement.style.color = '#f59e0b'; // Orange
            }
        }
    }, 1000);
}

// Initialize all features
function initializeQuizFeatures() {
    restoreSavedAnswers();
    autoSaveAnswers();
    checkTimeWarning();
}

// Export functions for use in templates
window.quizGame = {
    nextQuestion,
    prevQuestion,
    submitQuizWithConfirmation,
    validateQuizForm
};