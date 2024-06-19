from openai import OpenAI
import time
from pygame import mixer
import os
import json

client = OpenAI(default_headers={"OpenAI-Beta": "assistants=v2"})
mixer.init()

def get_assistant_ids():

    assistant_ids_file_path = 'jarvis-project/assistant_ids.json'

    # If there is an assistant_ids.json file already, then load that assistant
    if os.path.exists(assistant_ids_file_path):
        with open(assistant_ids_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            thread_id = assistant_data['thread_id']

    else:
        assistant = client.beta.assistants.create(
        name="Jarvis",
        instructions="You are a personal assistant modeled after Jarvis in Ironman.  Keep your responses brief and to the point.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4o",
        )
        thread = client.beta.threads.create()

        # Create a new assistant.json file to load on future runs
        with open(assistant_ids_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id, 'thread_id': thread.id}, file)
            print("Created a new assistant and saved the IDs.")
        
        assistant_id = assistant.id
        thread_id = thread.id
 
    
    return assistant_id, thread_id


assistant_id, thread_id = get_assistant_ids()

# Retrieve the assistant and thread
assistant = client.beta.assistants.retrieve(assistant_id)
thread = client.beta.threads.retrieve(thread_id)

def ask_question_memory(question):
    global thread
    client.beta.threads.messages.create(thread.id, role="user", content=question)
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
    
    while (run_status := client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)).status != 'completed':
        if run_status.status == 'failed':
            return "The run failed."
        time.sleep(1)
    
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value

def generate_tts(sentence, speech_file_path):
    response = client.audio.speech.create(model="tts-1", voice="echo", input=sentence)
    response.stream_to_file(speech_file_path)
    return str(speech_file_path)

def play_sound(file_path):
    mixer.music.load(file_path)
    mixer.music.play()

def TTS(text):
    speech_file_path = generate_tts(text, "speech.mp3")
    play_sound(speech_file_path)
    while mixer.music.get_busy():
        time.sleep(1)
    mixer.music.unload()
    os.remove(speech_file_path)
    return "done"
