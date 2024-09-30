#writing productivity tracker streamlined into a class with dictionary of sessions
#next features: pull word count from file

import datetime, csv, os

def str_time(time):
        #Returns datetime object as a string
        return time.strftime("%m/%d/%Y, %H:%M:%S")

def chop_ms(delta):
    #Returns timedelta object without microseconds
    return delta - datetime.timedelta(microseconds=delta.microseconds)

class WritingSessionTracker:
    def __init__(self):
        #instantiates a session as a list within a list
        #self.sessions = [] #needs to pull existing list from file
        self.session = {}
        self.file = "new_file.csv"
        self.project_path = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Bel e Kyre.scrivx"
        #self.metadata_path = os.path.join(self.project_path, "Settings", "ui.plist")
    
    def start_session(self):
        if os.path.exists(self.file):
            pass
        else:
            with open(self.file, "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Start Time", "End Time", "Total Time"])

        response = input("Type anything to start.")
        if response == "":
            print("No input was given.")
        else:
            start_time = datetime.datetime.now()
            str_start_time = str_time(start_time)
            print("Start Time: ", str_start_time)
            self.session["start"] = start_time

        additional_response = input("Type anything when you're finished with this writing session.")
        if response == "":
            print("No input was given.")
        else:
            self.end_session()
            self.calculation()
            self.write_to_file()

    def end_session(self):
        end_time = datetime.datetime.now()
        self.session["end"] = end_time
        
    def calculation(self):
        self.session["total_time"] = chop_ms(self.session["end"] - self.session["start"])
        print(self.session)

    def write_to_file(self):
        with open(self.file, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([str_time(self.session["start"]), str_time(self.session["end"]), str(self.session["total_time"])])

tracker = WritingSessionTracker()
tracker.start_session()