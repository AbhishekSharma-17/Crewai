from crewai import Task
from agents import researcher,writer
from tools import tool

research_task = Task(
    description=(
        "Identify next big trend in {topic}."
        "Focus on finding overall narative"
        "your final report should clearly articulate the key points,"
        "its market opportunity, and potential risks"
        ),
    expected_output= 'A comprehensive 4 paragraphs long report on Ai in education',
    tools= [tool],
    agent= researcher,
)
write_task = Task(
    description=(
        "Compose an insightful article on {topic}."
        "Focus on latest trend and how its impacting the industry"
        "The article should be easy to understand , engaging , and positive"
        "Mention the refrences and link , website names "
        ),
    expected_output= 'An elaborate article on {topic} advancements formatted as markdown.',
    tools= [tool],
    agent= writer,
    async_execution= False,
    output_file= 'new_blog.md'
)

