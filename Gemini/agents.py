from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from tools import tool

from dotenv import load_dotenv
load_dotenv()

#set the gemini model

llm = ChatGoogleGenerativeAI(
                            model="gemini-1.5-flash",
                            verbose=True,
                            temperature=0.5,
                            google_api_key=os.getenv("GOOGLE_API_KEY"),
                             )


researcher = Agent(
    role= "Senior Researcher",
    goal= 'Uncover ground breaking technologies in {topic}',
    verbose= True,
    memory= True,
    backstory= (
               "Driven by curiosity , you're at the forefront of inovation, eager to share and explore and share knowledge that could change the world"
                ),
    tools= [tool],
    llm= llm,
    allow_delegation= True,
)
writer = Agent(
    role= "Professional writter",
    goal= 'Narrate compelling tech stories about {topic}',
    verbose= True,
    memory= True,
    backstory= (
                "Craft engaging narratives which are captivating"
                "Simplify complex topics without altering the meaning"
                "Amazing writer who formats evrything properly"
                ),
    tools= [tool],
    llm= llm,
    allow_delegation= False,
)

