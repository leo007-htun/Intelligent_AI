from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 200)  # speech_rate
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)

todo_list = []


def create_note():
    global recognizer
    speaker.say("what would you like to write in your note?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("choose a file name")
                speaker.runAndWait()
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"note has been successfully created {filename}")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()  # reinitialize
            speaker.say("I do not understand")
            speaker.runAndWait()


def add_todo():
    global recognizer
    speaker.say("What todo, would you like to add")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

            item = recognizer.recognize_google(audio)
            item = item.lower()

            todo_list.append(item)
            done = True
            speaker.say(f"{item} has been added to todo list")
            speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I do not understand")
            speaker.runAndWait()


def show_todos():
    speaker.say("Your todo list are as follows:")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def greetings():
    speaker.say("Hello, what can I do for you?")
    speaker.runAndWait()


def quit():
    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit(0)


mapping = {'greeting': greetings,
           'create_note': create_note,
           'add_todo': add_todo,
           'show_todos': show_todos,
           'exit': quit
           }

assistant = GenericAssistant('intents.json', intent_methods=mapping)
assistant.train_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
