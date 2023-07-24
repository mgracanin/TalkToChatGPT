# TalkToChatGPT

This is a simple class called TalkToChatGPT that interacts with OpenAI's ChatGPT model to have a conversation. The class has methods for initializing the instance, getting user input either from voice or text, converting text to speech, playing the generated speech, typing text on the console, asking a question to the ChatGPT model, getting available voices for text-to-speech conversion, and running the conversation. The main method orchestrates the conversation by asking a question, converting the response to speech, and playing it. 

Keep in mind that the text_to_speech method takes a string as input and asynchronously converts it to speech using the edge_tts.Communicate class and then the output speech is saved to an mp3 file (in the same directory where the talking_chatgpt.py is located). Please note that each new output overwrites the previous mp3 file. Also, keep in mind the playing of the mp3 file will work only on Windows since I'm using winmm.dll and mciSendString function that sends a command string to an MCI device which is, in this case, an mp3 file (https://learn.microsoft.com/en-us/previous-versions/dd757161(v=vs.85)). You can easliy use any other Python module for this like playsound (https://pypi.org/project/playsound/).

The model in use is gpt-3.5-turbo-0613, but you can change it to any other OpenAI supported model (https://platform.openai.com/docs/models).

This script relies on several external libraries, including openai for interacting with the OpenAI API (https://pypi.org/project/openai/), edge_tts for text-to-speech (https://pypi.org/project/edge-tts/), SpeechRecognition for speech recognition (https://pypi.org/project/SpeechRecognition/), ctypes and winmm for playing mp3 files, asyncio for running asynchronous tasks, and json for printing json formatted data. 

You can install them using following command:

```
pip install openai edge_tts SpeechRecognition
```

Alos, for this to work, you'll need OpenAI API key. Just follow these steps to get it:

### Step 1: Create an OpenAI Account

First, you'll need an account on OpenAI. If you don't have one already, go to the [OpenAI website](https://beta.openai.com/signup/) and sign up.

### Step 2: Navigate to the API Key Section

After signing in to your account, navigate to the API Keys section. This can typically be found in the account settings or dashboard.

### Step 3: Generate a New API Key

Click on the button that says "Create a new API Key" or similar. Follow the prompts to generate a new key. 

Be sure to note down your API key in a safe place, as it will not be shown again. However, if you lose it, you can always generate a new one.

Then you can define it either as an environment variable or using API_KEY variable directly in the code.

## How to use the TalkToChatGPT?

Just create an instance of the TalkToChatGPT, and run it within the asyncio.run() function, as follows:

```
assistant = TalkToChatGPT(voice="en-US-JennyNeural", output_file="test.mp3", input_type="voice", language="en-US")
asyncio.run(assistant.main())
```

The TalkToChatGPT class includes a convenient method called get_available_voices(). This method queries and displays all the available voices that can be used for the text-to-speech functionality in edge_tts. The output is formatted as a dictionary, with each entry indicating a voice's friendly name and its corresponding short name which is used as a parameter when creating an instance of TalkToChatGPT. This way you can easily find out what languages are supported and how to use them.

To use this method and list all the available voices, simply call get_available_voices() on an instance of TalkToChatGPT within the asyncio.run() function:

```
asyncio.run(assistant.get_available_voices())
```

Remember to replace assistant with your instance of TalkToChatGPT class. This call will execute the get_available_voices() method asynchronously, listing all possible voices for your text-to-speech needs.

