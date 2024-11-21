from Database.database import Database
from models import JobApplication

def start_program():
    # Create a new instance of the Database class to interact with the database
    db = Database()

    # Create the job applications table if it does not already exist
    db.create_table()

    # Main program loop to keep the program running until the user decides to exit
    while True:
        # Display the main menu options
        print("\nJob Application Tracker")
        print("1. Add a job application")
        print("2. Show all sent applications")
        print("3. Update a job application")
        print("4. Add response to job application")
        print("5. Delete a job application")
        print("6. Exit")

        # Get the user's choice
        choice = input("Enter your choice: ")
        print("\n")

        if choice == '1':
            # Collect job application details from the user
            job_provider = input("Enter job provider: ")
            job_description = input("Enter job description: ")
            job_link = input("Enter job link: ")
            resume_used = input("Which resume did you use? (Enter text or leave blank if not applicable): ")
            personal_letter_used = input("Did you include a personal letter? (Enter text or leave blank if not applicable): ")

            # Create a new JobApplication instance with the provided details
            job_application = JobApplication(job_provider, job_description, job_link, resume_used, personal_letter_used)

            # Insert the new job application into the database
            db.insert_job_application(
                job_application.job_provider,
                job_application.job_description,
                job_application.job_link,
                job_application.resume_used,
                job_application.personal_letter_used
            )

        elif choice == '2':
            # Retrieve and display all sent job applications
            db.get_all_job_applications()

        elif choice == '3':
            # Prompt the user to enter the job application ID they want to update
            job_id = input("Enter the job application ID to update (or type 'exit' to go back): ")
            if job_id.lower() == 'exit':
                continue  # Return to the main menu if 'exit' is typed

            # Check if the specified job application exists
            if not db.check_job_application_exists(job_id):
                print(f"Job application with ID {job_id} does not exist. Returning to the main menu.")
                continue  # Return to the main menu if the job application doesn't exist

            # Allow the user to update the application fields, leaving them blank to keep current values
            print("Leave fields blank to keep current values.")
            job_provider = input("Enter new job provider (leave blank to keep current): ")
            job_description = input("Enter new job description (leave blank to keep current): ")
            job_link = input("Enter new job link (leave blank to keep current): ")
            resume_used = input("Enter new resume used (leave blank to keep current): ")
            personal_letter_used = input("Enter new personal letter used (leave blank to keep current): ")

            # Update the job application in the database with the new values
            db.update_job_application(
                job_id,
                job_provider if job_provider else None,
                job_description if job_description else None,
                job_link if job_link else None,
                resume_used if resume_used else None,
                personal_letter_used if personal_letter_used else None,
            )

        elif choice == '4':
            # Allow the user to add a response and notes to a job application
            job_id = input("Enter the job application ID to update response and note (or type 'exit' to go back): ")
            if job_id.lower() == 'exit':
                continue  # Return to the main menu if 'exit' is typed

            # Check if the specified job application exists
            if not db.check_job_application_exists(job_id):
                print(f"Job application with ID {job_id} does not exist. Returning to the main menu.")
                continue  # Return to the main menu if the job application doesn't exist

            # Prompt the user to enter the application response and additional notes
            application_response = input("Enter application response (e.g., denied, pending, accepted, interview): ")
            note = input("Enter any additional notes (e.g., interview details or feedback): ")

            # Update the response and notes in the job application database
            db.update_application_response_and_note(
                job_id,
                application_response,
                note
            )

        elif choice == '5':
            # Allow the user to delete a job application
            job_id = input("Enter the job application ID to delete (or type 'exit' to go back): ")
            if job_id.lower() == 'exit':
                continue  # Return to the main menu if 'exit' is typed

            # Check if the specified job application exists
            if not db.check_job_application_exists(job_id):
                print(f"Job application with ID {job_id} does not exist. Returning to the main menu.")
                continue  # Return to the main menu if the job application doesn't exist

            # Display the details of the job application the user is about to delete
            job_application = db.get_job_application_by_id(job_id)
            print("\nApplication details:")
            print(f"ID: {job_application[0]}")
            print(f"Job Provider: {job_application[1]}")
            print(f"Job Description: {job_application[2]}")
            print(f"Job Link: {job_application[3]}")
            print(f"Resume Used: {job_application[4]}")
            print(f"Personal Letter Used: {job_application[5]}")
            print(f"Application Response: {job_application[6]}")
            print(f"Note: {job_application[7]}")

            # Confirm with the user if they are sure they want to delete the application
            confirm = input("\nAre you sure you want to delete this application? (yes/no): ")
            if confirm.lower() == 'yes':
                db.delete_job_application(job_id)  # Delete the job application from the database
                print(f"Job application with ID {job_id} has been deleted.")
            else:
                print("Job application deletion cancelled.")

        elif choice == '6':
            # Exit the program
            print("Exiting the program.")
            break  # Exit the loop and end the program

        else:
            # Handle invalid input from the user
            print("Invalid choice. Please try again.")

    # Close the database connection when the program ends
    db.close()
