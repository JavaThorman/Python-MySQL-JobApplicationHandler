import mysql.connector
from mysql.connector import Error
from Database import config


class Database:
    def __init__(self):
        try:
            # Connect to MySQL server (without specifying a database)
            self.connection = mysql.connector.connect(
                host=config.DB_HOST,
                user=config.DB_USER,
                password=config.DB_PASSWORD
            )
            if self.connection.is_connected():
                print("\nConnection to MySQL server successful.\n")

            # Check if the database exists, if not, create it
            cursor = self.connection.cursor()
            cursor.execute("SHOW DATABASES LIKE 'job_tracker_db';")
            result = cursor.fetchone()

            if not result:
                # Database does not exist, so create it
                cursor.execute("CREATE DATABASE job_tracker_db;")
                print("\nDatabase 'job_tracker_db' created successfully.\n")

            # Now connect to the job_tracker_db
            self.connection.database = 'job_tracker_db'

            # Check the connection to the specified database
            if self.connection.is_connected():
                print("\nConnected to the 'job_tracker_db' database.\n")

        except Error as e:
            print(f"Error: {e}")
            self.connection = None

    def create_table(self):
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS job_applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            job_provider VARCHAR(255) NOT NULL,
            job_description VARCHAR(255) NOT NULL,
            job_link VARCHAR(255),
            resume_used_for_application VARCHAR(255) NOT NULL,
            personal_letter_used_for_application VARCHAR(255) NOT NULL,
            application_response VARCHAR(255),
            note TEXT,
            application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()

    def get_job_application_details(self, job_id):
        cursor = self.connection.cursor()
        query = "SELECT job_provider, job_description FROM job_applications WHERE id = %s;"
        cursor.execute(query, (job_id,))
        result = cursor.fetchone()

        if result:
            # Ensure the result is a tuple with 2 elements (job_provider, job_description)
            return result  # (job_provider, job_description)
        else:
            return None  # No job found with the given ID

    def insert_job_application(self, job_provider, job_description, job_link, resume_used, personal_letter_used):
        try:
            # Create a cursor object to interact with the database
            cursor = self.connection.cursor()

            # SQL query to insert the job application into the database
            insert_query = """
            INSERT INTO job_applications (job_provider, job_description, job_link, resume_used_for_application, personal_letter_used_for_application)
            VALUES (%s, %s, %s, %s, %s);
            """

            # Execute the query with the provided parameters
            cursor.execute(insert_query, (job_provider, job_description, job_link, resume_used, personal_letter_used))

            # Commit the transaction to save the changes to the database
            self.connection.commit()

            # Check if the insert was successful by verifying rowcount
            if cursor.rowcount > 0:
                return "Successful"
            else:
                return "Not Successful"
        except Exception as e:
            # If an error occurs, print the error and return failure
            print(f"Error inserting job application: {e}")
            return "Not Successful"
        finally:
            # Close the cursor to release the database resources
            cursor.close()

    def update_job_application(self, job_id, job_provider=None, job_description=None, job_link=None, resume_used=None,
                               personal_letter_used=None):
        cursor = self.connection.cursor()
        update_query = "UPDATE job_applications SET "
        update_values = []

        if job_provider is not None:
            update_query += "job_provider = %s, "
            update_values.append(job_provider)

        if job_description is not None:
            update_query += "job_description = %s, "
            update_values.append(job_description)

        if job_link is not None:
            update_query += "job_link = %s, "
            update_values.append(job_link)

        if resume_used is not None:
            update_query += "resume_used_for_application = %s, "
            update_values.append(resume_used)

        if personal_letter_used is not None:
            update_query += "personal_letter_used_for_application = %s, "
            update_values.append(personal_letter_used)

        update_query = update_query.rstrip(', ')
        update_query += " WHERE id = %s;"

        update_values.append(job_id)

        cursor.execute(update_query, tuple(update_values))
        self.connection.commit()


    def update_application_response_and_note(self, job_id, application_response=None, note=None):
        cursor = self.connection.cursor()

        update_query = "UPDATE job_applications SET "
        update_values = []

        if application_response is not None:
            update_query += "application_response = %s, "
            update_values.append(application_response)

        if note is not None:
            update_query += "note = %s, "
            update_values.append(note)

        update_query = update_query.rstrip(', ')
        update_query += " WHERE id = %s;"

        update_values.append(job_id)

        cursor.execute(update_query, tuple(update_values))
        self.connection.commit()


    def delete_job_application(self, job_id):
        cursor = self.connection.cursor()
        delete_query = "DELETE FROM job_applications WHERE id = %s;"
        cursor.execute(delete_query, (job_id,))
        self.connection.commit()


    def get_job_application_by_id(self, job_id):
        cursor = self.connection.cursor()
        query = "SELECT * FROM job_applications WHERE id = %s;"
        cursor.execute(query, (job_id,))
        result = cursor.fetchone()
        return result

    def get_all_job_applications(self):
        cursor = self.connection.cursor()
        select_query = "SELECT * FROM job_applications;"
        cursor.execute(select_query)
        result = cursor.fetchall()

        applications = []
        if result:
            for row in result:
                application_details = {
                    "id": row[0],
                    "job_provider": row[1],
                    "job_description": row[2],
                    "job_link": row[3],
                    "resume_used": row[4],
                    "personal_letter_used": row[5],
                    "application_response": row[6],
                    "note": row[7],
                }
                applications.append(application_details)
        return applications

    def check_job_application_exists(self, job_id):
        cursor = self.connection.cursor()
        select_query = "SELECT COUNT(*) FROM job_applications WHERE id = %s;"
        cursor.execute(select_query, (job_id,))
        result = cursor.fetchone()
        return result[0] > 0

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Connection closed.\n")
