import pickle
from dt import current_date

class ApplicationsMaster:
    def __init__(self):

        self.active_applications = []

        self.submitted_applications = []

        self.archived_applications = []
    
    def date_sort_appls(self):
        self.active_applications = sorted(self.active_applications, key=lambda appl: appl.deadline)
    
    def return_appls(self):
        self.date_sort_appls()
        return [x.job_title for x in self.active_applications]
    
    def add_application(self, application):
        self.active_applications.append(application)
        
    
    def update_appl(self, index, appl_obj):
        #target = 
        pass
    

class Application:
    def __init__(self, job_title, company, deadline, job_type, job_subtype=None):
        self.job_title = job_title
        self.company = company
        self.deadline = deadline
        self.cat = job_type
        self.subcat = job_subtype



    
applications = None
if not applications:
    applications = ApplicationsMaster()