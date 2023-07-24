# TalkToChatGPT
Simple Python class that enables users to talk to ChatGPT (via API call), using voice or typing questions

Usage is simple, but there are some requirements. You need OpenAI API key. Just follow these steps to get it:

## Step 1: Create an OpenAI Account

First, you'll need an account on OpenAI. If you don't have one already, go to the [OpenAI website](https://beta.openai.com/signup/) and sign up.

## Step 2: Navigate to the API Key Section

After signing in to your account, navigate to the API Keys section. This can typically be found in the account settings or dashboard.

## Step 3: Generate a New API Key

Click on the button that says "Create a new API Key" or similar. Follow the prompts to generate a new key. 

Be sure to note down your API key in a safe place, as it will not be shown again. However, if you lose it, you can always generate a new one.

I'm using edge_tts (https://pypi.org/project/edge-tts/) for text to speech and speech_recognition module (https://pypi.org/project/SpeechRecognition/) for speech recognition using microphone. Be sure to installed, as well as other requirements.

# How to use the class?

It is simple, for example:

```
assistant = TalkToChatGPT(voice="en-US-JennyNeural", output_file="test.mp3", input_type="voice", language="en-US")
asyncio.run(assistant.main())
```
There is also helpful method (get_available_voices()) which pretty prints the dictionary with all available voice for text to speech in edge_tts. You can call like like:

```
asyncio.run(assistant.get_available_voices())
```

