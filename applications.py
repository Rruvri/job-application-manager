
from dt import current_date, return_date_str
from saves import load_data, store_data
from write_up_analysis import Cover, JobDescription






class ApplicationsMaster:
    def __init__(self):

        self.active_applications = []

        self.submitted_applications = []

        self.archived_applications = []

        #self.staging_indexes = []

        self.staged_applications = []
        
        self.titles = []
        
        self.cats = []

        self.subcats = []
    
    def date_sort_appls(self):
        self.active_applications = sorted(self.active_applications, key=lambda appl: appl.deadline)

    
    def return_appls_str(self):

        self.date_sort_appls()
        return [(f"{x.job_title} | {x.company}", True if x.deadline < current_date else False, True if x.staged else False) for x in self.active_applications]

   

    '''
    def check_staged(self):
        
        indexes = []
        for a in self.active_applications:
            if a.staged:
                indexes.append(self.active_applications.index(a))
        print(indexes)
        self.staging_indexes = indexes
    '''


    
    def return_staged_appls_str(self):
        self.date_sort_appls()
        
        if self.staged_applications:
                return [f"{x.job_title} | {x.company} | {return_date_str(x.deadline)}" for x in self.staged_applications]
        
     
    
    def add_application(self, application):
        self.active_applications.append(application)
        self.process_update_checks(application.return_checks())
        
    
    def process_update_checks(self, checks):
        if checks[0] and checks[0] not in self.titles:
            self.titles.append(checks[0])
        if checks[1] and checks[1] not in self.cats:
            self.cats.append(checks[1])
        if checks[2] and checks[2] not in self.subcats:
            self.subcats.append(checks[2])

        
    
    def update_appl(self, index, appl_obj):
        target = self.active_applications[index]
        
        target.job_title = appl_obj.job_title
        target.company = appl_obj.company
        target.deadline = appl_obj.deadline
        target.cat = appl_obj.cat
        target.subcat = appl_obj.subcat
        target.url = appl_obj.url

        self.process_update_checks(target.return_checks())
    
    def delete_appl(self, index):
        self.active_applications.pop(index)
    
    def reinit_appl_classes(self):
        new = []
        for appl in self.active_applications:
            new_a = Application(appl.job_title, appl.company, appl.deadline, appl.cat, appl.subcat, appl.url, appl.cover, appl.job_description)
            new.append(new_a)
        self.active_applications = new
        


    
    

class Application:
    def __init__(self, job_title, company, deadline, job_type=None, job_subtype=None, url=None, cover=None, job_description = None, submitted=False, staged=False):
        self.job_title = job_title
        self.company = company
        self.deadline = deadline
        self.cat = job_type
        self.subcat = job_subtype
        
        self.url = url
        #self.submitted = submitted ->finish implementing
        self.cover = cover
        self.job_description = job_description
        self.submitted = submitted
        self.staged = staged
        
    
    def return_checks(self):
        return (self.job_title, self.cat, self.subcat)
    
    def create_cover(self):
        self.cover = Cover()
    
    def add_job_descr(self):
        self.job_description = JobDescription()

    def stage_application(self):
        self.staged = True

    def return_list_str(self):
        return f"{self.job_title} | {self.company} | {return_date_str(self.deadline)}"

    def return_list_edits(self):
        return (True if self.deadline < current_date else False, True if self.staged else False)

    



applications = load_data('appls')
#applications.reinit_appl_classes()  # uncomment when you've fucked with the classes
if applications == None:
    applications = ApplicationsMaster()
applications.reinit_appl_classes()


def save_appls():
    store_data(applications, 'appls')
    #print(applications.active_applications)

