import os
import asyncio
import openai
import edge_tts
import time
import ctypes
import json
import sys
import speech_recognition as sr
from pathlib import Path

API_KEY = ''
os.chdir(Path(__file__).parent)

# Set OpenAI API key
try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except KeyError:
    if API_KEY:
        openai.api_key = API_KEY
    else:
        print(
            "Open AI API key is needed. Please define it either as an environment variable or using API_KEY variable directly in the code.")
        sys.exit(1)


class TalkToChatGPT:
    def __init__(self, voice: str, output_file: str, input_type: str, language:str):
        """
        Initializes a new instance of the class with the specified voice, output file, and input type.

        :param voice: A str representing the voice to use. You can find list of voices using get_available_voices() method.
        :param output_file: A str representing the output file fot the generated Mp3.
        :param input_type: A str representing the type of input to use ("text" or "voice"). Will fallback to text if Microphone fails.
        :param  language: A str representing the language to use for speech recognition (use ISO language codes like "en-US" for English or "hr-HR" for Croatian).
        """
        self.voice = voice
        self.language = language
        self.output_file = output_file
        self.input_type = input_type
        self.chat_history = [
            {"role": "system", "content": "You are a smart and helpful assistant."}
        ]

    def get_input(self):
        """
        Gets input from the user based on the input type specified during initialization.
        If input type is "voice", listens to microphone and uses Google speech recognition to convert speech to text.
        Returns the user's input.
        """
        if self.input_type == "voice":
            pr_govor = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    audio = pr_govor.listen(source)
                question = pr_govor.recognize_google(audio, language=self.language)
                return question
            except:
                print("Error: microphone not detected or audio not recognized. Falling back to entering text manually...")
                return input("Type your question: ")
        else:
            return input("Type your question: ")

    async def text_to_speech(self, text: str) -> None:
        """
        Asynchronously converts the given text to speech and saves the output to and mp3 file.

        :param text: A string representing the text to be converted to speech.

        :return: None
        """
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(self.output_file)

    def play_mp3(self, mp3file) -> None:
        """
        Plays an MP3 file using the Windows Multimedia API. This only works on Windows.

        Args:
            mp3file (str): The path to the MP3 file to be played.
        """
        try:
            winmm = ctypes.windll.winmm
            result = winmm.mciSendStringW(f"open \"{mp3file}\" type MPEGVideo alias mp3", None, 0, None) ## sending open command to Windows Media Control Interface, https://learn.microsoft.com/en-us/windows/win32/multimedia/open
            
            if result != 0:  # means an error occurred
                raise Exception(f"Can't open file: error {result}")
            
            result = winmm.mciSendStringW("play mp3", None, 0, None) ## sending play command to WMC using mciSendStringW
            if result != 0:
                raise Exception(f"Can't play file: error {result}")
            
            while True:  # check status in a loop until playing is done
                buffer = ctypes.create_unicode_buffer(255)
                result = winmm.mciSendStringW("status mp3 mode", buffer, 254, None)
                
                if result != 0:
                    raise Exception(f"Can't check status: error {result}")
                elif buffer.value != "playing":
                    break
                
                time.sleep(0.1)
            
        except Exception as e:
            print(f"Sorry, there was an unexptected error: {e}")
    
        winmm.mciSendStringW("close mp3", None, 0, None)

    def type_text(self, text: str, typing_rate=0.08):  # adjust typing_rate value to change the speed
        for char in text:
            print(char, end='', flush=True)
            time.sleep(typing_rate)

    async def ask_question(self) -> str:
        """
        Asynchronously asks a question and returns the response.

        :return: A string representing the response to the question.
        :rtype: str
        """
        try:
            upit = self.get_input()
            self.chat_history.append({"role": "user", "content": upit})
            print("Waiting for response to be generated...")
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", messages=self.chat_history)
            return chat.choices[0].message.content

        except Exception as e:
            print(f"Error -> {e}")
            return ""

    #Pretty prints dictionary for all available voices in edge_tts using json.dumps()
    async def get_available_voices(self):
        voices = await edge_tts.list_voices()
        voices_sorted = sorted(voices, key=lambda voice: voice['ShortName']) ## sorting by short name, e.g. "en-US-GabrielaNeural" or "hr-HR-GabrijelaNeural"
        voices_dictionary = {voice['FriendlyName']: voice['ShortName'] for voice in voices_sorted}
        print(json.dumps(voices_dictionary, indent=4))

    async def main(self) -> None:
        text = await self.ask_question()
        await self.text_to_speech(text)

        ## Runing functions concurrently
        await asyncio.gather(
            asyncio.to_thread(self.type_text, text),
            asyncio.to_thread(self.play_mp3, self.output_file)
        )


if __name__ == "__main__":
    assistant = TalkToChatGPT(voice="en-US-JennyNeural", output_file="test.mp3", input_type="voice", language="en-US")
    asyncio.run(assistant.main())
    #asyncio.run(assistant.get_available_voices())

