
class WriteUp:
    def __init__(self):
        self.raw_text = ''
        self.sections = []
        #remember there's a markdown attr now, added in gui constructor, so amend this when possible
    
    def add_section(self, section):
        self.sections.append(section)


class Section:
    def __init__(self, text, tags):
        self.text = text
        self.tags = tags




class Cover(WriteUp):
    def __init__(self):
        super().__init__()
    
class JobDescription(WriteUp):
    def __init__(self):
        super().__init__()
