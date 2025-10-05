#!/usr/bin/env python3
"""
Jeet Kune Do Flashcard Training App
A desktop application for studying JKD concepts using spaced repetition
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import random
from pathlib import Path


class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeet Kune Do Training - Flashcard App")
        self.root.geometry("900x750")
        self.root.configure(bg='#1a1a1a')

        # Data
        self.flashcards = []
        self.current_card = None
        self.score = 0
        self.total_answered = 0

        # Load flashcards
        self.load_flashcards()

        # UI Setup
        self.setup_ui()

        # Load first question
        self.next_question()

    def load_flashcards(self):
        """Load flashcards from CSV file"""
        csv_path = Path(__file__).parent / "data" / "jkd_flashcards.csv"

        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.flashcards = list(reader)

            if not self.flashcards:
                messagebox.showerror("Error", "No flashcards found in CSV file!")
                self.root.quit()
        except FileNotFoundError:
            messagebox.showerror("Error", f"Flashcard file not found at: {csv_path}")
            self.root.quit()

    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2d2d2d', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🥋 JEET KUNE DO TRAINING",
            font=('Arial', 24, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff'
        )
        title_label.pack(pady=15)

        # Score frame
        score_frame = tk.Frame(self.root, bg='#1a1a1a')
        score_frame.pack(fill='x', padx=10)

        self.score_label = tk.Label(
            score_frame,
            text="Score: 0/0 (0%)",
            font=('Arial', 14),
            bg='#1a1a1a',
            fg='#4CAF50'
        )
        self.score_label.pack(side='left')

        self.concept_label = tk.Label(
            score_frame,
            text="Concept: Loading...",
            font=('Arial', 12),
            bg='#1a1a1a',
            fg='#888888'
        )
        self.concept_label.pack(side='right')

        # Question frame
        question_frame = tk.Frame(self.root, bg='#2d2d2d', height=120)
        question_frame.pack(fill='both', padx=10, pady=20)
        question_frame.pack_propagate(False)

        self.question_label = tk.Label(
            question_frame,
            text="",
            font=('Arial', 16, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            wraplength=850,
            justify='center'
        )
        self.question_label.pack(expand=True, pady=20)

        # Answer buttons frame
        self.buttons_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.buttons_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.answer_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.buttons_frame,
                text="",
                font=('Arial', 14),
                bg='#e0e0e0',
                fg='#000000',
                activebackground='#d0d0d0',
                activeforeground='#000000',
                relief='flat',
                cursor='hand2',
                wraplength=800,
                justify='left',
                padx=20,
                pady=15
            )
            btn.pack(fill='x', pady=5)
            self.answer_buttons.append(btn)

        # Feedback frame
        self.feedback_frame = tk.Frame(self.root, bg='#1a1a1a', height=100)
        self.feedback_frame.pack(fill='x', padx=10, pady=5)
        self.feedback_frame.pack_propagate(False)

        self.feedback_label = tk.Label(
            self.feedback_frame,
            text="",
            font=('Arial', 12, 'italic'),
            bg='#1a1a1a',
            fg='#888888',
            wraplength=850
        )
        self.feedback_label.pack(expand=True)

        # Control buttons
        control_frame = tk.Frame(self.root, bg='#1a1a1a')
        control_frame.pack(fill='x', padx=10, pady=10)

        self.next_btn = tk.Button(
            control_frame,
            text="Next Question →",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='#ffffff',
            activebackground='#45a049',
            activeforeground='#ffffff',
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=10,
            command=self.next_question,
            state='disabled'
        )
        self.next_btn.pack(side='right')

        reset_btn = tk.Button(
            control_frame,
            text="Reset Score",
            font=('Arial', 12),
            bg='#f44336',
            fg='#ffffff',
            activebackground='#da190b',
            activeforeground='#ffffff',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10,
            command=self.reset_score
        )
        reset_btn.pack(side='left')

    def next_question(self):
        """Load next random question"""
        # Reset UI
        self.feedback_label.config(text="")
        self.next_btn.config(state='disabled')

        # Pick random flashcard
        self.current_card = random.choice(self.flashcards)

        # Update question
        self.question_label.config(text=self.current_card['question_text'])
        self.concept_label.config(text=f"Concept #{self.current_card['concept_number']}: {self.current_card['concept_name']}")

        # Prepare answers
        answers = [
            self.current_card['correct_answer'],
            self.current_card['wrong_answer_1'],
            self.current_card['wrong_answer_2'],
            self.current_card['wrong_answer_3']
        ]
        random.shuffle(answers)

        # Update buttons
        for i, btn in enumerate(self.answer_buttons):
            answer_text = answers[i]
            btn.config(
                text=f"{chr(65+i)}) {answer_text}",
                bg='#e0e0e0',
                fg='#000000',
                state='normal',
                command=lambda ans=answer_text: self.check_answer(ans)
            )

    def check_answer(self, selected_answer):
        """Check if the selected answer is correct"""
        correct_answer = self.current_card['correct_answer']
        is_correct = selected_answer == correct_answer

        # Update score
        self.total_answered += 1
        if is_correct:
            self.score += 1

        # Update score display
        percentage = int((self.score / self.total_answered) * 100) if self.total_answered > 0 else 0
        self.score_label.config(text=f"Score: {self.score}/{self.total_answered} ({percentage}%)")

        # Update button colors and disable all
        for btn in self.answer_buttons:
            answer_text = btn.cget('text')[3:]  # Remove "A) ", "B) ", etc.

            if answer_text == correct_answer:
                btn.config(bg='#4CAF50', fg='#000000', state='disabled')
            elif answer_text == selected_answer and not is_correct:
                btn.config(bg='#f44336', fg='#000000', state='disabled')
            else:
                btn.config(state='disabled', bg='#888888', fg='#000000')

        # Show feedback
        if is_correct:
            self.feedback_label.config(
                text=f"✓ Correct! {self.current_card.get('explanation', '')}",
                fg='#4CAF50'
            )
        else:
            self.feedback_label.config(
                text=f"✗ Wrong. Correct answer: {correct_answer}. {self.current_card.get('explanation', '')}",
                fg='#f44336'
            )

        # Enable next button
        self.next_btn.config(state='normal')

    def reset_score(self):
        """Reset the score counter"""
        if messagebox.askyesno("Reset Score", "Are you sure you want to reset your score?"):
            self.score = 0
            self.total_answered = 0
            self.score_label.config(text="Score: 0/0 (0%)")
            self.next_question()


def main():
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
