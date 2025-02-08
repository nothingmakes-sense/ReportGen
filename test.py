import datetime
import threading
from AIResponses import AIResponse
from SaveDocx import pDocx
from gui_helpers import popup_gen, popup_err
import tkinter as tk
from tkinter import *
from tkinter import ttk

# Initialize tkinter variables
clientName = StringVar()
clientID = StringVar()
serviceProvided = StringVar()
serviceProvidedBy = StringVar()
SupportPlan = StringVar()

def genAndSave(clientName, clientID, currentDate, response, serviceProvided, serviceProvidedBy, SupportPlan, StartDate, EndDate, StartTime, EndTime, update_progress):
    hourFormat = "%I:%M %p"
    dateFormat = "%m/%d/%Y"
    difference = (EndDate - StartDate).days

    i = 0
    while i <= difference:
        response = AIResponse(clientName.get(), SupportPlan.get())
        pDocx(clientName.get(), clientID.get(), currentDate, response, serviceProvided.get(), serviceProvidedBy.get(), StartTime.strftime(hourFormat), EndTime.strftime(hourFormat), (EndTime - StartTime).total_seconds() / 3600)
        update_progress(i)
        currentDate += datetime.timedelta(days=1)
        i += 1
    popup_gen('Complete!')

def update_progress(value, progress_bar, panel, generate_button):
    progress_bar['value'] = value
    panel.update_idletasks()
    if value == progress_bar['maximum']:
        generate_button['state'] = NORMAL

def runGeneration(clientName, clientID, currentDate, response, serviceProvided, serviceProvidedBy, SupportPlan, StartDate, EndDate, StartTime, EndTime, update_progress, panel, generate_button):
    generate_button['state'] = DISABLED
    def wrapper():
        genAndSave(clientName, clientID, currentDate, response, serviceProvided, serviceProvidedBy, SupportPlan, StartDate, EndDate, StartTime, EndTime, update_progress)
    thread = threading.Thread(target=wrapper)
    thread.start()

def command(startDate, endDate, startTime, endTime, progress_bar, panel, clientName, clientID, currentDate, response, serviceProvided, serviceProvidedBy, SupportPlan, generate_button):
    try:
        hourFormat = "%I:%M %p"
        dateFormat = "%m/%d/%Y"
        StartDate = datetime.datetime.strptime(startDate.get(), dateFormat)
        EndDate = datetime.datetime.strptime(endDate.get(), dateFormat)
        StartTime = datetime.datetime.strptime(startTime.get(), hourFormat)
        EndTime = datetime.datetime.strptime(endTime.get(), hourFormat)
        difference = (EndDate - StartDate).days
        progress_bar = ttk.Progressbar(panel, maximum=difference)
        progress_bar.grid(column=3, row=14, columnspan=2, pady=10)
        runGeneration(clientName, clientID, currentDate, response, serviceProvided, serviceProvidedBy, SupportPlan, StartDate, EndDate, StartTime, EndTime, update_progress, panel, generate_button)
    except Exception as e:
        popup_err(e)

# GUI setup
root = tk.Tk()
root.title("Report Generator")

# Main panel
panel1 = ttk.Frame(root, padding="20 20 20 20")
panel1.grid(column=0, row=0, sticky=(N, W, E, S))

# Client info
ttk.Label(panel1, text="Client Name").grid(column=0, row=0, sticky=W)
clientName_entry = ttk.Entry(panel1, width=25, textvariable=clientName)
clientName_entry.grid(column=1, row=0, sticky=(W, E))

ttk.Label(panel1, text="Client ID").grid(column=0, row=1, sticky=W)
clientID_entry = ttk.Entry(panel1, width=25, textvariable=clientID)
clientID_entry.grid(column=1, row=1, sticky=(W, E))

ttk.Label(panel1, text="Service Provided").grid(column=0, row=2, sticky=W)
serviceProvided_entry = ttk.Entry(panel1, width=25, textvariable=serviceProvided)
serviceProvided_entry.grid(column=1, row=2, sticky=(W, E))

ttk.Label(panel1, text="Service Provided By").grid(column=0, row=3, sticky=W)
serviceProvidedBy_entry = ttk.Entry(panel1, width=25, textvariable=serviceProvidedBy)
serviceProvidedBy_entry.grid(column=1, row=3, sticky=(W, E))

ttk.Label(panel1, text="Support Plan").grid(column=0, row=4, sticky=W)
SupportPlan_entry = ttk.Entry(panel1, width=25, textvariable=SupportPlan)
SupportPlan_entry.grid(column=1, row=4, sticky=(W, E))

# Date and time inputs
ttk.Label(panel1, text="Start Date (month/day/year)").grid(column=0, row=5, sticky=W)
startDate = StringVar()
startDate_entry = ttk.Entry(panel1, width=25, textvariable=startDate)
startDate_entry.grid(column=1, row=5, sticky=(W, E))

ttk.Label(panel1, text="End Date (month/day/year)").grid(column=0, row=6, sticky=W)
endDate = StringVar()
endDate_entry = ttk.Entry(panel1, width=25, textvariable=endDate)
endDate_entry.grid(column=1, row=6, sticky=(W, E))

ttk.Label(panel1, text="Start Time (hh:mm AM/PM)").grid(column=0, row=7, sticky=W)
startTime = StringVar()
startTime_entry = ttk.Entry(panel1, width=25, textvariable=startTime)
startTime_entry.grid(column=1, row=7, sticky=(W, E))

ttk.Label(panel1, text="End Time (hh:mm AM/PM)").grid(column=0, row=8, sticky=W)
endTime = StringVar()
endTime_entry = ttk.Entry(panel1, width=25, textvariable=endTime)
endTime_entry.grid(column=1, row=8, sticky=(W, E))

# Generate button
generate_button = ttk.Button(panel1, text="Generate AI Reports", command=lambda: command(startDate, endDate, startTime, endTime, None, panel1, clientName, clientID, datetime.datetime.now(), "response", serviceProvided, serviceProvidedBy, SupportPlan, generate_button))
generate_button.grid(column=0, row=9, columnspan=2, pady=10)

# Second panel for managing clients
panel2 = ttk.Frame(root, padding="20 20 20 20")
panel2.grid(column=1, row=0, sticky=(N, W, E, S))

def update_client_list():
    client_listbox.delete(0, END)
    for patient in patients_data:
        client_listbox.insert(END, patient['name'])

def on_client_select(event):
    selected_index = client_listbox.curselection()
    if selected_index:
        selected_patient = patients_data[selected_index[0]]
        clientName.set(selected_patient['name'])
        clientID.set(selected_patient['id'])
        serviceProvided.set(selected_patient['service'])
        serviceProvidedBy.set(selected_patient.get('provider', ''))
        SupportPlan.set(selected_patient['support_plan'])

client_listbox = Listbox(panel2, height=15, font=('Arial', 14))
client_listbox.grid(column=0, row=0, rowspan=8, sticky=(N, S, E, W))
client_listbox.bind("<<ListboxSelect>>", on_client_select)

# Add a frame for editing client details
edit_frame = ttk.Frame(panel2, padding="10 10 10 10")
edit_frame.grid(column=1, row=0, rowspan=8, sticky=(N, S, E, W))

ttk.Label(edit_frame, text="Client Name").grid(column=0, row=0, sticky=W)
clientName_entry_edit = ttk.Entry(edit_frame, width=25, textvariable=clientName)
clientName_entry_edit.grid(column=1, row=0, sticky=(W, E))

ttk.Label(edit_frame, text="Client ID").grid(column=0, row=1, sticky=W)
clientID_entry_edit = ttk.Entry(edit_frame, width=25, textvariable=clientID)
clientID_entry_edit.grid(column=1, row=1, sticky=(W, E))

ttk.Label(edit_frame, text="Service Provided").grid(column=0, row=2, sticky=W)
serviceProvided_entry_edit = ttk.Entry(edit_frame, width=25, textvariable=serviceProvided)
serviceProvided_entry_edit.grid(column=1, row=2, sticky=(W, E))

ttk.Label(edit_frame, text="Service Provided By").grid(column=0, row=3, sticky=W)
serviceProvidedBy_entry_edit = ttk.Entry(edit_frame, width=25, textvariable=serviceProvidedBy)
serviceProvidedBy_entry_edit.grid(column=1, row=3, sticky=(W, E))

ttk.Label(edit_frame, text="Support Plan").grid(column=0, row=4, sticky=W)
SupportPlan_entry_edit = ttk.Entry(edit_frame, width=25, textvariable=SupportPlan)
SupportPlan_entry_edit.grid(column=1, row=4, sticky=(W, E))

root.mainloop()