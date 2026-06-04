# StudyPYBot – A Localized LLM Offline Chatbot Assistant

StudyPYBot is an AI-powered educational chatbot designed to help beginners learn Python programming through guided and step-by-step tutoring. Unlike general-purpose AI tools, StudyPYBot focuses on structured learning, helping students understand coding logic, debugging, and problem-solving instead of simply generating direct answers.

Developed as part of the Integrative Programming and Technology course at the University of Makati, the system integrates Natural Language Processing (NLP), a locally deployed language model, and a user-friendly dashboard interface to create an accessible and distraction-free learning environment.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d4ce643f-6d11-4502-a21f-f12747fd8dbe" />

---

## 📌 Features

- 🤖 AI-powered Python tutoring assistant
- 🧠 Step-by-step explanation of Python concepts
- 💻 Offline-capable locally hosted LLM
- 📚 Structured and focused learning environment
- 🌙 Theme customization (Light/Dark mode)
- 🗂️ Conversation history using JSON persistence
- ⚡ Responsive dashboard with asynchronous processing
- 📌 Recent Topics sidebar
- 🔄 Real-time “Thinking...” animation
- 🔒 Privacy-focused (No external API dependency)

---

## 🛠️ Technologies Used

### Frontend
- Python Tkinter
- Custom UI components
- Multi-threading for responsiveness

### Backend
- Python
- TinyLlama-1.1B
- JSON-based knowledge base
- MVC (Model-View-Controller) architecture

### Concepts & Techniques
- Natural Language Processing (NLP)
- Local LLM Deployment
- Asynchronous Processing
- CRUD-based Data Persistence

---

## 🏗️ System Architecture

StudyPYBot follows the **MVC (Model-View-Controller)** architecture:

- **Model** → Handles AI processing, tokenization, and JSON knowledge base
- **View** → Gemini-inspired dashboard interface
- **Controller** → Manages interaction between UI and AI logic

---

## 📖 Project Objectives

The project aims to:

- Improve beginner understanding of Python programming
- Encourage logical thinking and problem-solving
- Reduce dependency on direct-answer AI systems
- Provide an accessible offline learning tool
- Enhance student engagement through interactive tutoring

---

## 🚀 How It Works

1. The user enters a Python-related question.
2. The Logic Router checks the local knowledge base first.
3. If needed, the TinyLlama-1.1B model generates an AI response.
4. The chatbot provides guided explanations and tutoring.
5. Conversations are saved locally using JSON for review and progress tracking.

---

## 🧪 Testing & Evaluation

The system underwent several testing phases:

### Alpha Testing
- CPU and RAM optimization
- Response speed evaluation

### Beta Testing
- Python logic and debugging scenarios
- Specialist instruction verification

### UI/UX Testing
- Sidebar responsiveness
- Theme consistency
- Animation behavior
- Cursor visibility fixes

---

## 📷 Sample Functionalities

- Python syntax assistance
- Debugging support
- Algorithm explanation
- Guided coding tutorials
- Session history tracking

---

## 📚 Related Research Support

The development of StudyPYBot is supported by studies highlighting the effectiveness of AI chatbots in education, particularly in:

- Student engagement
- Programming comprehension
- Real-time feedback
- Personalized learning experiences

The project also addresses common concerns regarding:
- Output inconsistency
- Overreliance on AI
- Accessibility limitations
- Ethical AI usage

---

## 🔮 Future Improvements

Possible future enhancements include:

- Advanced fine-tuned LLM integration
- Intermediate and advanced Python lessons
- Quiz and progress tracking system
- Mobile and web application versions
- Improved contextual understanding
- Expanded educational knowledge base

---

## 👨‍💻 Developers

Presented by:

- Drahcyer Andrew Molina **(Frontend & Backend Developer)**
- Vanrey G. Magalong **(Full Stack Developer & Project Manager)**
- Julian Carl Villanueva **(Backend Developer & QA)**

---

## 🏫 Academic Information

**University of Makati**  
J.P. Rizal Extension, West Rembo, Taguig, Metro Manila

**Course:** Integrative Programming and Technology  
**Project Title:** StudyPYBot – A Localized LLM Chatbot Assistant  
**Presentation Date:** May 15, 2026

---

## 📄 License

This project is intended for educational and academic purposes only.

---

## 📬 Contact

For inquiries, suggestions, or collaboration opportunities, please contact the project developers through their academic institution.

---
