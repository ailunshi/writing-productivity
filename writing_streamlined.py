"""
To Do:
• Need to abstract this away. Set up new file that asks for project path and data path
 and creates a new WritingSessionTracker object with those paths.
• Add data.csv functionality and make sure info can be pulled from .json (especially datetime info)
    • ie. do i need to convert datetime info back from iso if i want to calculate things with it?
"""

import datetime, csv, os, time, json
from scrivx_parser import ScrivxParser

def str_time(time):
    # Returns datetime object as a string
    return time.strftime("%m/%d/%Y, %H:%M:%S")

def chop_ms(delta):
    # Returns timedelta object without microseconds
    return delta - datetime.timedelta(microseconds=delta.microseconds)

def serialize_datetime(obj): 
    if isinstance(obj, datetime.datetime): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 

class WritingSessionTracker:
    def __init__(self, filename="sessions.json"):
        # Sets up a WritingSessionTracker object with sessions dictionary, tracker file, and data file
        
        self.jsonfile = filename
        self.all_sessions = self.load_session()
        self.session = {}
        self.tracker = "writingtracker.csv"
        self.tracker_data = "data.csv"
        self.data = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Files/Data"
        self.project_path = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Bel e Kyre.scrivx"

    def start_session(self):
        # Starts the session, initiates a ScrivxParser object, runs parser

        parser = ScrivxParser(self.data, self.project_path)
        parser.parse_scrivx_file()

        if os.path.exists(self.tracker):
            pass
        else:
            with open(self.tracker, "a", newline='') as csvfile:
            #open(self.tracker, "a", newline='') as datafile:
                writer1 = csv.writer(csvfile)
                #writer2 = csv.writer(datafile)
                writer1.writerow(["Date", "Day", "Start Time", "End Time", "Elapsed Time", "Start Count", "End Count", "Words"])
                #writer2.writerow(["Average Rate", "Total Words", "Total Time", "Total Sessions", "Average Words Per Session", "Average Time Per Session"])

        response = input("Type anything to start.")
        if response == "":
            print("No input was given.")
        else:
            start_timestamp = datetime.datetime.now()
            self.session["start_timestamp"] = start_timestamp
            self.session["date"] = start_timestamp.strftime("%m/%d/%Y")
            self.session["day"] = start_timestamp.strftime("%A")
            self.session["start_time"] = start_timestamp.strftime("%H:%M:%S")

            counter_start = time.perf_counter()

            self.session["start_count"] = parser.run()

            counter_end = time.perf_counter()
            print(f"Word count run time took {counter_end - counter_start} seconds.")

        additional_response = input("Type anything when you're finished with this writing session.")

        if additional_response == "":
            print("No input was given.")
        else:
            self.end_session(parser)
            self.write_to_raw_file()
            #self.write_to_data_file()
            self.save_session()

    def end_session(self, parser):
        # Ends session and calculates the data
        end_timestamp = datetime.datetime.now()
        self.session["end_timestamp"] = end_timestamp
        self.session["end_time"] = end_timestamp.strftime("%H:%M:%S")
        self.session["end_count"] = parser.run()
        self.session["words"] = self.session["end_count"] - self.session["start_count"]
        self.session["elapsed_time"] = str(chop_ms(self.session["end_timestamp"] - self.session["start_timestamp"]))

    def write_to_raw_file(self):
        # Writes all the pertinent data into a CSV file
        with open(self.tracker, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.session["date"], self.session["day"], self.session["start_time"], self.session["end_time"], self.session["elapsed_time"], 
                             self.session["start_count"], self.session["end_count"], self.session["words"]])

    def write_to_data_file(self):
        # Compiles more useful data based on information from the CSV file

        # "Average Rate", "Total Words", "Total Time", "Total Sessions", "Average Words Per Session", "Average Time Per Session"

        # you have a list of all sessions (as dictionaries)
        # for dict in list
        # set up a dictionary with key as date, and value as dictionary of all other information
        data = {}

        for item in self.all_sessions: #item is a dictionary
            if item["date"] in data.keys():
                average_rate = (data[item]["total_words"] + item["words"] * 60) / (data[item]["elapsed_time"] + item["elapsed_time"])
                data[item] = [{"average_rate": average_rate, "total_words": data[item]["total_words"] + item["words"], "total_time": data[item]["elapsed_time"] + item["elapsed_time"],
                               "total_sessions": data[item]["total_sessions"] + 1, "average_words_per_session": (data[item]["total_words"] + item["words"]) / (data[item]["total_sessions"] + 1),
                               "average_time_per_session": (data[item]["elapsed_time"] + item["elapsed_time"]) / (data[item]["total_sessions"] + 1)}]
            else:
                data[item] = [{"average_rate": item["words"] * 60 / item["elapsed_time"], "total_words": item["words"], "total_time": item["elapsed_time"], 
                               "total_sessions": 1, "average_words_per_session": item["words"], "average_time_per_session": item["elapsed_time"]}]

        with open(self.tracker, "a") as datafile:
            writer = csv.writer(datafile)
            writer.writerow([])

    def load_session(self):
        # Loads all sessions for this project from a JSON file

        if os.path.exists(self.jsonfile):
            with open(self.jsonfile, 'r') as f:
                return json.load(f)
        else:
            return []

    def save_session(self):
        # Saves current writing session to a JSON file

        self.all_sessions.append(self.session)
        with open("sessions.json", "w") as file:
            json.dump(self.all_sessions, file, default=serialize_datetime)

        print(file.name)

if __name__== "__main__":
    tracker = WritingSessionTracker()
    tracker.start_session()
