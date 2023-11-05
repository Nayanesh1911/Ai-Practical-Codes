import speech_recognition as sr
import nltk
from nltk.chat.util import Chat, reflections
from gtts import gTTS
import os
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import cv2

# Initialize the speech recognition
recognizer = sr.Recognizer()

# Define a simple chatbot
pairs = [
    ("Show me a cat video", ["Video: cat_video.mp4"]),
    ("Show me a cat", ["Image: cat.jpg"]),
    ("hello", ["Hi there!", "Hello!"]),
    ("how are you", ["I'm just a computer program, so I don't have feelings, but I'm here to help."]),
    ("goodbye", ["Goodbye!", "See you later!"]),
    ("what's your name", ["I'm just a computer program, so I don't have a name."]),
    ("What is AI", ["Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans. It is a multidisciplinary field of computer science that encompasses various techniques, algorithms, and approaches to create systems capable of performing tasks that typically require human intelligence. These tasks include, but are not limited to, problem-solving, reasoning, learning, understanding natural language, recognizing patterns, and making decisions."]),
    ("What is the capital of France?", ["The capital of France is Paris."]),
    ("Who wrote 'Romeo and Juliet'?", ["'Romeo and Juliet' was written by William Shakespeare."]),
    ("What is the largest planet in our solar system?", ["The largest planet in our solar system is Jupiter."]),
    ("Who painted the Mona Lisa?", ["The Mona Lisa was painted by Leonardo da Vinci."]),
    ("What is the boiling point of water in Celsius?", ["The boiling point of water in Celsius is 100 degrees."]),
    ("Who is the current President of the United States?", ["As of my last update in January 2022, the President of the United States is Joe Biden."]),
    # Add more patterns and responses as needed
]

chatbot = Chat(pairs, reflections)
''
# Function to convert text to speech
def speak(text):
    if text:
        tts = gTTS(text)
        tts.save("response.mp3")
        os.system("mpg321 response.mp3")

# Function to handle text input and display the response
def handle_text_input():
    user_input = user_input_text.get()
    if user_input:
        response = chatbot.respond(user_input)
        handle_response(response)

# Function to handle voice input
def voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        print("You said:", user_input)
        response = chatbot.respond(user_input)
        handle_response(response)
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
    except sr.RequestError:
        print("I'm having trouble connecting to the Google API. Please check your internet connection.")

# Function to handle both text and voice responses
def handle_response(response):
    print("Bot:", response)
    if response:
        if response.startswith("Image: "):
            image_path = response.replace("Image: ", "")
            display_image(image_path)
        elif response.startswith("Video: "):
            video_path = response.replace("Video: ", "")
            display_video(video_path)
        else:
            speak(response)
            response_text.set(response)

# Function to display an image
def display_image(image_path):
    response_text.set("")  # Clear the response text
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    image_label = tk.Label(root, image=photo)
    image_label.image = photo  # To prevent garbage collection
    image_label.pack()

# Function to display a video
def display_video(video_path):
    response_text.set("")  # Clear the response text
    cap = cv2.VideoCapture(video_path)

    def update():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(Image.fromarray(frame))
            video_label.config(image=photo)
            video_label.image = photo
            video_label.after(10, update)  # Adjust the delay (in milliseconds) for video playback speed

    video_label = tk.Label(root)
    video_label.pack()
    update()

# Create a GUI window
root = tk.Tk()
root.title("Chatbot")

# Create a text input field
user_input_text = tk.StringVar()
user_input_entry = tk.Entry(root, textvariable=user_input_text, width=40, font=("Helvetica", 16))
user_input_entry.pack()

# Create a button to submit text input
text_input_button = tk.Button(root, text="Submit Text Input", command=handle_text_input)
text_input_button.pack()

# Create a button for voice input
voice_button = tk.Button(root, text="Voice Input", command=voice_input, bg="white", fg="white")
voice_button.pack()

# Create a text variable to display the response
response_text = tk.StringVar()
response_label = tk.Label(root, textvariable=response_text, font=("Helvetica", 14), wraplength=800, fg="Red", justify="left")
response_label.pack()

root.mainloop()
