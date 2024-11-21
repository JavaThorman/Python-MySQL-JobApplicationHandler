import mysql.connector
from mysql.connector import Error
from Database import config


class Database:
    def __init__(self):
        try:
            # Establish connection to the MySQL database
            self.connection = mysql.connector.connect(
                host=config.DB_HOST,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME
            )
            if self.connection.is_connected():
                print("\nConnection successful.\n")
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

    def insert_job_application(self, job_provider, job_description, job_link, resume_used, personal_letter_used):
        cursor = self.connection.cursor()
        insert_query = """
        INSERT INTO job_applications (job_provider, job_description, job_link, resume_used_for_application, personal_letter_used_for_application)
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (job_provider, job_description, job_link, resume_used, personal_letter_used))
        self.connection.commit()
        print("Job application added successfully.\n")

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
        print(f"Job application with ID {job_id} updated successfully.\n")

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
        print(f"Job application with ID {job_id} updated with response and note.\n")

    def delete_job_application(self, job_id):
        cursor = self.connection.cursor()
        delete_query = "DELETE FROM job_applications WHERE id = %s;"
        cursor.execute(delete_query, (job_id,))
        self.connection.commit()
        print(f"Job application with ID {job_id} deleted successfully.\n")

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

        if result:
            print("Job Applications:\n")
            for row in result:
                application_details = (
                    f"ID: {row[0]}, Provider: {row[1]}, Description: {row[2]}, "
                    f"Link: {row[3]}, Resume: {row[4]}, Letter: {row[5]}"
                )

                if row[6] is not None:
                    application_details += f"\nResponse: {row[6]}"

                if row[7] is not None:
                    application_details += f", Note: {row[7]}"

                print(application_details)
        else:
            print("No job applications found.\n")

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
