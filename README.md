# Napoleon Twitch Chatbot

A unique and entertaining AI chatbot that combines Napoleon Bonaparte's persona with modern Twitch streamer behavior. This bot uses speech recognition, text-to-speech, and large language models to create an interactive experience with an unhinged version of Napoleon who alternates between historical conquests and Twitch donations.

## Features

- 🎙️ Voice interaction through speech recognition
- 🗣️ Dynamic text-to-speech using ElevenLabs API (with fallback to pyttsx3)
- 🤖 AI-powered responses using the Ollama API
- 💾 Conversation history saving
- 🎭 Unique personality mixing historical Napoleon with Twitch streamer behavior
- 🔄 Automatic model prewarming for faster responses

## Prerequisites

- Python 3.x
- Ollama running locally with llama3.2 model
- ElevenLabs API key (optional, will fallback to pyttsx3)
- Working microphone and speakers

## Required Python Packages

```bash
pip install speech_recognition
pip install requests
pip install pygame
pip install pyttsx3
```

## Configuration

1. Set up your ElevenLabs API key (optional):
   - Replace the empty `ELEVEN_LABS_API_KEY` variable with your key
   - Optionally modify the `VOICE_ID` for a different voice

2. Configure your microphone:
   - The script uses device_index=2 by default
   - Modify the index in `speech_to_text()` function if needed

## Usage

1. Run the script:
```bash
python napoleon_chatbot.py
```

2. Available commands:
   - Press 'r' to speak to Napoleon
   - Press 's' to save the conversation history
   - Press 'q' to exit (Napoleon will be disappointed)

## Character Traits

Napoleon's AI personality includes:
- Twitch streamer behavior with frequent "POGGIES" exclamations
- Paranoid tendencies about spies
- Excessive excitement about potential conquests
- Begging for Twitch Prime subscriptions
- Random Twitch chat vocabulary usage
- Occasional rants about Vaporeon
- Random shoutouts to subscribers
- Dramatic interactions with imaginary chat moderators

## Output Files

- Conversation logs are saved as: `napoleon_conversation_YYYYMMDD_HHMMSS.txt`
- Temporary speech files are saved as: `napoleon_speech.mp3`

## Error Handling

The script includes fallback mechanisms for:
- TTS failures (ElevenLabs → pyttsx3)
- Speech recognition issues
- API connection problems
- Model loading errors

## Note

This is a humorous project that combines historical and modern internet culture elements. The bot's responses are intentionally exaggerated and should be taken in a lighthearted context.

## Limitations

- Requires active internet connection for optimal performance
- ElevenLabs API has usage quotas
- Speech recognition accuracy may vary based on environmental conditions
- Local GPU recommended for optimal Ollama performance

## Future Improvements (TODOs)

- Add start/pause functionality for voice prompting
- Switch speech-to-text to use Whisper
- Implement better conversation context management
- Add more personality variations
- Improve French accent simulation


Feel free to use and modify this code for your own unhinged Napoleon needs!
