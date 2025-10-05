#!/usr/bin/env python3
"""
Jeet Kune Do Flashcard Training App
A desktop application for studying JKD concepts using spaced repetition
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import csv
import random
from pathlib import Path


# JKD Concept Source Material - extracted from PDF
CONCEPT_TEXTS = {
    1: """Centerline Theory

1. The centerline is an imaginary vertical line that runs along the center of the body.
2. The primary targets on the centerline are the eyes, throat, groin and knees.
3. The secondary targets are the nose, mouth, chin, sternum, solar plexus, stomach, liver, inner thigh, outer thigh, shin, and instep.
4. Targets in the back are the head, neck, spine, tailbone, hamstrings, back of the knee, and Achilles tendon.
5. All offense is directed to the centerline.
6. All defense originates from the centerline.
7. All footwork is designed to intercept the centerline.
8. In emptiness, you hit in a straight line.
9. Control, occupy, and defend the centerline at all times.
10. Your objective is to hit the centerline, without being hit yourself.
11. Centerline control uses economy of motion. Keeping both hands on the centerline will minimize all defensive motions.
12. All actions in Jeet Kune Do focus on the centerline.""",

    2: """Economy of Motion Theory

1. Combat must be simple, direct, and non-classical (non-traditional).
2. Motions should be economical, not overly complicated, and should go directly to the target
3. Your actions must have no wasted energy and unnecessary motion. Use the least possible movement to hit your goal.
4. The shortest distance between two points is a straight line – so stay straight.""",

    3: """Four Ranges of Combat

1. Kicking – distance where you can only make contact with your legs or feet
2. Punching – distance where you can score with your lead hand
3. Trapping – distance where you can clinch his neck tightly
4. Grappling/Ground Fighting – distance where you can throw and ground fight""",

    4: """Fighting Measure (Proper Distance) Theory

1. The distance you want to maintain & control against an opponent.
2. Proper distance is where he can't touch you without first taking a step or making a big motion.
3. We avoid starting the fight in "trading blows" range.
4. Maintain a 360 circle of awareness and avoid "tunnel vision".""",

    5: """Power Side Forward Theory

1. Lead with your dominant side; you can hit harder, faster, and more accurately; weak side is in the rear, which gives it more power from hip rotation.
2. Both hands have "knockout" power – there is no "weak hand."
3. Bruce Lee took this concept from Fencing.""",

    6: """Forward Pressure Theory

1. Powerful driving energy pushes him back, forcing him to backpedal.
2. You must destroy his Base and Balance.
3. The Straight Blast and Boxing Combos are often used to create pressure.
4. Apply constant forward pressure against your opponent, which is like water flowing through the smallest crack seeking an opening. Whether your opponent retreats or advances, he should feel an "Alive" tension against his arms or body at all times, affecting his motions and restricting him.""",

    7: """Non-Telegraphic Motion Theory

1. Never show him what you are about to do before you do it: do not alert him.
2. Never show him anything. Telegraphing can be physical, emotional, and psychological, so clean up your communication.
3. Hit from where you are; there is no reset before striking.""",

    8: """Simultaneous Attack & Defense (Lin Sil Dai Da) Theory

1. Attack at the same time you defend. Offense and defense are one, not two.
2. By attacking & defending at the same time, your move is a one-count motion.
3. Your defense is also your attack. Treat his attack as an opportunity to counter-attack. Instead of blocking and then returning a strike, we block and strike at the same time.
4. JKD is an offensive style – we prefer a pre-emptive approach. If you hit him before he hits you, then you prevent him from leading the dance.""",

    9: """Visual Focus Principles

1. Where you look at during a fight
2. Make sure to widen your field of vision - avoid focal vision
3. Primary Visual Focus – his solar plexus
4. Secondary Visual Focus – his head
5. Tertiary Visual Focus – his elbows (for punches) and knees (for kicks)""",

    10: """Time-Distance Variable

1. The less distance you have from him, the less time you have to react.
2. The more distance you have from him, the more time you have to react.
3. Defensively, you want more distance from him to give you more reaction time.
4. Offensively, you want to close distance on him quickly to give him no reaction time.""",

    11: """9-Second Rule

1. You must end the fight in less than 9 seconds, or the odds of winning go down dramatically.
2. The longer the fight, the odds increase that you will end up on the ground, weapons will be drawn, and multiple enemies will attack you.""",

    12: """Worst-Case Scenario Theory

1. Always train as if the enemy is bigger, stronger, and tougher than you.
2. Always assume your enemy has a weapon, even if you cannot see it.
3. Always assume your enemy has friends coming to help him
4. Don't underestimate anyone""",

    13: """Four Corners Theory

1. The four corners are imaginary boundaries in which your hands operate.
2. The hands never go outside these boundaries.
3. The concept is to allow the opponent to enter one of the four corners and then close the gate upon the attack.
4. By not going outside of one's boundaries, one learns not to chase the illusive opponent – do not chase the attacking tool. Let it come to you.
5. The four corners are High Outside, Low Outside, High Inside, and Low Inside.""",

    14: """Three Attack Lines Theory

1. Attack Line 1 – Centerline (Attack is Straight)
2. Attack Line 2 – Slanted (Attack is Angled to Opposite Shoulder)
3. Attack Line 3 – Lateral Line (Attack Comes from the Side of the Head)""",

    15: """Five Ways of Attack

1. S.A.A./S.D.A. – Single Angular Attack/Single Direct Attack
2. A.B.C. – Attack by Combination
3. H.I.A./F.I.A. – Hand/Foot Immobilization Attack (Trapping)
4. P.I.A. – Progressive Indirect Attack
5. A.B.D. – Attack by Drawing""",

    16: """Immovable Elbow Theory

1. The front elbow must always be one fist away from the body, never less.
2. Open and close the elbow for attack and defense.
3. The concentration of energy on the elbow creates the immovable elbow.""",

    17: """Five Gates Theory

1. Bruce Lee added the fifth gate, which is from the waist down to the feet.
2. This gate was made for kicking offense and defense.
3. This gate is divided into the front and rear leg.""",

    18: """Do Not Meet Force with Force Theory

1. To defeat strength, use speed, footwork, angulation, sensitivity, explosive force, good body mechanics, and leverage.
2. If you have to strain your muscles to beat him, then your technique is flawed.
3. Deflect but don't block: blocking means putting yourself in the way of an attack to stop it; deflecting means moving yourself away from the attack and redirecting his force to another direction.
4. Blocking only works if you are the same size as your opponent. Otherwise, you will get destroyed by someone stronger than you. Deflecting is preferable.""",

    19: """Relax – Explode Principle

1. Maintain a loose and relaxed physical and mental state, until the last moment when you strike. Then return back to this state as soon as possible.
2. Your hit is delivered suddenly with maximum explosive force, velocity, and deep penetration. When you go from a relaxed state to a sudden burst of speed and high intensity, you create explosive force.
3. Explosive force accelerates towards the target and go past it; non-explosive force (pushing force) will slow down as it nears the target, with very little penetration.""",

    20: """Always Follow-Up: Assume Nothing is Final Theory

1. Upon a successful entry, always continue your attack with aggressive ABC, Forward Pressure, and Killer Instinct. Never allow him to regain his base and balance. Never allow him to counter-attack.
2. Do not stop attacking until the enemy is sufficiently immobilized.""",

    21: """Proper Body Mechanics Theory

1. Body mechanics involve compact power, efficient structure, and leverage.
2. Proper punching mechanics involve:
   - Stage 1: Driving from Foot to Hip
   - Stage 2: Fast Rotation from Hip to Shoulder
   - Stage 3: Loose and Relaxed Whipping Energy from Shoulder to Hand
3. Effective striking principles involve:
   - Correct Type of Force
   - Correct Line of Force
   - Correct Stability and Leverage Upon Impact
4. Proper Weight Transfer
5. Balance in Motion
6. Tactical Breathing
7. Alive Footwork – Perpetual Motion""",

    22: """The Different Types of Speed

1. Movement – the speed at which your body moves during an action
2. Reaction – the speed at which you receive stimuli, then take action
3. Initiation – the speed at which you go from inaction to action in response to stimuli.
4. Perception/Visual – the speed at which you see and perceive stimuli, then take action.
5. Audible – the speed at which you hear stimuli, then take action.
6. Mental – the speed at which your mind chooses the right action in response to stimuli.
7. Alteration – the speed at which you can change directions in the middle of an action.
8. Combination – the speed at which you can deliver a series of movements in one flow.
9. Sensitivity – the speed at which you can read pressure using touch, then take action.
10. Footwork/Agility – the speed at which you can move your feet properly.
11. Trapping – the speed at which you can apply effective trapping attacks on your enemy.""",

    23: """Three Levels of Defense Theory

1. Interception: respond by intercepting his movement with an attack.
2. Evasion and Footwork: respond by evading the enemy's attack, then counter-attack him.
3. Parrying, Trapping, and Counter-Attacking: respond by parrying, trapping, and counter-attacking his attacks.""",

    24: """Immovable Elbow Moving Line Theory

1. The lead elbow must be as strong as steel – never allow it to compress inwards,
2. The lead elbow must be lined up on the centerline.
3. The lead elbow must be placed about one and a half fist length from the body.
4. All punches and deflections begin from the elbow, not the hand.""",

    25: """The Hammer Principle

1. By aiming (dropping your hand like a hammer) and lining up the lead hand at the target a split second before striking, you land a fast, accurate hit without telegraphing""",

    26: """Three Sticks Theory

1. Stick 1 (Centerline) – protect and defend at all costs – never give away your centerline
2. Stick 2 (Lead Elbow) – "Strong as Steel" – never allow your elbow to collapse into your body
3. Stick 3 (Lead Forearm) – "Soft as a Blade of Grass" – soft, yielding, flexible, sensitive, adaptable""",

    27: """Flow Theory – Fluidity in Movement

1. Flowing is a non-stop continuous motion that changes and moves without missing a beat. We never meet strength with strength, or force with force. You must flow with the situation.""",

    28: """Comfortable in All Ranges and Adaptability Theory

1. You must be comfortable in ALL ranges. Learn to adapt and overcome anything. Learn to fight and adapt to any scenario. Bruce Lee states that JKD can "fit in with any style". It means that JKD can defeat an enemy regardless of their style or system.
2. The JKD man adapts to all weapons, kicking, boxing, trapping, clinching, and ground fighting ranges. He is the master of entry and exit.""",

    29: """Longest Weapon to Nearest Target (Nearest Weapon to Nearest Target) Theory

1. Use your longest (or nearest) weapon on the opponents nearest and most vulnerable target. Thus the lead hand and lead foot is preferred to using the rear hand and foot. Or in other words, as Bruce Lee said, "I would just as soon kick someone in the head as punch him in the toe…" For example, if your enemy's face is closest to your head, then a quick headbutt to the nose might be the best choice for attack, rather than pulling away to punch.""",

    30: """Straight-Line Attack Theory

1. The shortest distance between two points is a straight line.
2. In offense and defense, we utilize the nearest weapon to the nearest target.""",

    31: """Defend When You Attack: Always Cover Your Gates Theory

1. You are most vulnerable to attack when you attack. Always defend your gates when you attack.
2. Wu Sao is 80% for defense and is responsible for defending your centerline. You can hold it:
   - In front of your chin
   - Next to your Inside Gate jaw/cheek
   - Next to your Outside Gate jaw/cheek
3. Whenever you strike, be sure to cover your head with the non-striking hand and avoid dropping your hands.""",

    32: """Bridge Hand Theory

1. The forearm is referred to as the bridge.
2. The forearm is used to intercept the opponent's forearm or attack in both offense and defense. This interception is referred to as a bridge.
3. By using a bridge, we decrease the margin of being hit, and increase our margin of control.""",

    33: """Trapping Hands Theory

1. Referred to as the tying up of hands (immobilizing the hands).
2. The idea is to use one hand to pin the opponent's two hands with one hand so that the other hand is free to strike at will.
3. This theory also correlates that two hands should not be used to control one of the opponent's hands.""",

    34: """Triangle Theory

1. The triangle serves as the basic principle in the formation and use of all Wing Chun techniques.
2. It also serves as a strong and efficient device to redirect energy. The more precise the position, the less energy required by the technique.""",

    35: """Three Sectors Theory

1. The three sectors are imaginary lines which separate the body into three sections.
2. The high section is from the solar plexus up to the top of the head.
3. The middle section is from the groin to the solar plexus.
4. The low section is from the groin to the feet.
5. Hands take care of the top two levels; legs take care of the bottom level.
6. The hands do not chase into the low level.""",

    36: """Evade a Strong Force Theory

There is a limit to how much force any particular technique can handle. No matter how strong the stance or how precise the angle of hands, there will be a force strong enough to get through. Master Wong Kiu expressed this thought by saying "You cannot block a motorcycle with a Bong Sau." It just can't be done.

Jun Fan teaches some direct confrontation techniques in term of blocking kicks or roundhouse punches; however, when the attacks are too strong, then alternative methods must be used. The advantage of direct confrontation techniques is that they are faster than going with the flow methods.

One of the best remedies against a strong force such as a spinning kick or wild hook punch is not to be there when it arrives. You always risk getting hurt when you clash with a strong force.""",

    37: """Combined Strength Theory

There is a Chinese term called "Garb Lik" which means combined strength. This term also means to not have one passive hand and one active hand. For example, don't hold someone's arm with one hand while hitting high and low with the other hand. The holding hand is passive while the hitting hand is active.

When you punch, there is also an equal strength put into the Wu Sau (guarding hand). When you apply the Bong Sau (wing block hand), you also put a strong instantaneous force into the guarding hand.

In the Chi Sao (double sticking hands), when you do a Jik Jern (center palm hit), don't have a weak high Fook Sau or else the opponent can hit by changing his Boang Sau to a Sat Sau (neck chopping hand). Always have "Garb Lik" in all of your actions.""",

    38: """Use Body Position Theory

During fighting practice, the opponent may have you jammed up so that your hand actions cannot be applied. In such cases, a shift of the body can sometimes change the angles in such a way that you again have room to maneuver.

If shifting does not help, you may still be able to move the stance in such a way as to offbalance the opponent. Even a slight change in position can sometimes give you another chance to hit.

Seemingly hopeless situations, such as where the opponent has grabbed your kicking leg, can sometimes be remedied by changing the body position. In this case, dropping to the ground in order to kick the opponent's joint with the other leg.

In Jun Fan, it is not only the hands which provide shocking forces. When you are being trapped, violent rotations of the body combined with the use of the elbow can sometimes save the day. Think of trying to hold on to a wiggling fish.""",

    39: """Be Direct Theory

There are sayings in the martial arts world such as "Use Soft Against Hard" and "Go with the Flow." These principles are useful when handling large forces. When the forces are not large, such as in the case of a roundhouse punch thrown by a similar sized opponent, it is often much quicker to clash directly with the attack so that you hit the opponent immediately.

If you are confident with your technique and can handle the opponent's force, then you can just charge in directly to the opponent's center. Provided you are able to keep the Center, you will have no problems.

Use your common sense to figure out under what circumstances the general principles of Jun Fan apply. These principles were often sayings to help people remember what to do. If you stick too dogmatically to a saying, then you could also be done in by it.""",

    40: """Restrict Movement (Trapping) Theory

The most dangerous opponent is one who is at close range with free use of both arms and legs. At high speeds it is not possible to predict or deflect all attacks. You are bound to get hit. World champion boxers are not able to avoid all hits.

When in close contact with the opponent, try to restrict the opponent's movement. This increases your chances and decreases those of the opponent. Use one arm to control two. For example, use Gum Sau (pinning hand) to control the elbow of the opponent. When at close range, use your leg to trap the opponent's leg so that he cannot kick. There is a famous saying, "Allow the opponent's useless actions, but prevent is useful actions." If you try to control the opponent totally, then he will fight much harder than usual.""",

    41: """The Meaning Behind the Jeet Kune Do Symbol

The Chinese phrases surrounding the symbol are: "Using No Way as Way" and "Having No Limitation as Limitation". Regarding the first statement, one is to approach combat without any preconceived notions, and simply respond to "what is." In this way, the martial artist is adaptable and pliable enough to fit in with any opponent and situation instantly. He is using no particular or set way that was preconditioned in him. "No-mindedness" is a term often used to describe this state of unconscious consciousness or conscious unconsciousness. And, indeed, it is an ideal state that is difficult to attain but which one aspires to. In addition, one tries to be like water when using this "no-way" approach. Water automatically assumes the container that it is poured in, thereby constantly fitting in with and adapting to the situation.

By having no limitation as the only limitation, one can transcend martial arts boundaries that are set by style, tradition, race, individual preferences, etc. Lee gave the JKD man the freedom to explore other martial arts with the only limitation being that he has only has two hands and two feet and the objective is how to use them to the maximum. Furthermore, Lee wanted us to search deep within ourselves to find what works best for each one of us. No longer are we dependent on the teachings of various styles or teachers. But by taking an honest assessment of our own strengths and weaknesses, we can improve our martial skill as well as our daily living. Like he said, "Knowledge ultimately, means self-knowledge." With this freedom to improve our skill and life in any way that we like, one is able to honestly express one's self."""
}


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
            fg='#000000',
            activebackground='#45a049',
            activeforeground='#000000',
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=10,
            command=self.next_question,
            state='disabled'
        )
        self.next_btn.pack(side='right')

        self.source_btn = tk.Button(
            control_frame,
            text="📖 View Source Material",
            font=('Arial', 12),
            bg='#2196F3',
            fg='#000000',
            activebackground='#0b7dda',
            activeforeground='#000000',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10,
            command=self.show_source_material,
            state='disabled'
        )
        self.source_btn.pack(side='right', padx=10)

        reset_btn = tk.Button(
            control_frame,
            text="Reset Score",
            font=('Arial', 12),
            bg='#f44336',
            fg='#000000',
            activebackground='#da190b',
            activeforeground='#000000',
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
        self.source_btn.config(state='normal')

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
                btn.config(bg='#4CAF50', fg='#ffffff', state='disabled')
            elif answer_text == selected_answer and not is_correct:
                btn.config(bg='#f44336', fg='#ffffff', state='disabled')
            else:
                btn.config(state='disabled', bg='#888888', fg='#ffffff')

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

    def show_source_material(self):
        """Show the full source text for the current concept"""
        if not self.current_card:
            return

        concept_num = int(self.current_card['concept_number'])
        concept_name = self.current_card['concept_name']

        # Get the source text
        source_text = CONCEPT_TEXTS.get(concept_num, "Source material not found.")

        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title(f"Source Material - Concept #{concept_num}")
        popup.geometry("700x600")
        popup.configure(bg='#2d2d2d')

        # Title
        title_label = tk.Label(
            popup,
            text=f"Concept #{concept_num}: {concept_name}",
            font=('Arial', 16, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            pady=15
        )
        title_label.pack()

        # Scrollable text area
        text_frame = tk.Frame(popup, bg='#2d2d2d')
        text_frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))

        text_area = scrolledtext.ScrolledText(
            text_frame,
            font=('Arial', 12),
            bg='#ffffff',
            fg='#000000',
            wrap=tk.WORD,
            padx=15,
            pady=15
        )
        text_area.pack(fill='both', expand=True)
        text_area.insert('1.0', source_text)
        text_area.config(state='disabled')  # Make read-only

        # Close button
        close_btn = tk.Button(
            popup,
            text="Close",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='#000000',
            activebackground='#45a049',
            activeforeground='#000000',
            relief='flat',
            cursor='hand2',
            padx=40,
            pady=10,
            command=popup.destroy
        )
        close_btn.pack(pady=15)


def main():
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
