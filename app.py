import os
import json
from datetime import datetime, timedelta
import time
import random
import speech_recognition as sr
import pyttsx3
from ollama import Client

class VoiceInterviewBot:
    def __init__(self):
        try:
            # Initialize Ollama clientN
            self.client = Client()
            self.model_name = 'mistral'
            
            # Initialize conversation history
            self.conversation_history = []
            
            # Initialize voice components
            self.recognizer = sr.Recognizer()
            self.engine = pyttsx3.init()
            
            # Configure voice settings
            voices = self.engine.getProperty('voices')
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
            self.engine.setProperty('rate', 150)
            
            # Add pause threshold
            self.pause_threshold = 3
            
            # Exit commands
            self.exit_commands = {'stop', 'exit', 'quit', 'end interview', 'terminate'}
            
            self.position = None
            self.candidate_name = None
            self.interview_stage = "introduction"
            self.interview_duration = timedelta(minutes=45)
            self.start_time = None
            
            # Initialize the persona
            self.setup_interviewer_persona()
            
        except Exception as e:
            print(f"Initialization error: {e}")
            raise

    def check_for_exit(self, text):
        """Check if the response contains any exit commands"""
        if text:
            text_lower = text.lower()
            for command in self.exit_commands:
                if command in text_lower:
                    return True
        return False

    def handle_exit(self, interview_record):
        """Handle early exit from interview"""
        exit_message = f"""
        I understand you'd like to end the interview. Thank you for your time today, {self.candidate_name}. 
        I hope you had a good experience. Have a great rest of your day!
        """
        self.speak(exit_message)
        self.save_interview_record(interview_record)
        return True

    def speak(self, text):
        """Convert text to speech"""
        try:
            text = text.strip()
            print(f"\nInterviewer: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")
            print(f"Falling back to text output: {text}")

    def listen(self):
        """Convert speech to text with pause detection"""
        try:
            with sr.Microphone() as source:
                print("\nListening... (Say 'stop' or 'exit' to end the interview)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                try:
                    audio = self.recognizer.listen(source, timeout=self.pause_threshold)
                    text = self.recognizer.recognize_google(audio)
                    print(f"{self.candidate_name if self.candidate_name else 'Candidate'}: {text}")
                    return text
                    
                except sr.WaitTimeoutError:
                    print("\nPause detected - moving to next question")
                    return None
                    
                except sr.UnknownValueError:
                    self.speak("I didn't catch that. Could you please repeat?")
                    return self.listen()
                    
                except sr.RequestError:
                    print("Speech recognition service error. Falling back to text input.")
                    return input(f"{self.candidate_name if self.candidate_name else 'Candidate'} (type 'stop' to end): ")
        except Exception as e:
            print(f"Microphone error: {e}")
            print("Falling back to text input mode.")
            return input(f"{self.candidate_name if self.candidate_name else 'Candidate'} (type 'stop' to end): ")

    def send_message(self, prompt):
        """Send message to Ollama and get response"""
        try:
            # Add conversation history to maintain context
            full_prompt = "\n".join(self.conversation_history + [prompt])
            
            response = self.client.chat(model=self.model_name, messages=[{
                'role': 'user',
                'content': full_prompt
            }])
            
            # Store the interaction in history
            self.conversation_history.append(f"User: {prompt}")
            self.conversation_history.append(f"Assistant: {response['message']['content']}")
            
            # Keep history manageable
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return response['message']['content']
            
        except Exception as e:
            print(f"Error communicating with Ollama: {e}")
            print("Make sure Ollama is installed and running")
            return "I apologize, but I'm having trouble processing that. Let's continue with the next question."

    def setup_interviewer_persona(self):
        """Initialize the interviewer's persona"""
        persona = """
        You are Priya Chen, a senior technical interviewer with 12 years of experience. Your personality traits:
        - Warm and professional demeanor
        - Excellent active listening skills
        - Ability to make candidates feel comfortable while maintaining professionalism
        - Skilled at asking insightful follow-up questions
        
        Interview guidelines:
        1. Start with light conversation to put the candidate at ease
        2. Listen carefully and reference previous answers in follow-up questions
        3. Show appropriate reactions to answers
        4. Use natural transitions between questions
        5. Never make assumptions about candidate's experience not mentioned in conversation
        6. Maintain a conversational yet professional tone
        
        Keep responses concise and conversational. Respond directly without any prefixes or role-playing indicators.
        """
        try:
            self.send_message(persona)
        except Exception as e:
            print(f"Error setting up persona: {e}")
            print("Continuing with basic functionality...")

    def natural_delay(self):
        """Add natural pause between interactions"""
        time.sleep(random.uniform(1, 2))

    def check_time_remaining(self):
        """Check if interview time limit is approaching"""
        elapsed_time = datetime.now() - self.start_time
        remaining_time = self.interview_duration - elapsed_time
        
        if remaining_time <= timedelta(minutes=5) and remaining_time > timedelta(minutes=4):
            self.speak("We have about 5 minutes remaining. Let's make sure we cover any final important points.")
        
        return remaining_time > timedelta(minutes=0)

    def generate_question(self, context):
        """Generate the next interview question"""
        if not context:
            question_prompt = f"""
            Generate an initial open-ended question for {self.candidate_name} who is interviewing for a {self.position} position.
            The question should:
            1. Be general and not make assumptions about their background
            2. Help understand their interest in {self.position}
            3. Let them share their relevant experience if they have any
            
            Keep it conversational and avoid assuming any specific experience.
            """
        else:
            question_prompt = f"""
            Based on the position of {self.position} and this context: {context}
            Generate ONE natural follow-up question that:
            1. Builds naturally from their previous response
            2. Helps understand their knowledge and experience level
            3. Stays relevant to the {self.position} role
            
            Keep it focused and conversational.
            """
        
        return self.send_message(question_prompt)

    def analyze_response(self, question, response, context):
        """Analyze candidate's response and generate interviewer's response"""
        analysis_prompt = f"""
        Analyze this response from {self.candidate_name}:
        Question: {question}
        Response: {response}
        Previous context: {context}
        
        Generate a natural interviewer response that:
        1. Acknowledges their answer appropriately
        2. Includes a relevant follow-up question OR a natural transition
        3. Maintains the conversational flow
        4. Only references information they've explicitly shared
        
        Keep the response concise and natural.
        """
        
        return self.send_message(analysis_prompt)

    def start_interview(self):
        """Start the interview process"""
        print("\n=== Voice-Enabled Technical Interview (45 minutes) ===")
        print("Note: You can say 'stop' or 'exit' at any time to end the interview\n")
        
        self.start_time = datetime.now()
        self.speak("Hello! I'm Priya Chen. Before we begin, could you please tell me your name?")
        self.candidate_name = self.listen()
        
        if self.check_for_exit(self.candidate_name):
            return False
            
        if self.candidate_name is None:
            self.speak("I noticed a pause. Could you please tell me your name?")
            self.candidate_name = self.listen()
            if self.check_for_exit(self.candidate_name):
                return False
        
        self.speak("Which position are you interviewing for today?")
        self.position = self.listen()
        
        if self.check_for_exit(self.position):
            return False
            
        if self.position is None:
            self.speak("I noticed a pause. Which position are you applying for?")
            self.position = self.listen()
            if self.check_for_exit(self.position):
                return False
        
        welcome_prompt = f"""
        Give a warm, natural welcome to {self.candidate_name} who is interviewing for {self.position}.
        Include:
        1. A warm greeting
        2. Make them feel comfortable
        3. Explain that this will be a 45-minute interview
        4. Explain that we'll start by learning about their interest in {self.position}
        5. Encourage them to ask questions
        
        Keep it concise and conversational.
        """
        
        welcome = self.send_message(welcome_prompt)
        self.natural_delay()
        self.speak(welcome)
        return True

    def conduct_interview(self):
        """Main interview loop"""
        if not self.start_interview():
            print("\nInterview ended during introduction.")
            return
            
        interview_record = {
            "candidate_name": self.candidate_name,
            "position": self.position,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "conversation": []
        }
        
        context = ""
        try:
            while self.check_time_remaining():
                self.natural_delay()
                question = self.generate_question(context)
                self.speak(question)
                
                response = self.listen()
                
                # Check for exit command
                if self.check_for_exit(response):
                    if self.handle_exit(interview_record):
                        return
                
                if response is None:
                    interview_record["conversation"].append({
                        "question": question,
                        "response": "[Candidate paused]",
                        "interviewer_feedback": "Moving to next question due to pause"
                    })
                    continue
                
                interviewer_response = self.analyze_response(question, response, context)
                
                context += f"\nQ: {question}\nA: {response}\n"
                interview_record["conversation"].append({
                    "question": question,
                    "response": response,
                    "interviewer_feedback": interviewer_response
                })
                
                self.natural_delay()
                self.speak(interviewer_response)
            
            self.wrap_up_interview(interview_record)
                
        except KeyboardInterrupt:
            self.handle_early_termination(interview_record)

    def wrap_up_interview(self, interview_record):
        """Conclude the interview"""
        wrap_up_prompt = f"""
        Generate a natural interview conclusion for {self.candidate_name}.
        Include:
        1. Thank them for their time
        2. Explain next steps
        3. Offer opportunity for quick final questions
        
        Keep it warm and professional.
        """
        
        conclusion = self.send_message(wrap_up_prompt)
        self.natural_delay()
        self.speak(conclusion)
        
        if self.check_time_remaining():
            final_response = self.listen()
            if final_response and final_response.strip():
                final_feedback = self.send_message(f"Give a brief, natural response to: {final_response}")
                self.natural_delay()
                self.speak(final_feedback)
        
        self.save_interview_record(interview_record)

    def handle_early_termination(self, interview_record):
        """Handle early termination of interview"""
        print("\n\nI understand we need to conclude early.")
        self.wrap_up_interview(interview_record)

    def save_interview_record(self, interview_record):
        """Save the interview record to a JSON file"""
        filename = f"interview_{self.candidate_name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(interview_record, f, indent=4)
        print(f"\nInterview record saved to {filename}")

def main():
    try:
        interviewer = VoiceInterviewBot()
        interviewer.conduct_interview()
    except Exception as e:
        print(f"Critical error: {e}")
        print("\nPlease ensure:")
        print("1. Ollama is installed and running (https://ollama.ai/download)")
        print("2. The 'mistral' model is pulled (run 'ollama pull mistral')")
        print("3. All required Python packages are installed:")
        print("   pip install ollama SpeechRecognition pyttsx3 pyaudio")

if __name__ == "__main__":
    main()