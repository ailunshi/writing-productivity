#building a writing productivity tracker

import datetime
import csv


def str_time(time):
    #Returns datetime object as a string
    return time.strftime("%m/%d/%Y, %H:%M:%S")

def chop_ms(delta):
    #Returns timedelta object without microseconds
    return delta - datetime.timedelta(microseconds=delta.microseconds)

file_path = "new_file.csv"
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

response = input("Type anything once finished with your writing session.")
if response == "":
    print("No input was given.")
else:
    end_time = datetime.datetime.now()
    str_end_time = str_time(end_time)
    print("End Time: ", str_end_time)
    total_time = chop_ms(end_time - start_time) #total_time is timedelta object
    print("Total Time: ", str(total_time))

    with open("new_file.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([str_start_time, str_end_time, str(total_time)])


"""
steps:
pull empty .txt file to reference
use fake word counts for now?
fill in calculations

eventually:
reference meta data from scrivener
    not sure if it's possible to see if i've edited the page

reference from google doc
"""