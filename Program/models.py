# models.py
class JobApplication:
    def __init__(self, job_provider, job_description, job_link, resume_used, personal_letter_used):
        self.job_provider = job_provider
        self.job_description = job_description
        self.job_link = job_link
        self.resume_used = resume_used
        self.personal_letter_used = personal_letter_used

    def __repr__(self):
        return f"JobApplication(job_provider={self.job_provider}, job_description={self.job_description}, job_link={self.job_link})"
