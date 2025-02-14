from writing_streamlined import WritingSessionTracker
import os

class Writing:
    def __init__(self, project):
        self.project = project
        self.project_file = "/Users/balloon/short stories/stories.scriv/stories.scrivx"
        # "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Bel e Kyre.scrivx"
        self.data = "/Users/balloon/short stories/stories.scriv/Files/Data"
        # "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Files/Data"
        self.memory = "sessions_stories.json"
        # "sessions.json"
        self.data_json = "data_stories.json"
        # "data.json"
        self.writing_tracker = "writingtracker_stories.csv"
        # "writingtracker.csv"
        self.data_tracker = "data_stories.csv"
        # "data.csv"
        self.session_file = "session_stories.txt"
            
    def call_writing_streamlined(self):
        new_session = WritingSessionTracker(self.project_file, self.data, self.memory, self.data_json, self.writing_tracker, self.data_tracker, self.session_file)
        new_session.start_session()

if __name__ == "__main__":
    project = "Short Stories"
    writing_instance = Writing(project)
    writing_instance.call_writing_streamlined()