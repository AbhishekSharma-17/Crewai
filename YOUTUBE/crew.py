from crewai import Crew, Process
from tasks import research_task, write_task
from agents import blog_researcher,blog_writer

crew = Crew(
        agents=[blog_researcher,blog_writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        memory=True,
        cache=True,
        max_rpm=100,
        share_crew=True
    )

input = {'topic': 'Fabric: This OPENSOURCE AI Framework can AUTOMATE YOUR LIFE & ANY TASK (Setup with Ollama & Groq)'}
result = crew.kickoff(inputs=input)

print(result)
    