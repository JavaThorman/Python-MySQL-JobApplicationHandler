import os
from os import access

from Database.database import Database
import customtkinter as ctk

class JobApplicationTrackerUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Job Application Tracker")

        # Maximize the window at startup
        self.state('zoomed')

        # Configure grid to make the frames stretch with resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialize the database
        self.db = Database()
        # Initialize the db tables
        self.db.create_table()  # Ensure tables are created

        # Create frames for different views (initialize only once)
        self.menu_frame = ctk.CTkFrame(self)
        self.add_frame = ctk.CTkFrame(self)
        self.show_frame = ctk.CTkFrame(self)
        self.update_frame = ctk.CTkFrame(self)
        self.response_frame = ctk.CTkFrame(self)
        self.delete_frame = ctk.CTkFrame(self)

        # Feedback label for showing success/error messages
        self.feedback_label = ctk.CTkLabel(self, text="", font=("Arial", 14), fg_color="green")
        self.feedback_label.grid(row=1, column=0, padx=20, pady=10)

        # Start by showing the main menu
        self.show_menu()
    def clear_feedback_message(self):
            """Clear the feedback message."""
            self.feedback_label.configure(text="")

    def show_feedback_message(self, message, success=True):
        """Show feedback message in the main window."""
        self.feedback_label.configure(text=message, fg_color="green" if success else "red")
        # Hide the feedback message after 3 seconds
        self.after(3000, self.clear_feedback_message)



    def show_menu(self):
        """Show the main menu with action buttons."""
        # Clear existing content in frames (hide all frames)
        self.clear_all_frames()

        # Title
        if not hasattr(self, 'title_label'):
            self.title_label = ctk.CTkLabel(self.menu_frame, text="Job Application Tracker", font=("Arial", 20, "bold"))
            self.title_label.pack(pady=20)

        # Buttons (create once)
        if not hasattr(self, 'add_button'):
            self.add_button = ctk.CTkButton(self.menu_frame, text="Add Job Application", command=self.show_add_application)
            self.add_button.pack(pady=10)

            self.show_button = ctk.CTkButton(self.menu_frame, text="Show All Applications", command=self.show_all_applications)
            self.show_button.pack(pady=10)

            self.update_button = ctk.CTkButton(self.menu_frame, text="Update Application", command=self.show_update_application)
            self.update_button.pack(pady=10)

            self.response_button = ctk.CTkButton(self.menu_frame, text="Add Response to Application", command=self.show_add_response)
            self.response_button.pack(pady=10)

            self.delete_button = ctk.CTkButton(self.menu_frame, text="Delete Application", command=self.show_delete_application)
            self.delete_button.pack(pady=10)

            self.exit_button = ctk.CTkButton(self.menu_frame, text="Exit", command=self.exit_program)
            self.exit_button.pack(pady=10)

        # Show the menu frame
        self.menu_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def show_add_application(self):
        """Show the add job application form."""
        self.clear_all_frames()  # Clear other frames

        # Initialize add_frame if not already initialized
        if not hasattr(self, 'add_frame'):
            self.add_frame = ctk.CTkFrame(self.root)  # Replace `self.root` with the parent frame

        # Back Button
        if not hasattr(self, 'back_button_add'):
            self.back_button_add = ctk.CTkButton(self.add_frame, text="Back", command=self.show_menu)
            self.back_button_add.grid(row=0, column=0, padx=10, pady=10)  # Use grid instead of pack

        # Labels and Entries
        if not hasattr(self, 'job_provider_entry'):
            ctk.CTkLabel(self.add_frame, text="Job Provider:").grid(row=1, column=0, padx=10, pady=5)
            self.job_provider_entry = ctk.CTkEntry(self.add_frame)
            self.job_provider_entry.grid(row=1, column=1, padx=10, pady=5)

            ctk.CTkLabel(self.add_frame, text="Job Description:").grid(row=2, column=0, padx=10, pady=5)
            self.job_description_entry = ctk.CTkEntry(self.add_frame)
            self.job_description_entry.grid(row=2, column=1, padx=10, pady=5)

            ctk.CTkLabel(self.add_frame, text="Job Link:").grid(row=3, column=0, padx=10, pady=5)
            self.job_link_entry = ctk.CTkEntry(self.add_frame)
            self.job_link_entry.grid(row=3, column=1, padx=10, pady=5)

            ctk.CTkLabel(self.add_frame, text="Resume Used:").grid(row=4, column=0, padx=10, pady=5)
            self.resume_entry = ctk.CTkEntry(self.add_frame)
            self.resume_entry.grid(row=4, column=1, padx=10, pady=5)

            ctk.CTkLabel(self.add_frame, text="Personal Letter Used:").grid(row=5, column=0, padx=10, pady=5)
            self.letter_entry = ctk.CTkEntry(self.add_frame)
            self.letter_entry.grid(row=5, column=1, padx=10, pady=5)

            # Submit Button
            self.submit_button_add = ctk.CTkButton(self.add_frame, text="Submit", command=self.submit_add_application)
            self.submit_button_add.grid(row=6, columnspan=2, pady=20)  # Center the button

        # Show the add frame
        self.add_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def submit_add_application(self):
        """Submit the new job application."""
        # Call the insert_job_application method and get the result
        result = self.db.insert_job_application(
            self.job_provider_entry.get(),
            self.job_description_entry.get(),
            self.job_link_entry.get(),
            self.resume_entry.get(),
            self.letter_entry.get()
        )

        # Use the result to show a feedback message
        if result == "Successful":
            self.show_feedback_message("Job application submitted successfully!", success=True)
        else:
            self.show_feedback_message("Failed to submit the job application. Please try again.", success=False)

        # Clear form and return to menu
        self.clear_all_frames()
        self.show_feedback_message("Application successfully added!", success=True)
        self.show_menu()

    def show_add_response(self):
        """Show the add response form."""
        self.clear_all_frames()

        # Initialize response_frame if not already initialized
        if not hasattr(self, 'response_frame'):
            self.response_frame = ctk.CTkFrame(self.root)  # Replace `self.root` with the parent frame

        # Back Button
        if not hasattr(self, 'back_button_response'):
            self.back_button_response = ctk.CTkButton(self.response_frame, text="Back", command=self.show_menu)
            self.back_button_response.grid(row=0, column=0, padx=10, pady=10)  # Use grid instead of pack

        # Labels and Entries
        if not hasattr(self, 'application_id_entry'):
            ctk.CTkLabel(self.response_frame, text="Job Application ID:").grid(row=1, column=0, padx=10, pady=5)
            self.application_id_entry = ctk.CTkEntry(self.response_frame)
            self.application_id_entry.grid(row=1, column=1, padx=10, pady=5)

            ctk.CTkLabel(self.response_frame, text="Response:").grid(row=2, column=0, padx=10, pady=5)
            self.response_entry = ctk.CTkEntry(self.response_frame)
            self.response_entry.grid(row=2, column=1, padx=10, pady=5)

            ctk.CTkLabel(self.response_frame, text="Note:").grid(row=3, column=0, padx=10, pady=5)  # Added note label
            self.note_entry = ctk.CTkEntry(self.response_frame)  # Added note entry
            self.note_entry.grid(row=3, column=1, padx=10, pady=5)  # Use grid for consistency

            # Submit Button
            self.submit_button_response = ctk.CTkButton(self.response_frame, text="Submit Response",
                                                        command=self.submit_response)
            self.submit_button_response.grid(row=4, columnspan=2, pady=20)  # Center the button

        # Show the response frame
        self.response_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def submit_response(self):
        """Submit the response for the selected job application."""
        application_id = self.application_id_entry.get()
        response = self.response_entry.get()
        note = self.note_entry.get()  # Get the note from the entry field

        if application_id and response:
            self.db.update_application_response_and_note(application_id, application_response=response,
                                                         note=note)  # Pass both response and note
            print(f"Response and note for application ID {application_id} added.")
            self.clear_all_frames()
            self.show_menu()

            # Show success feedback message
            self.show_feedback_message("Response and note added successfully!", success=True)
        else:
            print("Please provide both application ID and response.")
            self.show_feedback_message("Please provide both application ID and response.", success=False)

    def submit_delete_application(self):
        """Submit the delete for a job application."""
        job_id = self.job_id_entry.get()

        if job_id:
            self.db.delete_job_application(job_id)
            print(f"Application with ID {job_id} deleted.")
            self.clear_all_frames()
            self.show_menu()

            # Show success feedback message
            self.show_feedback_message(f"Application {job_id} deleted successfully!", success=True)
        else:
            self.show_feedback_message("Please provide a valid job ID to delete.", success=False)

    def show_all_applications(self):
        """Show all job applications."""
        self.clear_all_frames()

        # Back Button
        if not hasattr(self, 'back_button_show'):
            self.back_button_show = ctk.CTkButton(self.show_frame, text="Back", command=self.show_menu)
            self.back_button_show.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        applications = self.db.get_all_job_applications()

        if not applications:
            applications = [{"id": "N/A", "job_provider": "N/A", "job_description": "N/A", "job_link": "N/A",
                             "resume_used": "N/A", "personal_letter_used": "N/A", "application_response": "N/A",
                             "note": "N/A"}]

        # Headers
        headers = ["ID", "Provider", "Description", "Link", "Response", "Note"]

        # Create a canvas for scrolling
        canvas = ctk.CTkCanvas(self.show_frame)
        canvas.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Create vertical and horizontal scrollbars
        v_scrollbar = ctk.CTkScrollbar(self.show_frame, orientation="vertical", command=canvas.yview)
        v_scrollbar.grid(row=1, column=1, sticky="ns", padx=10, pady=10)

        h_scrollbar = ctk.CTkScrollbar(self.show_frame, orientation="horizontal", command=canvas.xview)
        h_scrollbar.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        # Configure the canvas to use the scrollbars
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Create a frame inside the canvas to hold the content
        content_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Create headers in the first row, from column 1 to 6
        for col, header in enumerate(headers, start=1):
            ctk.CTkLabel(content_frame, text=header, font=("Arial", 12, "bold")).grid(row=1, column=col, padx=10,
                                                                                      pady=5, sticky="w")

        # Application details
        for row, app in enumerate(applications, start=2):  # Start from row 2 to leave space for headers
            ctk.CTkLabel(content_frame, text=app['id']).grid(row=row, column=1, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(content_frame, text=app['job_provider']).grid(row=row, column=2, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(content_frame, text=app['job_description']).grid(row=row, column=3, padx=10, pady=5,
                                                                          sticky="w")
            ctk.CTkLabel(content_frame, text=app['job_link']).grid(row=row, column=4, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(content_frame, text=app['application_response']).grid(row=row, column=5, padx=10, pady=5,
                                                                               sticky="w")
            ctk.CTkLabel(content_frame, text=app['note']).grid(row=row, column=6, padx=10, pady=5, sticky="w")

        # Update the canvas scroll region to fit the content
        content_frame.update_idletasks()  # Ensure content size is calculated
        canvas.config(scrollregion=canvas.bbox("all"))

        # Show the show frame
        self.show_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def show_update_application(self):
        """Show the update application form."""
        self.clear_all_frames()

        # Back Button
        if not hasattr(self, 'back_button_update'):
            self.back_button_update = ctk.CTkButton(self.update_frame, text="Back", command=self.show_menu)
            self.back_button_update.pack(side="left", padx=10, pady=10)

        # Labels and Entries
        if not hasattr(self, 'job_id_entry'):
            ctk.CTkLabel(self.update_frame, text="Job ID:").pack(pady=5)
            self.job_id_entry = ctk.CTkEntry(self.update_frame)
            self.job_id_entry.pack(pady=5)

            ctk.CTkLabel(self.update_frame, text="New Job Provider:").pack(pady=5)
            self.job_provider_entry = ctk.CTkEntry(self.update_frame)
            self.job_provider_entry.pack(pady=5)

            ctk.CTkLabel(self.update_frame, text="New Job Description:").pack(pady=5)
            self.job_description_entry = ctk.CTkEntry(self.update_frame)
            self.job_description_entry.pack(pady=5)

            ctk.CTkLabel(self.update_frame, text="New Job Link:").pack(pady=5)
            self.job_link_entry = ctk.CTkEntry(self.update_frame)
            self.job_link_entry.pack(pady=5)

            ctk.CTkLabel(self.update_frame, text="New Resume Used:").pack(pady=5)
            self.resume_used_entry = ctk.CTkEntry(self.update_frame)
            self.resume_used_entry.pack(pady=5)

            ctk.CTkLabel(self.update_frame, text="New Personal Letter Used:").pack(pady=5)
            self.personal_letter_used_entry = ctk.CTkEntry(self.update_frame)
            self.personal_letter_used_entry.pack(pady=5)

            # Submit Button
            self.submit_button_update = ctk.CTkButton(self.update_frame, text="Submit", command=self.submit_job_update)
            self.submit_button_update.pack(pady=20)

        # Show the update frame
        self.update_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def submit_job_update(self):
        """Submit the update for an existing job application."""
        job_id = self.job_id_entry.get()
        new_provider = self.job_provider_entry.get()
        new_description = self.job_description_entry.get()
        new_link = self.job_link_entry.get()
        new_resume_used = self.resume_used_entry.get()
        new_letter_used = self.personal_letter_used_entry.get()

        if job_id:
            self.db.update_job_application(job_id, new_provider, new_description, new_link, new_resume_used,
                                           new_letter_used)
            print(f"Application with ID {job_id} updated.")
            self.clear_all_frames()
            self.show_menu()

            # Show success feedback message
            self.show_feedback_message(f"Application {job_id} updated successfully!", success=True)

    def show_delete_application(self):
        """Show the delete application form."""
        self.clear_all_frames()

        # Initialize delete_frame if not already initialized
        if not hasattr(self, 'delete_frame'):
            self.delete_frame = ctk.CTkFrame(self.root)  # Replace `self.root` with the parent frame

        # Back Button
        if not hasattr(self, 'back_button_delete'):
            self.back_button_delete = ctk.CTkButton(self.delete_frame, text="Back", command=self.show_menu)
            self.back_button_delete.grid(row=0, column=0, padx=10, pady=10)  # Use grid for consistency

        # Job Application ID Entry
        if not hasattr(self, 'job_id_entry'):
            ctk.CTkLabel(self.delete_frame, text="Enter Job Application ID to delete:").grid(row=1, column=0, padx=10,
                                                                                             pady=5)
            self.job_id_entry = ctk.CTkEntry(self.delete_frame)
            self.job_id_entry.grid(row=1, column=1, padx=10, pady=5)

            # Fetch and display job details when user enters an ID
            self.job_id_entry.bind("<KeyRelease>", self.fetch_job_details)

        # Job Details Display
        if not hasattr(self, 'job_details_label'):
            self.job_details_label = ctk.CTkLabel(self.delete_frame,
                                                  text="Job Provider and Description will appear here.")
            self.job_details_label.grid(row=2, columnspan=2, padx=10, pady=5)

        # Delete Button
        self.delete_button = ctk.CTkButton(self.delete_frame, text="Delete Application", command=self.confirm_delete)
        self.delete_button.grid(row=3, columnspan=2, pady=20)

        # Show the delete frame
        self.delete_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def fetch_job_details(self, event=None):
        """Fetch and display job provider and description based on the entered job ID."""
        job_id = self.job_id_entry.get()

        if job_id:
            job_details = self.db.get_job_application_details(job_id)  # Assuming this method exists

            if job_details:
                if len(job_details) >= 2:  # Ensure there are at least 2 values (provider, description)
                    provider, description = job_details[0], job_details[1]
                    self.job_details_label.configure(
                        text=f"Provider: {provider}\nDescription: {description}")  # Use 'configure' instead of 'config'
                else:
                    self.job_details_label.configure(text="Invalid job details.")  # Use 'configure' here as well
            else:
                self.job_details_label.configure(text="No job found with the given ID.")  # Use 'configure'
        else:
            self.job_details_label.configure(text="Job Provider and Description will appear here.")  # Use 'configure'

    def confirm_delete(self):
        """Ask user for confirmation to delete a job application."""
        job_id = self.job_id_entry.get()

        if job_id:
            # Fetch job details from the database
            job_details = self.db.get_job_application_details(job_id)  # Assuming this method exists

            if job_details:
                # Unpack the job details safely
                provider = job_details[0] if len(job_details) > 0 else "Unknown Provider"
                description = job_details[1] if len(job_details) > 1 else "Unknown Description"

                # Create confirmation popup using self as the parent window
                self.confirmation_popup = ctk.CTkToplevel(self)
                self.confirmation_popup.title("Confirm Deletion")
                self.confirmation_popup.geometry("300x250")  # Set a suitable geometry for the popup

                # Ensure the popup stays on top of the main window
                self.confirmation_popup.attributes("-topmost", True)

                # Add warning message to the popup
                message = f"You are about to delete the application with ID {job_id}."
                confirmation_label = ctk.CTkLabel(self.confirmation_popup, text=message, justify="left")
                confirmation_label.pack(pady=10)  # Add padding for space between messages

                # Add an empty label for spacing
                spacer = ctk.CTkLabel(self.confirmation_popup, text="")
                spacer.pack(pady=5)

                # Display provider and description
                message2 = f"Provider: {provider}\nDescription: {description}"
                confirmation_details_label = ctk.CTkLabel(self.confirmation_popup, text=message2, justify="left")
                confirmation_details_label.pack(pady=10)

                # Create Delete and Cancel buttons
                delete_button = ctk.CTkButton(self.confirmation_popup, text="Delete",
                                              command=lambda: self.delete_job(job_id))
                delete_button.pack(side="left", padx=10, pady=10)

                cancel_button = ctk.CTkButton(self.confirmation_popup, text="Cancel",
                                              command=self.confirmation_popup.destroy)
                cancel_button.pack(side="right", padx=10, pady=10)

            else:
                # If no job found with the given ID
                self.job_details_label.configure(text="No job found with the given ID.")
        else:
            # If no ID is provided
            self.job_details_label.configure(text="Please enter a valid Job ID to delete.")

    def delete_job(self, job_id):
        """Perform the actual job deletion."""
        # Call the database method to delete the job application
        self.db.delete_job_application(job_id)

        # Close the confirmation popup after deleting
        self.confirmation_popup.destroy()

        # Provide feedback and return to the menu
        self.show_feedback_message(f"Job application with ID {job_id} deleted successfully.", success=True)
        self.clear_all_frames()
        self.show_menu()

    def clear_all_frames(self):
        """Clear all frames."""
        for frame in [self.menu_frame, self.add_frame, self.show_frame, self.update_frame, self.response_frame, self.delete_frame]:
            frame.grid_forget()

    def exit_program(self):
        """Exit the program."""
        self.quit()

# Run the UI application
if __name__ == "__main__":
    app = JobApplicationTrackerUI()
    app.mainloop()
