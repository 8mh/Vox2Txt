"""
Vox2Txt: Azure Speech-to-Text #vox2txt
Free tier mic/file transcription.
Post results to r/Vox2text!
"""
import azure.cognitiveservices.speech as speechsdk
import sys

# #vox2txt Config
SPEECH_KEY = os.getenv("VOX2TXT_KEY")     # Azure Key 1
SPEECH_REGION = "northeurope"  # e.g., "eastus"

print("🚀 Vox2Txt #vox2txt – Join r/Vox2text for feedback!")

def recognize_mic():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_recognition_language = "en-US"  # en-US, el-GR, etc.

    audio_config = speechsdk.audio.AudioConfig(use_default_mic=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)

    print("🎤 Speak... (Ctrl+C to stop)")

    def on_recognized(evt):
        text = evt.result.text.strip()
        if text: print(f"📝 {text}")

    def on_canceled(evt):
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"❌ {evt.error_details}")

    recognizer.recognized.connect(on_recognized)
    recognizer.canceled.connect(on_canceled)
    recognizer.start_continuous_recognition()
    
    try: input("\nPress Enter to stop...\n")
    finally: recognizer.stop_continuous_recognition()

def recognize_file(file_path):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioConfig(filename=file_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)

    result = recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"📄 {result.text}")
        with open("vox2txt_transcript.txt", "w") as f:
            f.write(result.text)
        print("💾 Saved to vox2txt_transcript.txt")
    else:
        print(f"❌ {result.reason}")

if __name__ == "__main__":
    print("1: 🎤 Mic | 2: 📁 File")
    choice = input("Choose: ").strip()
    if choice == "1":
        recognize_mic()
    elif choice == "2":
        file_path = input("File path (WAV/MP3): ").strip()
        if file_path: recognize_file(file_path)
    else:
        print("Invalid – rerun!")