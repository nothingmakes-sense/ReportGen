import tkinter as tk
from tkinter import *
from tkinter import ttk
import datetime
from tkcalendar import DateEntry
from SaveDocx import pDocx
from AIResponses import AIResponse
import threading
import json
from gui_helpers import *
from client_management import *
from report_generator import *

# Global variables
patients_data = []
providers_data = []

root = Tk()
root.title("KAP Software | AI Powered Patient Report Generator ")
root.geometry("1080x720")
root.configure(bg='#f0f0f0')

style = ttk.Style()
style.configure('TFrame', background='#f0f0f0')
style.configure('TLabel', background='#f0f0f0', font=('Arial', 14))
style.configure('TEntry', font=('Arial', 14))
style.configure('TButton', font=('Arial', 14), padding=6)
style.configure('TCombobox', font=('Arial', 14))

notebook = ttk.Notebook(root)
notebook.grid(column=0, row=0, sticky=(N, W, E, S))

# First Panel
panel1 = ttk.Frame(notebook, padding="20 20 20 20")
panel1.grid(column=0, row=0, sticky=(N, W, E, S))
notebook.add(panel1, text='Report Generator')

descriptionCol = 2
textBoxCol = 3
textboxWidth = 30

# company name
companyName = StringVar()
companyName_entry = ttk.Entry(panel1, width=textboxWidth, textvariable=companyName)
companyName_entry.grid(column=textBoxCol, row=1, sticky=(W, E))
ttk.Label(panel1, text="Company Name").grid(column=descriptionCol, row=1, sticky=W)

clientName = StringVar()
clientName_combo = ttk.Combobox(panel1, width=textboxWidth, textvariable=clientName)
clientName_combo.grid(column=textBoxCol, row=2, sticky=(W, E))
clientName_combo.bind("<<ComboboxSelected>>", lambda event: on_client_name_selected(event, clientName, clientID, clientDOB, serviceProvided, SupportPlan, serviceProvidedBy, patients_data))
ttk.Label(panel1, text="Client Name").grid(column=descriptionCol, row=2, sticky=W)

clientID = StringVar()
clientID_entry = ttk.Entry(panel1, width=textboxWidth, textvariable=clientID)
clientID_entry.grid(column=textBoxCol, row=3, sticky=(W, E))
ttk.Label(panel1, text="Client ID").grid(column=descriptionCol, row=3, sticky=W)

clientDOB = StringVar()
clientDOB_entry = ttk.Entry(panel1, width=textboxWidth, textvariable=clientDOB)
clientDOB_entry.grid(column=textBoxCol, row=4, sticky=(W, E))
ttk.Label(panel1, text="Client DOB").grid(column=descriptionCol, row=4, sticky=W)

serviceProvided = StringVar()
serviceProvided_entry = ttk.Entry(panel1, width=textboxWidth, textvariable=serviceProvided)
serviceProvided_entry.grid(column=textBoxCol, row=5, sticky=(W, E))
ttk.Label(panel1, text="Service Provided").grid(column=descriptionCol, row=5, sticky=W)

serviceProvidedBy = StringVar()
serviceProvidedBy_combo = ttk.Combobox(panel1, width=textboxWidth, textvariable=serviceProvidedBy)
serviceProvidedBy_combo.grid(column=textBoxCol, row=6, sticky=(W, E))
ttk.Label(panel1, text="Service Provided By").grid(column=descriptionCol, row=6, sticky=W)

SupportPlan = StringVar()
SupportPlan_entry = ttk.Entry(panel1, width=textboxWidth, textvariable=SupportPlan)
SupportPlan_entry.grid(column=textBoxCol, row=7, sticky=(W, E))
ttk.Label(panel1, text="Support Plan").grid(column=descriptionCol, row=7, sticky=W)

# Generate time intervals
time_options = [datetime.time(hour=h, minute=m).strftime("%I:%M %p") for h in range(24) for m in (0, 15, 30, 45)]

startTime = StringVar()
startTime_combo = ttk.Combobox(panel1, width=textboxWidth, textvariable=startTime, values=time_options)
startTime_combo.grid(column=textBoxCol, row=8, sticky=(W, E))
ttk.Label(panel1, text="Start Time").grid(column=descriptionCol, row=8, sticky=W)

endTime = StringVar()
endTime_combo = ttk.Combobox(panel1, width=textboxWidth, textvariable=endTime, values=time_options)
endTime_combo.grid(column=textBoxCol, row=9, sticky=(W, E))
ttk.Label(panel1, text="End Time").grid(column=descriptionCol, row=9, sticky=W)

startDate = StringVar()
startDate_entry = DateEntry(panel1, width=textboxWidth-2, textvariable=startDate, date_pattern='mm/dd/yyyy')
startDate_entry.grid(column=textBoxCol, row=10, sticky=(W, E))
ttk.Label(panel1, text="Start Date (month/day/year)").grid(column=descriptionCol, row=10, sticky=W)

endDate = StringVar()
endDate_entry = DateEntry(panel1, width=textboxWidth-2, textvariable=endDate, date_pattern='mm/dd/yyyy')
endDate_entry.grid(column=textBoxCol, row=11, sticky=(W, E))
ttk.Label(panel1, text="End Date (month/day/year)").grid(column=descriptionCol, row=11, sticky=W)

button_state = NORMAL

progress_var = tk.IntVar()
generate_button = ttk.Button(panel1, text="Generate AI Reports", command=lambda: command(startDate, endDate, startTime, endTime, progress_bar, panel1, clientName, clientID, currentDate, response, serviceProvided, serviceProvidedBy, SupportPlan, generate_button), state=button_state)
generate_button.grid(column=descriptionCol, row=13, columnspan=2, pady=10)

# Load company name button
load_button = ttk.Button(panel1, text="Load Company Name", command=lambda: load_company_name(companyName))
load_button.grid(column=descriptionCol, row=15, columnspan=2, pady=10)

# Save client data button
save_client_button = ttk.Button(panel1, text="Save Client", command=lambda: save_client_data(clientName, clientID, clientDOB, serviceProvided, SupportPlan, serviceProvidedBy, clientName_combo, update_client_list))
save_client_button.grid(column=descriptionCol, row=16, columnspan=2, pady=10)

# Save provider data button
save_provider_button = ttk.Button(panel1, text="Save Provider", command=lambda: save_provider_data(serviceProvidedBy, serviceProvidedBy_combo))
save_provider_button.grid(column=descriptionCol, row=17, columnspan=2, pady=10)

# Second Panel for managing clients
panel2 = ttk.Frame(notebook, padding="20 20 20 20")
panel2.grid(column=0, row=0, sticky=(N, W, E, S))
notebook.add(panel2, text='Manage Clients')

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
        clientDOB.set(selected_patient['dob'])
        serviceProvided.set(selected_patient['service'])
        SupportPlan.set(selected_patient['support_plan'])
        serviceProvidedBy.set(selected_patient.get('provider', ''))

client_listbox = Listbox(panel2, height=15, font=('Arial', 14))
client_listbox.grid(column=0, row=0, rowspan=8, sticky=(N, S, E, W))
client_listbox.bind("<<ListboxSelect>>", on_client_select)

# Add a frame for editing client details
edit_frame = ttk.Frame(panel2, padding="10 10 10 10")
edit_frame.grid(column=1, row=0, rowspan=8, sticky=(N, S, E, W))

ttk.Label(edit_frame, text="Client Name").grid(column=0, row=0, sticky=W)
clientName_entry_edit = ttk.Entry(edit_frame, width=textboxWidth, textvariable=clientName)
clientName_entry_edit.grid(column=1, row=0, sticky=(W, E))

ttk.Label(edit_frame, text="Client ID").grid(column=0, row=1, sticky=W)
clientID_entry_edit = ttk.Entry(edit_frame, width=textboxWidth, textvariable=clientID)
clientID_entry_edit.grid(column=1, row=1, sticky=(W, E))

ttk.Label(edit_frame, text="Client DOB").grid(column=0, row=2, sticky=W)
clientDOB_entry_edit = ttk.Entry(edit_frame, width=textboxWidth, textvariable=clientDOB)
clientDOB_entry_edit.grid(column=1, row=2, sticky=(W, E))

# Entry point to the application
