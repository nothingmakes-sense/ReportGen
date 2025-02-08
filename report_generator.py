import datetime
import threading
from AIResponses import AIResponse
from SaveDocx import pDocx
from gui_helpers import popup_gen, popup_err
import tkinter as tk
from tkinter import *
from tkinter import ttk

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