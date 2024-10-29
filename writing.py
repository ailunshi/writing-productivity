from writing_streamlined import WritingSessionTracker

class Writing:
    def __init__(self, project):
        self.project = project
        self.project_file = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Bel e Kyre.scrivx"
        self.data = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Files/Data"
        self.memory = "sessions.json"
        self.data_json = "data.json"
        self.writing_tracker = "writingtracker.csv"
        self.data_tracker = "data.csv"

    def call_writing_streamlined(self):
        new_session = WritingSessionTracker(self.project_file, self.data, self.memory, self.data_json, self.writing_tracker, self.data_tracker)
        new_session.start_session()

if __name__ == "__main__":
    project = "Bel e Kyre"
    writing_instance = Writing(project)
    writing_instance.call_writing_streamlined()