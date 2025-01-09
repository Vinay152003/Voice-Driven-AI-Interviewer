# Voice-Driven-AI-Interviewer
The Voice-Driven AI Interviewer solves inefficiencies in hiring by automating interviews, ensuring consistency, reducing bias, and enhancing scalability, accessibility, and candidate engagement while saving time and resources for HR teams

🚀 Vision

The Voice-Driven AI Interviewer aims to transform the recruitment process by providing a scalable, unbiased, and professional interview experience. It solves challenges such as interviewer fatigue, inconsistent candidate experiences, high-volume interview handling, and documentation inefficiencies. The project uses AI-driven conversations to mimic the warmth of human interviews, allowing for seamless and inclusive interactions.

🔧 Features

Voice-Enabled Interviews: Uses speech recognition and AI to carry out dynamic, real-time interviews.
AI-Powered Question Generation: Automatically generates open-ended and follow-up questions based on the candidate's responses.
Natural Language Processing (NLP): Understands and generates natural, context-aware responses.
Automated Documentation: Saves interview records in a structured format, including conversations and feedback.
Scalable: Efficiently handles high-volume recruitment by automating the process.
Inclusive Design: Adaptive to different candidate needs, ensuring accessibility and fairness.
Time Management: Tracks interview duration and provides timely reminders for wrapping up.

⚙️ Technologies Used

Python: Core programming language
Ollama: AI model for conversational interactions
SpeechRecognition: Speech-to-text conversion
pyttsx3: Text-to-speech engine
JSON: For storing interview records
Datetime: For managing and tracking interview time

🛠️ Installation

Follow these steps to set up the project locally:

Clone this repository:

git clone [https://github.com/yourusername/voice-driven-ai-interviewer](https://github.com/Vinay152003/Voice-Driven-AI-Interviewer)
cd voice-driven-ai-interviewer

Install dependencies:

pip install -r requirements.txt
Download the required AI model (Mistral): Ensure Ollama is installed and running, then pull the necessary model:

ollama pull mistral

Run the application:

python app.py

💬 How It Works

Initial Setup: The AI interviewer introduces itself and asks the candidate for their name and the position they are applying for.

Question Generation: Based on the candidate’s responses, the AI dynamically generates relevant follow-up questions.

Voice Interaction: The system listens to the candidate's responses, processes them, and generates a natural response.

Documenting the Interview: All conversations, questions, and feedback are saved in a structured JSON file for future reference.

Wrap-up: As the interview nears its conclusion, the AI provides a warm wrap-up message, offers next steps, and allows time for final questions.

💡 Benefits

Efficiency: Save time for HR teams by automating the interview process.

Consistency: Ensure every candidate has the same experience and is evaluated objectively.

Scalability: Perfect for handling large-scale recruitment without increasing HR workload.

Candidate Engagement: Provide candidates with a modern, engaging, and inclusive interview experience.

Data-Driven Insights: Automatically save and analyze interview data for better decision-making.

📂 File Structure

app.py: Main script that runs the interview process

requirements.txt: List of Python dependencies

interviews/: Directory to store saved interview records

README.md: This file

interview_bot/: Contains the core logic of the interview bot, including speech recognition, AI interactions, and more

📌 Contributing

We welcome contributions! If you have any ideas for improving the Voice-Driven AI Interviewer, feel free to open an issue or submit a pull request.

Fork the repository

Create a new branch (git checkout -b feature-branch)
Commit your changes (git commit -am 'Add feature')
Push to the branch (git push origin feature-branch)
Open a pull request

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🤖 Acknowledgments

Ollama: For providing the conversational AI model.
SpeechRecognition: For enabling voice-to-text functionality.
pyttsx3: For converting text to speech.
OpenAI: For the inspiration behind natural language processing in interview automation.
