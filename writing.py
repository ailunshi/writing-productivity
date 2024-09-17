#building a writing productivity tracker
"""
import tkinter as tk
app = tk.Tk()
app.title('Writing Productivity Tracker')
button = tk.Button(app, text='Start', width=25, command=app.destroy)
button.pack()

app.mainloop()
"""

import datetime

def str_time(time):
    #Returns datetime object as a string
    return time.strftime("%m/%d/%Y, %H:%M:%S")

def chop_ms(delta):
    #Returns timedelta object without microseconds
    return delta - datetime.timedelta(microseconds=delta.microseconds)

file_path = "new_file.txt"

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
    #total_time = chop_ms(total_time)
    print("Total Time: ", str(total_time))

    with open(file_path, 'a') as file:
        file.write(f" {str_start_time}, {str_end_time}, {str(total_time)}")
        file.write("\n")



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