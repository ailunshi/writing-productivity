#writing productivity tracker streamlined into a class with dictionary of sessions
#next features: pull word count from file

import datetime, csv, os, time
from scrivx_parser import ScrivxParser

def str_time(time):
        #Returns datetime object as a string
        return time.strftime("%m/%d/%Y, %H:%M:%S")

def chop_ms(delta):
    #Returns timedelta object without microseconds
    return delta - datetime.timedelta(microseconds=delta.microseconds)

class WritingSessionTracker:
    def __init__(self):
        self.session = {}
        self.file = "Writing Tracker.csv"
        self.data = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Files/Data"
        self.project_path = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Bel e Kyre.scrivx"

    def start_session(self):
        # Starts the session, instantiates a parser, runs parser

        parser = ScrivxParser(self.data, self.project_path)
        parser.parse_scrivx_file()

        if os.path.exists(self.file):
            pass
        else:
            with open(self.file, "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Start Time", "End Time", "Total Time", "Start Count", "End Count", "Words"])

        response = input("Type anything to start.")
        if response == "":
            print("No input was given.")
        else:
            start_time = datetime.datetime.now()
            str_start_time = str_time(start_time)
            print("Start Time: ", str_start_time)
            self.session["start"] = start_time

            counter_start = time.perf_counter()

            self.session["start_count"] = parser.run()

            counter_end = time.perf_counter()
            print(f"Word count run time took {counter_end - counter_start} seconds.")

        additional_response = input("Type anything when you're finished with this writing session.")

        if additional_response == "":
            print("No input was given.")
        else:
            self.end_session(parser)
            self.write_to_file()

    def end_session(self, parser):
        # Ends session and calculates the data
        self.session["end"] = datetime.datetime.now()
        self.session["end_count"] = parser.run()
        self.session["words"] = self.session["end_count"] - self.session["start_count"]
        self.session["total_time"] = chop_ms(self.session["end"] - self.session["start"])
        print(self.session)

    def write_to_file(self):
        # Writes all the pertinent data into a CSV file
        with open(self.file, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([str_time(self.session["start"]), str_time(self.session["end"]), str(self.session["total_time"]), self.session["start_count"], self.session["end_count"], self.session["words"]])

if __name__== "__main__":
    tracker = WritingSessionTracker()
    tracker.start_session()
