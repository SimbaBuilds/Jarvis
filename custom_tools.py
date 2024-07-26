import duckduckgo_search as DDGS
from openai import OpenAI

client = OpenAI()

__system = """
For your inforamtion:
Here is the path to the backend of the project: /Users/cameronhightower/Programming Projects/AI_Powered_Tutoring_Service/fastapi/app",
Path to front end: /Users/cameronhightower/Programming Projects/AI_Powered_Tutoring_Service/react_app/src
If you need something like a database url, username, password, help finding a file, etc.. to write the code, ask me

Example SQLAlchmey model:
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    access_token = Column(String(255), nullable=True)  
    token_type = Column(String(255), nullable=True)  
    username = Column(String(255), unique=True, nullable=False)

Example Pydantic schema:
class UpdateUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
"""


def append_script_to_file(nl_description):
    
    #logic/reasoning for filename later
    filename = "/Users/cameronhightower/Programming Projects/AI_Powered_Tutoring_Service/fastapi/app/models.py"
    system = """
    Create a SQL Alchemy model based on the NL Description given.
    Here is an example:
    class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    access_token = Column(String(255), nullable=True)  
    token_type = Column(String(255), nullable=True)  
    username = Column(String(255), unique=True, nullable=False)

    """
    content = nl_description

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": content},
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=messages
    )


    script_to_append = completion.choices[0].message.content


    try:
        # Open the file in append mode
        with open(filename, 'a') as file:
            # Append the script
            file.write('\n' + script_to_append + '\n')
        print(f"Script successfully appended to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")



# Define the search function using DuckDuckGo
def web_search(query):
    ddgs = DDGS()
    results = ddgs.text(query, max_results=5)
    return "\n".join([result['snippet'] for result in results])


