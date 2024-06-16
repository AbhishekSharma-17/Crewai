from langchain_groq import ChatGroq
from crewai import Agent


class Email_personalization:
    def __init__(self):
        self.llm = ChatGroq(
            api_key="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",
            model="llama3-70b-8192",
            temperature=0.2,
        )

    def personalize_email_agent(self):
        return Agent(
            role="Email Personalazier",
            goal=f"""
            Personalize template email for recipient using this information.
            
            Give me a template email and recipient information (name,email,bio,last conversation),
            personalize the email while maintaning the core message and structure of original email.
            This involves updating the  introcuctionn, body, and closing of  email to make it more personal and engaging foor each recipient.             
            """,
            backstory="""
            As an email personalizer, you are responsible  for customizing the template email for indivisual recipient
            
            """,
            verbose=True,
            llm=self.llm,
            max_iter=2,
        )

    def writer_agent(self):
        return Agent(
            role="Writer",
            goal=f"""
            Revise draft emails to adopt the ghostwriter's writing style.
            
            Use an informal, engaging, and slightly sales oriented tone, mirroring the ghostwriter's final communication style.
            
            """,
            backstory="""
            As a ghostwriter you are responsible for revising draf email to match the ghostwriter's writing style
            focusing on clear direct communication with a friendly and approachable tone.
            """,
            verbose=True,
            llm=self.llm,
            max_iter=2,
        )
