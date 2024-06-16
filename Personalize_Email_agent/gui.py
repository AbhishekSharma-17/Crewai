import tkinter as tk
from tkinter import filedialog, ttk
import ttkthemes
from agents import Email_personalization
from tasks import Email_task
import csv
from crewai import Crew
import time

email_template = """
Hey there, [Name]!

I hope this email finds you doing well. I wanted to reach out and remind you about our awesome gaming community. We're a vibrant group of passionate gamers who gather weekly for exciting gaming sessions, and we'd be thrilled to have you join us!

The best part? It's completely free! You'll have the opportunity to socialize, interact, and share your love for gaming with like-minded individuals. Whether you're a seasoned pro or just starting out, our community is a welcoming space where you can connect, grow, and have a blast!

In addition to our weekly gaming sessions, we also have a few streamers and esports players who regularly share their expertise and insights. You'll have the chance to learn from the best and take your gaming skills to the next level.

But that's not all! We also organize various gaming tournaments and events throughout the year, giving you the chance to showcase your skills and compete against other enthusiastic gamers. Who knows, you might even discover a hidden talent for competitive gaming!

If you have any questions or need help with any games, our community is the perfect place to find guidance and support. We're all here to help each other grow and have an amazing gaming experience.

So, what are you waiting for? Join our community today and unleash your inner gamer! We can't wait to have you on board and share countless hours of gaming fun together.

Best regards,
Abhishek Sharma
Community Manager
"""

class EmailPersonalizationGUI:
    def __init__(self, master):
        self.master = master
        master.title("Email Personalization")
        master.geometry("800x600")  # Larger window size

        # Apply a custom theme
        self.theme = ttkthemes.ThemedStyle(master)
        self.theme.set_theme("arc")  # Set the theme

        # Create GUI elements
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.file_label = ttk.Label(self.main_frame, text="Select CSV file with recipient data:", font=("Helvetica", 14, "bold"), style="Heading.TLabel")
        self.file_label.pack(pady=10)

        self.file_frame = ttk.Frame(self.main_frame)
        self.file_frame.pack(fill="x", pady=10)

        self.file_entry = ttk.Entry(self.file_frame, width=50, font=("Helvetica", 12))
        self.file_entry.pack(side="left", padx=5)

        self.browse_button = ttk.Button(self.file_frame, text="Browse", command=self.browse_file, style="Accent.TButton")
        self.browse_button.pack(side="left", padx=5)

        self.start_button = ttk.Button(self.main_frame, text="Start Personalization", command=self.start_personalization, style="Accent.TButton")
        self.start_button.pack(pady=10)

        self.progress_frame = ttk.Frame(self.main_frame)
        self.progress_frame.pack(pady=10)

        self.progress_label = ttk.Label(self.progress_frame, text="", font=("Helvetica", 12))
        self.progress_label.pack(side="left", padx=10)

        self.progress_bar = ttk.Progressbar(self.progress_frame, mode="determinate", length=300, style="Horizontal.TProgressbar")
        self.progress_bar.pack(side="left", padx=10)

        self.output_frame = ttk.Frame(self.main_frame)
        self.output_frame.pack(fill="both", expand=True, pady=10)

        self.output_text = tk.Text(self.output_frame, font=("Courier", 10), wrap="word")
        self.output_text.pack(fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.output_frame, command=self.output_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=self.scrollbar.set)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)

    def start_personalization(self):
        csv_file_path = self.file_entry.get()
        if not csv_file_path:
            self.progress_label.config(text="Please select a CSV file.")
            return

        # Clear the output text
        self.output_text.delete("1.0", "end")

        # Initialize the Email_personalization and Email_task classes
        agents = Email_personalization()
        email_personalizer = agents.personalize_email_agent()
        email_writer = agents.writer_agent()
        tasks = Email_task()

        personalize_email = []
        Writer_email = []

        # Read recipient data from the CSV file
        with open(csv_file_path, mode="r", newline="") as file:
            csv_reader = csv.DictReader(file)
            total_recipients = sum(1 for _ in csv_reader)
            file.seek(0)  # Reset the file pointer

            progress_step = 100 / (total_recipients * 2)
            current_progress = 0

            for row in csv_reader:
                # Extract recipient information from each row
                recipient = {
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "bio": row["bio"],
                    "last_conversation": row["last_conversation"],
                }

                # Append personalized email tasks and writer email tasks
                personalize_email.append(tasks.personalize_email(
                    agent=email_personalizer,
                    recipient=recipient,
                    email_template=email_template,
                ))
                current_progress += progress_step
                self.progress_bar["value"] = current_progress
                self.master.update_idletasks()

                Writer_email.append(tasks.writer_email(
                    agent=email_writer,
                    recipient=recipient,
                    draft_email=personalize_email[-1],
                ))
                current_progress += progress_step
                self.progress_bar["value"] = current_progress
                self.master.update_idletasks()

        # Initialize the Crew object with the agents and tasks
        crew = Crew(
            agents=[email_personalizer, email_writer],
            tasks=[*personalize_email, *Writer_email],
            max_rpm=29
        )

        # Measure the time it takes to kick off the crew
        start_time = time.time()
        result = crew.kickoff()
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Update the progress label with the elapsed time and crew usage metrics
        progress_text = f"Crew kickoff took {elapsed_time:.2f} seconds.\nCrew Usage: {crew.usage_metrics}"
        self.progress_label.config(text=progress_text)

        # Display the results in the output text area
        for task in crew.tasks:
            self.output_text.insert("end", f"{task.description}\n\n{task.output}\n\n")

root = tk.Tk()
app = EmailPersonalizationGUI(root)
root.mainloop()