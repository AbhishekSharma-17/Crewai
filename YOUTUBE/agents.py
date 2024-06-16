from crewai import Agent
from tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()

# from langchain_groq import ChatGroq

# llm = ChatGroq(groq_api_key="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",
#                model_name="llama3-70b-8192",
#                temperature=0.6,
# )


llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        verbose=True,
        temperature=0.5,
    )

blog_researcher = Agent(
    role='professional Blog researcher agent from youtube videos',
    goal='Get relevant video content from the {topic} from youtube channel',
    verbose=True,
    memory=True,
    backstory=(
        "Expert in understanding youtube videos and transcribing them into blogposts"
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=True
)

blog_writer = Agent(
    role='Professional blog writer',
    goal='write compelling tech stories about the video {topic} from youtube channel',
    verbose=True,
    memory=True,
    backstory=(
        """Amazing blog writer who simplifies complex concepts and topics and writes engaging and captivating blogs, highly professional and consistent bringing amazing discoveries to light"""
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=False
)
