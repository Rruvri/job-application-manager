



class Application:
    def __init__(self, job_title, company, due_date, job_type, job_subtype=None):
        self.job_title = job_title
        self.company = company
        self.due_date = due_date
        self.category = job_type
        self.subcategory = job_subtype
    
