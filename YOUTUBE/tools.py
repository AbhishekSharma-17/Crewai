from crewai_tools import YoutubeChannelSearchTool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
import os

api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(api_key=api_key,
                             model="gemini-1.5-flash"
                             )

tool = YoutubeChannelSearchTool(
    youtube_channel_handle='@AICodeKing',
    config=dict(
        llm=dict(
            provider="google", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="gemini-1.5-flash",
                temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google", # or openai, ollama, ...
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
                                
  )