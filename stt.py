"""
Vox2Txt: Azure Speech-to-Text #vox2txt
Free tier mic/file transcription.
Post results to r/Vox2text!
"""
import azure.cognitiveservices.speech as speechsdk
import sys
import os

# Secure Config (ENV Vars)
SPEECH_KEY = os.getenv("VOX2TXT_KEY")
SPEECH_REGION = os.getenv("VOX2TXT_REGION")

if not SPEECH_KEY or not SPEECH_REGION:
    print("Set ENV VARS:")
    print("Win PS: $env:VOX2TXT_KEY='key' ; $env:VOX2TXT_REGION='eastus'")
    print("Mac/Lin: export VOX2TXT_KEY='key' ; export VOX2TXT_REGION='eastus'")
    sys.exit(1)

print("Vox2Txt #vox2txt Ready!")

def recognize_mic():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_recognition_language = "en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak now... (Press Enter to stop)")

    def on_recognized(evt):
        text = evt.result.text.strip()
        if text: print(text)  # <-- EMOJI REMOVED HERE

    def on_canceled(evt):
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"ERROR: {evt.error_details}")

    recognizer.recognized.connect(on_recognized)
    recognizer.canceled.connect(on_canceled)
    recognizer.start_continuous_recognition()
    
    try: input("\nPress Enter to stop...")
    finally: recognizer.stop_continuous_recognition()

def recognize_file(file_path):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioConfig(filename=file_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Transcript: {result.text}")
        with open("vox2txt_transcript.txt", "w", encoding="utf-8") as f:
            f.write(result.text)
        print("Saved to vox2txt_transcript.txt")
    else:
        print(f"Error: {result.reason}")

if __name__ == "__main__":
    print("1: Microphone | 2: File")
    choice = input("Choose: ").strip()
    if choice == "1": recognize_mic()
    elif choice == "2":
        file_path = input("File path (WAV/MP3): ").strip()
        if file_path: recognize_file(file_path)
    else: print("Invalid choice!")
