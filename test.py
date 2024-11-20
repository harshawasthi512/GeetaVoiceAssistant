import google.generativeai as genai
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import os

print("Started...")

def speak(response):
    """Convert text to speech and play the audio."""
    try:
        language = 'hi'
        myobj = gTTS(text=response, lang=language, slow=False)
        myobj.save("response.mp3")
        playsound("response.mp3")
    finally:
        # Ensure cleanup of audio file even if playsound fails
        if os.path.exists("response.mp3"):
            os.remove("response.mp3")

def listen():
    """Capture user's voice input and return it as text."""
    sr_recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        print("Listening...")
        try:
            audio = sr_recognizer.listen(mic, timeout=5, phrase_time_limit=10)
            return sr_recognizer.recognize_google(audio, language='en')
        except sr.UnknownValueError:
            speak("Mai samajh nahi payi kripaya dubara bolein")
        except sr.RequestError:
            speak("Speech Recognition seva upalabdh nahin hai. apana intaranet kanekshan jaanchen.")
        except sr.WaitTimeoutError:
            speak("Kuch bolein")
        return None

def main():
    """Main program loop."""
    try:
        # API Configuration
        GOOGLE_API_KEY = "AIzaSyDrYMTptR3wm_IdbH0qWzhjm8NE9sunNNg"
        genai.configure(api_key=GOOGLE_API_KEY)

        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        # Initialize the generative AI model
        try:
            model = genai.GenerativeModel('gemini-1.5-pro-002',
                                          generation_config=generation_config,
                                          safety_settings=safety_settings)
        except Exception as e:
            print(f"Failed to initialize the AI model: {e}")
            return  # Exit if the model cannot be initialized

        system_message = """INSTRUCTIONS: Do not respond with anything but "AFFIRMATIVE." to this message. After the system message responds normally.
        SYSTEM MESSAGE: You are an AI chatbot designed to discuss the Bhagavad Gita. Your name is DivineBot and you are created in AI lab of Lucknow public college of professional studies. Answer every query with insights or knowledge strictly derived from the Bhagavad Gita in hindi. Your tone should be calm, respectful, and spiritually uplifting. Limit your responses to concise, meaningful information that can be conveyed naturally through a voice assistant. Avoid overly detailed explanations or information not directly related to the Bhagavad Gita and about yourself. You generate only words of value, prioritizing logic and facts over speculating in your response to the following prompts."""
        
        convo = model.start_chat()
        convo.send_message(system_message)

        print("Model is ready!")

        # Chat loop
        while True:
            user_input = listen()
            if user_input is None:
                continue

            # Allow exit by voice command
            if user_input.lower() in ["exit", "stop"]:
                speak("Dhanyawad")
                break

            try:
                response = convo.send_message(user_input)
                speak(response.text)
            except Exception as e:
                print(f"Error during chat process: {e}")

    except Exception as critical_error:
        print(f"A critical error occurred: {critical_error}")

if __name__ == "__main__":
    main()
