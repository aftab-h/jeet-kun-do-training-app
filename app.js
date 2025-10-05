// Jeet Kune Do Flashcard App - Web Version
let flashcards = [];
let currentCard = null;
let score = 0;
let totalAnswered = 0;
let currentAnswers = [];
let correctAnswer = '';

// DOM Elements
const questionText = document.getElementById('question-text');
const scoreDisplay = document.getElementById('score-display');
const conceptDisplay = document.getElementById('concept-display');
const feedbackEl = document.getElementById('feedback');
const nextBtn = document.getElementById('next-btn');
const sourceBtn = document.getElementById('source-btn');
const resetBtn = document.getElementById('reset-btn');
const answerButtons = [
    document.getElementById('answer-0'),
    document.getElementById('answer-1'),
    document.getElementById('answer-2'),
    document.getElementById('answer-3')
];

// Modal elements
const modal = document.getElementById('source-modal');
const modalTitle = document.getElementById('modal-title');
const sourceText = document.getElementById('source-text');
const closeModalBtn = document.getElementById('close-modal-btn');
const closeModalX = document.getElementById('close-modal');

// Load flashcards from JSON
async function loadFlashcards() {
    try {
        const response = await fetch('flashcards.json');
        flashcards = await response.json();
        console.log(`Loaded ${flashcards.length} flashcards`);
        nextQuestion();
    } catch (error) {
        console.error('Error loading flashcards:', error);
        questionText.textContent = 'Error loading flashcards. Please refresh the page.';
    }
}

// Shuffle array
function shuffle(array) {
    const newArray = [...array];
    for (let i = newArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
    }
    return newArray;
}

// Load next question
function nextQuestion() {
    // Reset UI
    feedbackEl.textContent = '';
    feedbackEl.className = 'feedback';
    nextBtn.disabled = true;
    sourceBtn.disabled = false;

    // Pick random flashcard
    currentCard = flashcards[Math.floor(Math.random() * flashcards.length)];

    // Update question
    questionText.textContent = currentCard.question_text;
    conceptDisplay.textContent = `Concept #${currentCard.concept_number}: ${currentCard.concept_name}`;

    // Prepare answers
    currentAnswers = shuffle([
        currentCard.correct_answer,
        currentCard.wrong_answer_1,
        currentCard.wrong_answer_2,
        currentCard.wrong_answer_3
    ]);
    correctAnswer = currentCard.correct_answer;

    // Update buttons
    answerButtons.forEach((btn, i) => {
        btn.textContent = `${String.fromCharCode(65 + i)}) ${currentAnswers[i]}`;
        btn.className = 'answer-btn';
        btn.disabled = false;
        btn.onclick = () => checkAnswer(currentAnswers[i], btn);
    });
}

// Check answer
function checkAnswer(selectedAnswer, selectedBtn) {
    const isCorrect = selectedAnswer === correctAnswer;

    // Update score
    totalAnswered++;
    if (isCorrect) {
        score++;
    }

    // Update score display
    const percentage = totalAnswered > 0 ? Math.round((score / totalAnswered) * 100) : 0;
    scoreDisplay.textContent = `Score: ${score}/${totalAnswered} (${percentage}%)`;

    // Update button colors and disable all
    answerButtons.forEach(btn => {
        const answerText = btn.textContent.substring(3); // Remove "A) ", "B) ", etc.

        if (answerText === correctAnswer) {
            btn.className = 'answer-btn correct';
        } else if (btn === selectedBtn && !isCorrect) {
            btn.className = 'answer-btn wrong';
        } else {
            btn.className = 'answer-btn other';
        }
        btn.disabled = true;
    });

    // Show feedback
    if (isCorrect) {
        feedbackEl.textContent = `✓ Correct! ${currentCard.explanation || ''}`;
        feedbackEl.className = 'feedback correct';
    } else {
        feedbackEl.textContent = `✗ Wrong. Correct answer: ${correctAnswer}. ${currentCard.explanation || ''}`;
        feedbackEl.className = 'feedback wrong';
    }

    // Enable next button
    nextBtn.disabled = false;
}

// Reset score
function resetScore() {
    if (confirm('Are you sure you want to reset your score?')) {
        score = 0;
        totalAnswered = 0;
        scoreDisplay.textContent = 'Score: 0/0 (0%)';
        nextQuestion();
    }
}

// Show source material
function showSourceMaterial() {
    if (!currentCard) return;

    const conceptNum = parseInt(currentCard.concept_number);
    const conceptName = currentCard.concept_name;
    const sourceTextContent = CONCEPT_TEXTS[conceptNum] || 'Source material not found.';

    modalTitle.textContent = `Concept #${conceptNum}: ${conceptName}`;
    sourceText.textContent = sourceTextContent;
    modal.classList.add('show');
}

// Close modal
function closeModal() {
    modal.classList.remove('show');
}

// Event listeners
nextBtn.addEventListener('click', nextQuestion);
resetBtn.addEventListener('click', resetScore);
sourceBtn.addEventListener('click', showSourceMaterial);
closeModalBtn.addEventListener('click', closeModal);
closeModalX.addEventListener('click', closeModal);

// Close modal when clicking outside
modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    } else if (e.key === 'Enter' && !nextBtn.disabled) {
        nextQuestion();
    } else if (e.key >= '1' && e.key <= '4') {
        const index = parseInt(e.key) - 1;
        if (!answerButtons[index].disabled) {
            answerButtons[index].click();
        }
    } else if (e.key.toLowerCase() === 's' && !sourceBtn.disabled) {
        showSourceMaterial();
    }
});

// Initialize app
loadFlashcards();
