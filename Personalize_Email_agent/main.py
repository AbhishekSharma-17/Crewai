import time
from agents import Email_personalization
from tasks import Email_task
import csv
from crewai import Crew

# Define the email template to be personalized
email_template = """
Heyy [Name]! 

Just a quick reminder that we have a new club where you can join us for weekly gaming sessions. The club is totally free and we can socialize and interact and enjoy gaming together. 
we'd love to have you join us ! If you have any question or need help withh any games, this is a great place to connect and grow a community.
we have well over 100 people on our community if you are inttrested you can join aswell apart from that we have a few streamers and esports players aswell.

Best regards, 
Abhishek Sharma 
"""

# Initialize the Email_personalization and Email_task classes
agents = Email_personalization()

email_personalizer = agents.personalize_email_agent()
email_writer = agents.writer_agent()


tasks = Email_task()

personalize_email = []
Writer_email = []

# Define the path to the CSV file containing recipient data
csv_file_path = "data/client_medium_data.csv"

# Read recipient data from the CSV file
with open(csv_file_path, mode="r",newline="") as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        # Extract recipient information from each row
        recipient = {
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "email": row["email"],
            "bio": row["bio"],
            "last_conversation": row["last_conversation"],
        }
        
        # Append a personalized email task to the personalize_email list
        personalize_email.append(tasks.personalize_email(
            agent=email_personalizer,
            recipient=recipient,
            email_template=email_template,
        ))
        
        # Append a written email task to the Writer_email list
        Writer_email.append(tasks.writer_email(
            agent=email_writer,
            recipient=recipient,
            draft_email=personalize_email[-1], # Use the last personalized email as the draft for writing
        ))
        
        personalize_email.append(tasks.personalize_email(
            agent=email_personalizer,
            recipient=recipient,
            email_template=email_template,
        ))

# Initialize the Crew object with the agents and tasks
        Writer_email.append(tasks.writer_email(
            agent=email_writer,
            recipient=recipient,
            draft_email=personalize_email[-1], # Use the last personalized email as the draft for writing
        ))

# Initialize the Crew object with the agents and tasks
crew = Crew(
    agents = [email_personalizer,email_writer],
    tasks = [
        *personalize_email,
        *Writer_email
    ],
    max_rpm = 29
)

# Measure the time it takes to kick off the crew
start_time = time.time()

result = crew.kickoff()

end_time = time.time()
elapsed_time = end_time - start_time

# Print the elapsed time and crew usage metrics
print(f"Crew kickoff took {elapsed_time} Seconds.")
print("Crew Usage", crew.usage_metrics)


