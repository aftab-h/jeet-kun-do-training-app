# Jeet Kune Do Training Flashcard App

A flashcard application for studying Jeet Kune Do concepts (Levels 1-2) with multiple-choice questions and spaced repetition features.

## Features

- 📚 **200+ Questions** covering all 41 JKD concepts
- 🎯 **Multiple Choice Format** with 4 answer options
- 📊 **Score Tracking** with percentage calculation
- 📖 **View Source Material** - verify answers against original PDF text
- 🎨 **Dark Theme UI** for comfortable studying
- 💻 **Desktop & Web Versions**

## Desktop App (Python/Tkinter)

### Requirements
- Python 3.x
- tkinter (usually comes with Python)

### Run Desktop App
```bash
# Double-click the launcher
./run_app.command

# Or run directly with Python
python3 flashcard_app.py
```

## Web App

### Run Web App
Simply open `web/index.html` in your browser, or serve it locally:

```bash
cd web
python3 -m http.server 8000
# Then visit http://localhost:8000
```

### Deploy Web App
The web version can be deployed to:
- GitHub Pages
- Netlify
- Vercel
- Any static hosting service

## Project Structure

```
jeet-kun-do-training-app/
├── data/
│   ├── jkd_flashcards.csv           # Flashcard questions database
│   └── jeet-kun-do-concepts-level-1-and-2.pdf  # Source material
├── web/
│   ├── index.html                   # Web app HTML
│   ├── styles.css                   # Web app styles
│   ├── app.js                       # Web app logic
│   ├── conceptTexts.js              # Source material for web
│   └── flashcards.json              # Questions in JSON format
├── flashcard_app.py                 # Desktop app (Python)
├── run_app.command                  # macOS launcher
└── README.md
```

## JKD Concepts Covered

The app covers all 41 concepts from Phase 1-2:

1. Centerline Theory
2. Economy of Motion Theory
3. Four Ranges of Combat
4. Fighting Measure Theory
5. Power Side Forward Theory
6. Forward Pressure Theory
7. Non-Telegraphic Motion Theory
8. Simultaneous Attack & Defense (Lin Sil Dai Da)
9. Visual Focus Principles
10. Time-Distance Variable
... and 31 more concepts

## Keyboard Shortcuts (Web App)

- `1-4` - Select answer A-D
- `Enter` - Next question
- `S` - View source material
- `Esc` - Close modal

## Usage Tips

1. **Study Mode**: Read the question carefully before selecting an answer
2. **Verify**: Use "View Source Material" to check the exact wording from the PDF
3. **Track Progress**: Monitor your score percentage to identify weak areas
4. **Reset**: Clear score anytime to start fresh

## Data Accuracy

All questions and answers are extracted directly from the official JKD Concepts PDF (Predator Edition). No information has been fabricated - all content is verifiable against the source material.

## Credits

- **Source Material**: Tandez Academy of Martial Arts
- **Copyright**: Adrian Tandez Enterprises 2024
- **App Development**: Created for personal JKD study

## License

This project is for personal educational use. The JKD concepts and source material are copyrighted by Adrian Tandez Enterprises 2024.
