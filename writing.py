from writing_streamlined import WritingSessionTracker
import os

class Writing:
    def __init__(self, project):
        self.project = project
        self.project_file = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Bel e Kyre.scrivx"
        # "/Users/balloon/short stories/stories.scriv/stories.scrivx"
        # 
        self.data = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Files/Data"
        # "/Users/balloon/short stories/stories.scriv/Files/Data"
        self.memory = "sessions.json"
        # "sessions_stories.json"
        self.data_json = "data.json"
        # "data_stories.json"
        self.writing_tracker = "writingtracker.csv"
        # "writingtracker_stories.csv"
        self.data_tracker = "data.csv"
        # "data_stories.csv"
        self.session_file = "session_number.txt"
        # "session_stories.txt"
            
    def call_writing_streamlined(self):
        new_session = WritingSessionTracker(self.project_file, self.data, self.memory, self.data_json, self.writing_tracker, self.data_tracker, self.session_file)
        new_session.start_session()

if __name__ == "__main__":
    project = "Bel e Kyre"
    writing_instance = Writing(project)
    writing_instance.call_writing_streamlined()