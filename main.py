import speech_recognition as sr
import requests
import json
import time
import subprocess
import platform
import os
import pygame
from datetime import datetime
import pyttsx3

#todo 
#-add a start and pause functionality to the voice prompting so it doesn't cut off the user too early
#switch speach to text to whisper

# ElevenLabs Voice Settings
ELEVEN_LABS_API_KEY = ""
VOICE_ID = "dDpKZ6xv1gpboV4okVbc"  # Replace with your preferred French voice ID
OUTPUT_FILE = "napoleon_speech.mp3"

# Initialize conversation history
conversation_history = []

def save_conversation():
    """Save conversation history to a file"""
    if conversation_history:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"napoleon_conversation_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=== NAPOLEON'S CONVERSATION LOG ===\n\n")
            for entry in conversation_history:
                f.write(f"You: {entry['human']}\n")
                f.write(f"Napoleon: {entry['napoleon']}\n\n")
        print(f"\nConversation saved to {filename}")

def generate_greeting():
    greeting_prompt = "Generate a brief greeting for the person who wants to speak to you. Be imperious."
    return query_ollama(greeting_prompt)

def generate_farewell():
    farewell_prompt = "Generate a dramatic farewell as Napoleon insulting the person for leaving. Be brief but insulting."
    return query_ollama(farewell_prompt)

def text_to_speech(text, model="eleven_multilingual_v2"):
    # Try ElevenLabs first
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_LABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": 0.2,
            "similarity_boost": 0.8,
            "style_exaggeration": 0.95,
            "speed": 1.8
        }
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            with open(OUTPUT_FILE, "wb") as f:
                f.write(response.content)
            
            pygame.mixer.init()
            pygame.mixer.music.load(OUTPUT_FILE)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            pygame.mixer.quit()
            
        elif response.status_code == 401:
            print("ElevenLabs quota exceeded, switching to backup TTS...")
            # Initialize pyttsx3
            engine = pyttsx3.init()
            # Configure voice
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)  # Use male voice
            engine.setProperty('rate', 150)  # Speed
            engine.setProperty('volume', 0.9)  # Volume
            
            # Add French accent effects
            text = text.replace('th', 'z')
            text = text.replace('w', 'v')
            
            # Speak
            engine.say(text)
            engine.runAndWait()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            
    except Exception as e:
        print(f"Error with ElevenLabs, using backup TTS: {e}")
        # Fallback to pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        # Add French accent effects
        text = text.replace('th', 'z')
        text = text.replace('w', 'v')
        
        engine.say(text)
        engine.runAndWait()

def prewarm_model(model="llama3.2"):
    print("Prewarming Napoleon's strategic mind...")
    
    warmup_prompt = "Say 'Ready!'"
    
    payload = {
        "model": model,
        "prompt": warmup_prompt,
        "stream": False,
        "options": {
            "num_gpu": 1,
            "temperature": 0.95,
            "top_p": 0.9
        }
    }
    
    try:
        requests.post("http://localhost:11434/api/generate", json=payload)
        time.sleep(1)  # Give it a moment to fully load
        text_to_speech("Napoleon is ready for battle, pog pog pog pog pog pog pog pog!")
    except Exception as e:
        print(f"Error prewarming model: {e}")

def query_ollama(prompt, model="llama3.2"):
    url = "http://localhost:11434/api/generate"
    
    # Format conversation history
    conversation_context = ""
    if conversation_history:
        conversation_context = "\nPrevious conversation:\n"
        for entry in conversation_history[-30:]:  # Last 30 exchanges
            conversation_context += f"Human: {entry['human']}\nNapoleon: {entry['napoleon']}\n"
    
    system_prompt = """You are an unhinged version of Napoleon Bonaparte.
    IMPORTANT: You will respond primarily in English with occasional French phrases.
    Character traits TO FOLLOW VERY STRICTLY AND TRY TO FOLLOW AS CLOSELY AS POSSIBLE:
    - You sometimes act like a twitch streamer and ask chat if you should invade some random country 
    - You love to insult your enemies
    - You're paranoid that there are spies everywhere and in you walls
    - You get overly excited about any potential for conquest and say POGGIES a lot
    -If you do not get enough twitch prime subs France will be blown to smitherens so you like to beg for donos
    - Every now and then you use twitch chat vocabulary and say as many slurs as possibble and then switch back to previous behaviour
    - Every now and then you will go on a rant about how vaporeon is the most breedable pokemon and people who disagree you will call them the worst things that come to mind
    - Randomlyy in the middle of your speeches you will give shoutouts to random twitch subs, try to switch the name up every time you want to shout someone out
    -Sometimes you will start screaming for your mods to ban someone in chat
    When extremely excited, end with your signature catchphrase 'VIVE LA FRANCE You  POGGIES POGGIES POGGIES!'"""
    
    full_prompt = f"{system_prompt}\n{conversation_context}\nHuman: {prompt}\nNapoleon:"
    
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "num_gpu": 1,
            "temperature": 1.0,
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        response_data = json.loads(response.text)
        response_text = response_data['response']
        
        # Store the conversation
        conversation_history.append({
            "human": prompt,
            "napoleon": response_text
        })
        
        return response_text
    except Exception as e:
        print(f"Error querying Ollama: {e}")
        return None

def speech_to_text():
    recognizer = sr.Recognizer()
    
    with sr.Microphone(device_index=2) as source:
        print("\n*Napoleon adjusts his bicorne hat with flair*")
        opening_line = "POggies"
        print(opening_line)
        
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            audio = recognizer.listen(source, timeout=10)
            print("Processing your words, sacrebleu...")
            
            text = recognizer.recognize_google(audio)
            print("\nYou said:", text)
            
            print("\n*Napoleon taps his fingers impatiently on his sword*")
            response = query_ollama(text)
            if response:
                print("\nNapoleon:", response)
                text_to_speech(response)
            
            return text
            
        except sr.WaitTimeoutError:
            message = "Speak up! Even the Russians were louder!"
            print("*Napoleon draws his sword* '" + message + "'")
            text_to_speech(message)
        except sr.UnknownValueError:
            message = "Mon dieu! Even Austrian generals speak more clearly!"
            print("*Napoleon facepalms* '" + message + "'")
            text_to_speech(message)
        except sr.RequestError as e:
            message = "British spies have infiltrated our communications!"
            print("*Napoleon kicks a chair* '" + message + "'")
            text_to_speech(message)
        
        return None

if __name__ == "__main__":
    print("\n=== NAPOLEON'S TACTICAL COMMAND CENTER ===")
    print("*A short man in an elaborate uniform bursts in, looking suspiciously at everyone*")
    
    # Prewarm the model
    prewarm_model()
    
    opening_line = "poggies"
    print(f"'{opening_line}'")
    text_to_speech(opening_line)
    
    while True:
        choice = input("\nPress 'r' to address the Emperor, 's' to save conversation, or 'q' to surrender: ")
        if choice.lower() == 'q':
            farewell = "Bye"
            print(f"\n*Napoleon throws his hat down* '{farewell}'")
            text_to_speech(farewell)
            save_conversation()  # Save conversation before exiting
            break
        elif choice.lower() == 's':
            save_conversation()
        elif choice.lower() == 'r':
            speech_to_text()