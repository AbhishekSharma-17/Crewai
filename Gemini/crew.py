from crewai import Crew,Process
from tasks import research_task,write_task
from agents import researcher,writer
crew =  Crew(
    agents=[researcher,writer],
    tasks=[research_task,write_task],
    process=Process.sequential,
    
)

inputs = {'topic': 'AI in Health care'}
result = crew.kickoff(inputs=inputs)
print(result)