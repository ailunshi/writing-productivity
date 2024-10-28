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

def unserialize_datetime(date_string):
    try:
        return datetime.datetime.fromisoformat(date_string)
    except ValueError:
        raise TypeError("Date string not in ISO format")

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
        self.session_dates = []

        for session in self.all_sessions:
            start_timestamp = unserialize_datetime(session["start_timestamp"])
            start_date = start_timestamp.strftime("%m/%d/%Y")
            self.session_dates.append(start_date)
        print(self.session_dates)

    def start_session(self):
        # Starts the session, initiates a ScrivxParser object, runs parser

        parser = ScrivxParser(self.data, self.project_path)
        parser.parse_scrivx_file()

        if os.path.exists(self.tracker):
            pass
        else:
            with open(self.tracker, "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Date", "Day", "Start Time", "End Time", "Elapsed Time", "Start Count", "End Count", "Words"])

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
            self.write_to_data_file()
            self.save_session()

    def end_session(self, parser):
        # Ends session and calculates the data

        end_timestamp = datetime.datetime.now()
        self.session["end_timestamp"] = end_timestamp
        self.session["end_time"] = end_timestamp.strftime("%H:%M:%S")
        self.session["end_count"] = parser.run()
        self.session["words"] = self.session["end_count"] - self.session["start_count"]
        self.session["elapsed_time_str"] = str(chop_ms(self.session["end_timestamp"] - self.session["start_timestamp"]))
        self.session["elapsed_time_sec"] = int(chop_ms(self.session["end_timestamp"] - self.session["start_timestamp"]).total_seconds())

    def write_to_raw_file(self):
        # Writes all the pertinent data into a CSV file

        with open(self.tracker, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.session["date"], self.session["day"], self.session["start_time"], self.session["end_time"], self.session["elapsed_time_str"], 
                             self.session["start_count"], self.session["end_count"], self.session["words"]])

    def write_to_data_file(self):
        # Compiles more useful data based on information from the CSV file

        data = {}

        # Initialize data for the session date if it doesn't exist
        session_date = self.session["date"]
        if session_date not in self.session_dates:
            data[session_date] = {
                "average_rate": self.session["words"] / (self.session["elapsed_time_sec"] / 3600) if self.session["elapsed_time_sec"] > 0 else 0,
                "total_words": self.session["words"],
                "total_time": self.session["elapsed_time_sec"] / 3600,
                "total_sessions": 1,
                "average_words_per_session": self.session["words"],
                "average_time_per_session": self.session["elapsed_time_sec"]
            }
        else:
            # Update data for the current session date
            data[session_date]["average_rate"] = (data[session_date]["total_words"] + self.session["words"]) / (data[session_date]["total_time"] + self.session["elapsed_time_sec"] / 3600)
            data[session_date]["total_words"] += self.session["words"]
            data[session_date]["total_time"] += self.session["elapsed_time_sec"] / 3600
            data[session_date]["total_sessions"] += 1
            data[session_date]["average_words_per_session"] = data[session_date]["total_words"] / data[session_date]["total_sessions"]
            data[session_date]["average_time_per_session"] = data[session_date]["total_time"] / data[session_date]["total_sessions"]

        # Write the calculated data to data.csv
        with open(self.tracker_data, "w", newline='') as datafile:
            writer = csv.writer(datafile)
            writer.writerow(["Date", "Average Rate", "Total Words", "Total Time (sec)", "Total Sessions", 
                             "Average Words Per Session", "Average Time Per Session (sec)"])
            
            for date, stats in data.items():
                writer.writerow([
                    date,
                    stats["average_rate"],
                    stats["total_words"],
                    stats["total_time"],
                    stats["total_sessions"],
                    stats["average_words_per_session"],
                    stats["average_time_per_session"]
                ])
  
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
