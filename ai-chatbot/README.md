# 🤖 StudyPYBot – AI Chat Assistant

StudyPYBot is an AI-powered chatbot developed using Python that can interact with users through natural language. It is designed to assist students and general users by answering questions, providing explanations, and simulating human-like conversations. The system integrates basic artificial intelligence concepts such as Natural Language Processing (NLP) and context-aware responses.

## 📌 Features

- 💬 Real-time text-based conversation
- 🧠 AI-generated responses using NLP
- 🗂️ Conversation history tracking
- 🖥️ User-friendly graphical interface (GUI)
- 🔄 Context-aware interaction (basic memory)
- ⚙️ Modular and scalable architecture

## 🏗️ Project Structure
    
    StudyPYBot/
        │── main.py
        │── config.py
        │── requirements.txt
        │
        ├── docs/               # Mainly documentations
        ├── app/                # Core application logic
        ├── ai/                 # AI and NLP processing
        ├── memory/             # Chat history and storage
        ├── gui/                # User interface (Tkinter)
        ├── utils/              # Helper functions
        ├── data/               # JSON files and configurations
        └── tests/              # Unit testing

## ⚙️ Installation

    Clone the repository:
    - git clone https://github.com/your-username/StudyPYBot.git
    cd StudyPYBot
    
    Install dependencies:
    - pip install -r requirements.txt

## ▶️ Usage

    Run the application:

    - python main.py

    Then start chatting with the bot through the interface.

## 📦 Python Packages / Dependencies

The following Python libraries and packages were used in developing StudyPYBot:

### Core Packages
```bash
pip install torch
pip install transformers
pip install accelerate
pip install sentencepiece
```

### GUI & Interface
```bash
pip install customtkinter
pip install pillow
```

### Utility Packages
```bash
pip install numpy
pip install requests
```

### Built-in Python Modules
These modules are included with Python and do not require installation:

- tkinter
- json
- threading
- os
- time

---

## 📋 Example `requirements.txt`

```txt
torch
transformers
accelerate
sentencepiece
customtkinter
pillow
numpy
requests
```

---

## ⚙️ Installation

Clone the repository and install the dependencies:

```bash
git clone <your-repository-link>
cd StudyPYBot
pip install -r requirements.txt
```

---

## 🤖 Model Used

StudyPYBot uses:

- TinyLlama-1.1B (Locally Hosted Transformer Model)

Built using the Hugging Face `transformers` library together with `PyTorch`.

## 🧠 Technologies Used

- Python – Main programming language
- Tkinter – GUI development
- Transformers / OpenAI API – AI and NLP processing
- JSON – Data storage
- Torch – Machine learning support

## 🎯 Objectives

1. To develop an AI chatbot capable of understanding user input
2. To simulate human-like conversation using NLP
3. To provide assistance in learning and general queries
4. To demonstrate basic AI application in software development

## ⚠️ Limitations

- Limited understanding of complex or ambiguous queries
- Requires internet connection (if using API-based AI)
- No voice input/output in current version
- Not intended for professional or medical advice

## 🚀 Future Improvements

- 🎤 Voice input and speech output
- 🌐 Multi-language support
- 🧠 Improved memory and learning capability
- 📱 Web or mobile version
- 🔐 User authentication system

## 👨‍💻 Developer

    PyTech-Group | BSIT Students | Aspiring Software Developers & Network Engineers

## 📄 License

    This project is for educational purposes only.

## 💡 Note

StudyPYBot is a beginner-to-intermediate AI project designed to demonstrate the integration of artificial intelligence into a functional application. It can be further enhanced into a more advanced system with additional AI features and improvements.
