

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
                             QTextEdit, QListWidgetItem,
                             QListView)
from PyQt6.QtCore import (QDate, QDateTime, QAbstractListModel, Qt, QModelIndex)
from PyQt6.QtGui import (QColor, QBrush, QImage)
from applications import Application, ApplicationsMaster, applications, save_appls
from dt import current_date


class ApplModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.appl_master = applications

    def data(self, index, role):
        target = self.appl_master.active_applications[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return target.return_list_str()

        if role == Qt.ItemDataRole.ForegroundRole:
            item = target.return_list_edits()
            if item[0] == True:
                return (QColor("gray"))
            if item[1] == True:
                return (QColor("light green")) 


    def rowCount(self, index=QModelIndex()):
        return len(self.appl_master.active_applications)

    def add(self, appl):
        self.appl_master.add_application(appl)
        self.appl_master.date_sort_appls()
        self.layoutChanged.emit()

    def update(self, appl_index, new_appl):
        self.appl_master.update_appl(appl_index, new_appl)


    
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
        self.job_url = QLineEdit(parent=self)
        
        #self.submitted = QCheckBox(parent=self)
        
        self.job_cat = QComboBox(parent=self)
        self.job_cat.setEditable(True)

        self.job_subcat = QComboBox(parent=self)
        self.job_subcat.setEditable(True)

        

        entry_form.addRow("Job Title:", self.job_title)
        entry_form.addRow("Company:", self.job_company)
        entry_form.addRow("Deadline", self.job_deadline)
        entry_form.addRow("Category (optional):", self.job_cat)
        entry_form.addRow("Subcategory (optional):", self.job_subcat)
        entry_form.addRow("URL:", self.job_url)

        
        entry_layout.addLayout(entry_form)


                #entry buttons
        self.staged_chk = QCheckBox("Staged?", parent=self)
        self.staged_chk.stateChanged.connect(self.set_staged)
        entry_layout.addWidget(self.staged_chk)
        
        self.save_entry = QPushButton("Save", parent=self)
        self.save_entry.clicked.connect(self.save_appl)
        entry_layout.addWidget(self.save_entry)
        
        self.clear_entry = QPushButton("Clear", parent=self)
        self.clear_entry.clicked.connect(self.clear_entry_form)
        entry_layout.addWidget(self.clear_entry)

        self.save_all =  QPushButton("Save all to mem", parent=self)
        #self.save_all.clicked.connect(save_appls)
        entry_layout.addWidget(self.save_all)
        
        
        applications_layout.addLayout(entry_layout)


        #view list
        
        self.appl_list_layout = QVBoxLayout()
        #self.populate_applications_list()
        self.model = ApplModel()
        self.application_list = QListView()
        self.application_list.setModel(self.model)
        self.selectionModel = self.application_list.selectionModel()        

       
        self.selectionModel.currentChanged.connect(self.select_appl)


        
        self.clear_entry_btn = QPushButton("Temp. Deselect Button")
        self.clear_entry_btn.clicked.connect(self.deselct_list_and_reset)

        self.appl_list_layout.addWidget(self.application_list)
        self.appl_list_layout.addWidget(self.clear_entry_btn)
        applications_layout.addLayout(self.appl_list_layout)

        #applications_layout.addWidget(self.application_list)


        self.descr_layout = QVBoxLayout()
        self.description_field = QTextEdit(parent=self)
        self.descr_layout.addWidget(self.description_field)

        self.save_descr_btn = QPushButton("Save Description", parent=self)
        self.save_descr_btn.clicked.connect(self.save_job_descr)
        self.descr_layout.addWidget(self.save_descr_btn)

        applications_layout.addLayout(self.descr_layout)



        self.cover_layout = QVBoxLayout()
        self.cover_writer = QTextEdit()
        self.cover_layout.addWidget(self.cover_writer)

        self.save_cover_btn = QPushButton("Save Cover", parent=self)
        self.save_cover_btn.clicked.connect(self.save_cover)
        self.cover_layout.addWidget(self.save_cover_btn)


        applications_layout.addLayout(self.cover_layout)

       
        #THESE TWO HAD TO MOVE AS THEY HAD INTERACTIONS WITH CLEARING!
        #self.application_list.itemSelectionChanged.connect(self.select_appl)
        #self.application_list.setCurrentRow(0)

        
    
    
    def save_appl(self):

        err = False
        if not self.job_title.text():
            self.job_title.setPlaceholderText("Required")
            err = True
        else:
            title = self.job_title.text().title()
        if not self.job_company.text():
            self.job_company.setPlaceholderText("Required")
            err = True
        else:
            company = self.job_company.text().title()
        deadline = self.job_deadline.date().toPyDate() 

        cat = self.job_cat.currentText().title()
        subcat = self.job_subcat.currentText().title()
        url = self.job_url.text()


        if not err:
            #print(title, company, cat, subcat, url)    
            new_job = Application(title, company, deadline, cat, subcat, url)

            if not self.selectionModel.currentIndex().isValid():
                self.model.add(new_job)
            else:
                applications.update_appl(self.selectionModel.currentIndex(), new_job)
            
            #self.populate_applications_list()
            
    
    def deselct_list_and_reset(self):
        self.application_list.clearFocus()
        self.application_list.clearSelection()
        self.save_entry.setText("Add Application")
        self.clear_entry.setText("Clear Input")
        
        self.clear_entry_form()
        self.description_field.clear()
        self.cover_writer.clear()


    def select_appl(self):
        '''
        
            
            self.save_entry.setText("Add Application")
            self.clear_entry.setText("Clear Input")

            self.clear_entry_form()
            self.description_field.clear()
            self.cover_writer.clear()
        else:
        '''
         

    
        self.save_entry.setText("Update Application")
        self.clear_entry.setText("Delete Application")
        selected_index = self.selectionModel.currentIndex()
        row = selected_index.row()
        selected = applications.active_applications[row]
        
        self.job_title.setText(selected.job_title)
        self.job_company.setText(selected.company)
        self.job_deadline.setDate(QDate(selected.deadline.year, selected.deadline.month, selected.deadline.day))
        self.job_cat.setCurrentText(selected.cat)
        self.job_subcat.setCurrentText(selected.subcat)

        if selected.staged:
            self.staged_chk.setChecked(True)
        else:
            self.staged_chk.setChecked(False)
        
        self.job_url.setText(selected.url)

        if selected.cover:
            self.cover_writer.setText(selected.cover.raw_text)
        else:
            self.cover_writer.clear()
        if selected.job_description:
            if hasattr(selected.job_description, "markdown"):
                self.description_field.setMarkdown(selected.job_description.markdown)
            else:
                self.description_field.setText(selected.job_description.raw_text)
        else:
            self.description_field.clear()

        
    
    def clear_entry_form(self):
        '''
        if self.application_list.currentRow() != 0:
            applications.delete_appl(self.application_list.currentRow()-1)
            self.application_list.setCurrentRow(0)
            self.populate_applications_list()
            print(applications.active_applications)
        '''
        self.job_title.clear()
        self.job_company.clear()
        self.job_deadline.setDate(QDate(current_date.year, current_date.month, current_date.day))
        self.job_cat.clearEditText()
        self.job_subcat.clearEditText()
        self.job_url.clear()
        
    
    def populate_applications_list(self):
        if applications.cats:
            self.job_cat.addItems(applications.cats)
        if applications.subcats:
            self.job_subcat.addItems(applications.subcats)
        self.clear_entry_form()


    def save_cover(self):
    
        selected_index = self.selectionModel.currentIndex()
        row = selected_index.row()
        selected = applications.active_applications[row]
        if not selected.cover:
            selected.create_cover()    
        selected.cover.text = self.cover_writer.toPlainText()
        
    def save_job_descr(self):
        selected_index = self.selectionModel.currentIndex()
        row = selected_index.row()
        selected = applications.active_applications[row]
        if not selected.job_description:
            selected.add_job_descr()    
        selected.job_description.raw_text = self.description_field.toPlainText()
        selected.job_description.markdown = self.description_field.toMarkdown()

    def set_staged(self):
        selected_index = self.selectionModel.currentIndex()
        row = selected_index.row()
        selected = applications.active_applications[row]
        if self.staged_chk.isChecked():
            selected.staged = True
            #self.application_list.currentItem().setBackground(QColor("light green"))
        else:
            selected.staged = False
            #self.application_list.currentItem().setBackground(QColor("white"))
        


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

    def populate_active_appls(self):
        pass




def launch_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    window.show()
    app.exec()