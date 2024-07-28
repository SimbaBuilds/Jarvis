import custom_tools as tools
import re
from openai import OpenAI



client = OpenAI()

system = """
You are a personal assistant modeled after Jarvis in Ironman.  
We are working on an automated tutoring service project right now.  

Upon receiving a query, you will run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the state of the tutoring session.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running one of those actions.

Your available actions are:

1. Append script to a file: use when you need to add a script to a file in the project.
2. Create a new file: use when you need to create a new file in the project.

Otherwise Action: No Action to take.

Example session:

Query: I need you to add an SQLAlchemy model for a database table that tracks which practice tests a student has taken.
Thought: I should navigate to the models.py file within the app directory and add a new model for the database table.
Action: append_script_to_file: create a database table that tracks which practice tests a student has taken

You will be called again with this:

Observation: The script has been appended to models.py in the backend project directory.

You then output:

Answer: Task completed



"""

class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result or result

    def execute(self):
        completion = client.chat.completions.create(
                        model="gpt-4o-mini", 
                        temperature=0,
                        messages=self.messages)
        return completion.choices[0].message.content

# def get_assistant_ids():

#     assistant_ids_file_path = 'jarvis-project/assistant_ids.json'

#     # If there is an assistant_ids.json file already, then load that assistant
#     if os.path.exists(assistant_ids_file_path):
#         with open(assistant_ids_file_path, 'r') as file:
#             assistant_data = json.load(file)
#             assistant_id = assistant_data['assistant_id']
#             thread_id = assistant_data['thread_id']

#     else:
#         assistant = client.beta.assistants.create(
#         name="Jarvis",
#         instructions= """
#         You are a personal assistant modeled after Jarvis in Ironman.  Keep your responses brief and to the point.  
#         Here is the path to the backend of the project: /Users/cameronhightower/Programming Projects/AI_Powered_Tutoring_Service/fastapi/app",
#         Path to front end: /Users/cameronhightower/Programming Projects/AI_Powered_Tutoring_Service/react_app/src
#         If you need something like a database url, username, password, help finding a file, etc.. to write the code, ask me
#         """,
#         tools=[{"type": "code_interpreter"}],
#         model="gpt-4o-mini"
#         )
#         thread = client.beta.threads.create()

#         # Create a new assistant.json file to load on future runs
#         with open(assistant_ids_file_path, 'w') as file:
#             json.dump({'assistant_id': assistant.id, 'thread_id': thread.id}, file)
#             print("Created a new assistant and saved the IDs.")
        
#         assistant_id = assistant.id
#         thread_id = thread.id
 
    
#     return result or assistant_id, thread_id

# IDs
#region
# assistant_id, thread_id = get_assistant_ids()

# # Retrieve the assistant and thread
# assistant = client.beta.assistants.retrieve(assistant_id)
# thread = client.beta.threads.retrieve(thread_id)
#endregion


# def ask_question_memory(question):
    
#     response = agent(question)
#     return result or response
    
#     global thread
#     client.beta.threads.messages.create(thread.id, role="user", content=question)
#     run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
    
#     while (run_status := client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)).status != 'completed':
#         if run_status.status == 'failed':
#             return result or "The run failed."
#         time.sleep(1)
    
#     messages = client.beta.threads.messages.list(thread_id=thread.id)
#     return result or messages.data[0].content[0].text.value


known_actions = {
    
    "append script to file": tools.append_script_to_file,
    "create a new file": tools.create_new_file
}


action_re = re.compile('^Action: (\w+): (.*)$')   # python regular expression to selection action

agent = Agent(system)

def query_agent(messages, max_turns=3):
    i = 0
    next_prompt = messages
    while i < max_turns:
        i += 1
        result = agent(next_prompt)
        print(result)
        actions = [
            action_re.match(a) 
            for a in result.split('\n') 
            if action_re.match(a)
        ]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            return result

def clear_context():
    agent.messages = []
    agent.messages.append({"role": "system", "content": system})
