
'''
        #application entry page __________________________________________
        applications_page = QWidget(self)
        applications_layout = QHBoxLayout()
        applications_page.setLayout(applications_layout)
            
            #entry form
        
        entry_layout = QVBoxLayout()
        entry_form = QFormLayout()

        job_cat = QComboBox(parent=applications_page)
        job_cat.setEditable(True)

        job_subcat = QComboBox(parent=applications_page)
        job_subcat.setEditable(True)

        entry_form.addRow("Job Title:", QLineEdit(parent=applications_page))
        entry_form.addRow("Company:", QLineEdit(parent=applications_page))
        entry_form.addRow("Deadline", QDateEdit(parent=applications_page))
        entry_form.addRow("Category:", job_cat)
        entry_form.addRow("Subcategory (optional):", job_subcat)
        
        entry_layout.addLayout(entry_form)


            #entry buttons
        save_entry = QPushButton("Save", parent=applications_page)
        entry_layout.addWidget(save_entry)
        
        clear_entry = QPushButton("Clear", parent=applications_page)
        entry_layout.addWidget(clear_entry)


        applications_layout.addLayout(entry_layout)


            #view list
        application_list = QListWidget(parent=applications_page)
        applications_layout.addWidget(application_list)






                #cover letter page __________________________________________
        write_up_page = QWidget(self)
        write_up_layout = QHBoxLayout()
        write_up_page.setLayout(write_up_layout)

            #select application
        write_up_list = QListWidget(parent=write_up_page)
        
        write_up_layout.addWidget(write_up_list)

            #cover letter write-up
        cover_entry = QTextEdit(parent=write_up_page)
        write_up_layout.addWidget(cover_entry)

        '''

import sys
from PyQt6.QtWidgets import (QApplication, QLabel,
                             QWidget, QGridLayout,
                             QFormLayout, QLineEdit,
                             QDialog, QHBoxLayout,
                             QDialogButtonBox, QMainWindow,
                             QStackedLayout, QComboBox,
                             QCalendarWidget, QDateEdit,
                             QDateTimeEdit, QCheckBox,
                             QVBoxLayout, QListWidget, 
                             QPushButton, QTabWidget,
                             QTextEdit)
from PyQt6.QtCore import (QDate, QDateTime)
from applications import Application, ApplicationsMaster, applications

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ravi's Application Hub")
        
        main_page = QWidget(self)
        main_layout = QGridLayout()
        main_page.setLayout(main_layout)
        
        
        #tab widget __________________________________________
        tabs = QTabWidget(self)

        
        appls = Appl()
        covers = Covers()
        tabs.addTab(appls, "Applications")
        tabs.addTab(covers, 'Write-ups')
        

        #add widget and finish set-up
        main_layout.addWidget(tabs)

        self.setCentralWidget(main_page)
    
    

class Appl(QWidget):
    def __init__(self):
        super().__init__()
        
        applications_layout = QHBoxLayout()
        self.setLayout(applications_layout)
            
            #entry form
        entry_layout = QVBoxLayout()
        entry_form = QFormLayout()

        self.job_title = QLineEdit(parent=self)
        self.job_company = QLineEdit(parent=self)
        self.job_deadline = QDateEdit(parent=self)
        
        self.job_cat = QComboBox(parent=self)
        self.job_cat.setEditable(True)

        self.job_subcat = QComboBox(parent=self)
        self.job_subcat.setEditable(True)

        entry_form.addRow("Job Title:", self.job_title)
        entry_form.addRow("Company:", self.job_company)
        entry_form.addRow("Deadline", self.job_deadline)
        entry_form.addRow("Category:", self.job_cat)
        entry_form.addRow("Subcategory (optional):", self.job_subcat)
        
        entry_layout.addLayout(entry_form)


                #entry buttons
        save_entry = QPushButton("Save", parent=self)
        save_entry.clicked.connect(self.save_appl)
        entry_layout.addWidget(save_entry)
        
        clear_entry = QPushButton("Clear", parent=self)
        clear_entry.clicked.connect(self.clear_entry_form)
        entry_layout.addWidget(clear_entry)


        applications_layout.addLayout(entry_layout)


            #view list
        self.application_list = QListWidget(parent=self)
        self.application_list.itemSelectionChanged.connect(self.select_appl)
        self.populate_applications_list()
        #populate list here
        

        applications_layout.addWidget(self.application_list)


        
    
    
    def save_appl(self):
        title = self.job_title.text().title()
        company = self.job_company.text().title()
        deadline = self.job_deadline.date().toPyDate 
        cat = self.job_cat.currentText().title()
        subcat = self.job_subcat.currentText().title()

        new_job = Application(title, company, deadline, cat, subcat)
        
        
        applications.add_application(new_job)
        #self.application_list.addItems(applications.add_application(new_job))

        #self.clear_entry_form()
        self.populate_applications_list()
    
    def select_appl(self):
        
        if self.application_list.currentItem().text() == "<Select for new entry>":
            self.clear_entry_form()
        else:
            selected = applications.active_applications[(self.application_list.currentRow()-1)]
            
            self.job_title.setText(selected.job_title)
            self.job_company.setText(selected.company)
            self.job_deadline.setDate(QDate(selected.deadline.year, selected.deadline.month, selected.deadline.day))
            self.job_cat.setCurrentText(selected.cat)
            
            self.job_subcat.setCurrentText(selected.subcat)
    
    def clear_entry_form(self):
        self.job_title.clear()
        self.job_company.clear()
        #self.job_deadline
        self.job_cat.clearEditText()
        self.job_subcat.clearEditText()
    
    def populate_applications_list(self):
        self.application_list.clear()
        self.application_list.addItem("<Select for new entry>")
        self.application_list.addItems(applications.return_appls())
        self.clear_entry_form()


    

        



class Covers(QWidget):
    def __init__(self):
        super().__init__()
        
        covers_layout = QHBoxLayout()
        self.setLayout(covers_layout)

        self.setLayout(covers_layout)

            #select application
        write_up_list = QListWidget(parent=self)
        
        covers_layout.addWidget(write_up_list)

            #cover letter write-up
        cover_entry = QTextEdit(parent=self)
        covers_layout.addWidget(cover_entry)

def launch_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    window.show()
    app.exec()