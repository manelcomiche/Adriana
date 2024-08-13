# 🌟 Adriana: The Voice Assistant Bot for Discord 🌟

Welcome to **Adriana**, a Discord bot designed to provide audio-to-text in real-time implementing also special weather updates using voice commands! Originally conceived as speech-to-text bot, Adriana evolved into a more powerful assistant capable of converting voice messages into text, processing them with Whisper, and responding with synthesized speech (tts). 🎙️

## 🎯 Project Overview

Adriana started as a humble idea: a bot that could transcribe audio messages in Discord. However, as the project progressed, it became clear that the bot could do much more! Now, Adriana not only transcribes your voice messages but also processes them to provide intelligent responses, including live weather updates for any city you ask about. 🌦️

## 🚀 Features

- **Speech-to-Text**: Adriana listens to your voice messages and converts them into text using advanced transcription technology. 📝
- **Intelligent Responses**: Using GPT, Adriana provides meaningful responses based on your voice input. 🤖
- **Weather Updates**: Simply ask, "What's the weather like in [City]?" and Adriana will give you a brief, accurate weather report. ☁️
- **Text-to-Speech**: Adriana converts the responses back into speech and plays them in your voice channel. 🎧

### 📦 Requirements

To run the current transcription script, you'll need to install the necessary Python packages. These are listed in the `requirements.txt` file.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/manelcomiche/adriana.git
   cd ADRIANA
   ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the transcription script:
    ```bash
    python adriana.py
    ```

## 🧰 Dependencies
The project currently relies on the following Python libraries:
- 🗣️ SpeechRecognition
- 🎧 PyAudio


## 📚 How It Works
- Voice Message Transcription:
    - Adriana transcribes the audio message using the NAGA API. The transcription is then processed to detect whether the user is asking about the weather.

- Weather Check:
    - If the message contains a weather query, Adriana fetches the latest weather data for the requested city using the WeatherAPI.

- GPT Processing:
    - The weather information or any other input is processed by GPT, generating a natural language response.

- Speech Synthesis:
    - Finally, Adriana converts the text response into speech using a TTS API and plays it back in the voice channel.

## 💡 Original Concept

The initial concept for Adriana was to develop a straightforward speech-to-text bot for Discord. However, given that I only had two days to complete this project, implementing a full-fledged voice assistant that handles continuous speech recognition and processes voice chunks in real-time was quite challenging, especially as one of my first Discord bot projects (in python). As development progressed, I decided to pivot and enhance Adriana with more interactive and useful features, resulting in its current form as a voice assistant capable of providing real-time information and intelligent responses.


## 🤝 Contributing
Contributions are welcome! Feel free to submit issues, feature requests, or pull requests to help improve ADRIANA.

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for more details.

Made with ❤️ by Manel Comiche.