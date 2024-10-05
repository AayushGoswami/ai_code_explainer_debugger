import os
from dotenv import load_dotenv
import groq
import speech_recognition as sr

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = groq.Groq(api_key=api_key)

def generate_response_stream(messages):
    chat_completion = client.chat.completions.create(
        messages=messages,
        # model="llama-3.1-70b-versatile",
        model="gemma2-9b-it",
        temperature=0.7,
        top_p=0.9,
        stream=True,
    )
    return chat_completion

def explain_code(code, language, ):
    messages = [
        {
            "role": "system",
            "content": "You are an experienced software developer.\
                  You have been given a code script. Your tasks are:\
                  1. Breakdown the whole script into its containing functions.\
                  2. Show the functions as code block output.\
                  3. Provide a step-by-step explanation to each of these functions.\
                  4. Explain the purpose of each function or method in the code.\
                  5. Explain the data structures used in the code.\
                  6. Explain the algorithms used in the code.\
                  Please respond as if you were explaining the code to someone who is a beginner in software development or a student.",
        },
        {
            "role": "user",
            "content": f"Please explain this {language} code:\n\n```{language.lower()}\n{code}\n```"
        }
    ]
    return generate_response_stream(messages)

def debug_code(code, language, ):
    messages =  [
        {
            "role": "system",
            "content": "You are an expert debugger and code reviewer.\
                 Your task is to identify potential issues, bugs, or improvements in the given code.\
                     Provide clear explanations of the problems and suggest fixes or optimizations.\
                         If the code given to you is logically and functionally correct, then don't proceed with debugging it\
                            and just say that 'The code is absolutely fine!'",
        },
        {
            "role": "user",
            "content": f"Please debug this {language} code and suggest improvements:\n\n```{language.lower()}\n{code}\n```"
        }
    ]
    return generate_response_stream(messages)

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text, None
    except sr.UnknownValueError:
        return None, "Sorry, I couldn't understand that. Please try again."
    except sr.RequestError:
        return None, "Sorry, there was an error processing your request. Please try again later."