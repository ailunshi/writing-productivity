#writing productivity tracker streamlined into a class with dictionary of sessions
#next thing to do: don't add start/end/total time if it already exists

import datetime, csv

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
    
    def start_session(self):
        file_path = "new_file.csv" #eventually: need to check if file and titles already exist
        with open("new_file.csv", "a", newline='') as csvfile:
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
        with open("new_file.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([str_time(self.session["start"]), str_time(self.session["end"]), str(self.session["total_time"])])

tracker = WritingSessionTracker()
tracker.start_session()