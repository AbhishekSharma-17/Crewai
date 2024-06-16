from crewai import Task


class Email_task:
    def personalize_email(self, agent, recipient, email_template):
        return Task(
            description=f"""
            Personalize the template email for recipient using their information.
            
            -Name : {recipient['first_name']}{recipient['last_name']}
            -Email : {recipient['email']}
            -Bio : {recipient['bio']}
            -Last conversation : {recipient['last_conversation']}

            Import info to consider :
            -When personalizing te email, only use one sentence from the bio or last conversation.
            And make sure to incoparate it naturally  to the email. without going too much in detail.
            -Make sure to keep the updated email roughly the same length as  the template email.
            
            the template email as follow:
           
            '''{email_template}'''
            
            """,
            agent=agent,
            expected_output=f"Personalized email draft.",
            # async_execution=True,
        )

    def writer_email(self, agent, draft_email, recipient):
         return Task(
          description=f"""
            Revise the draft email to adopt the following writing style.

            Writing Style:

            - Use an informal, engaging, and slightly sales-oriented tone, mirroring Ghostwriter's final email communication style.
            - This approach prioritizes clear, direct communication while maintaining a friendly and approachable tone.
            - Use straightforward language, including phrases like "Hey [Name]!" to start emails or messages.
            The tone will be optimistic and encouraging, aiming to build a positive relationship with the person you are communicating with, while staying grounded in practicality.

            Important Notes:
            - Don't use emojis.
            """,
        agent=agent,
        context=[draft_email],
        expected_output="A revised email draft in Ghostwriter's specified tone and style.",
        output_file=f"Output/{recipient['first_name']}_{recipient['last_name']}.txt"
    ) 
