import tkinter as tk
from tkinter import ttk
import json

def popup_err(e):
    win = tk.Toplevel()
    win.wm_title("Error")
    l = tk.Label(win, text=e, wraplength=400, justify="center", padx=20, pady=20, bg='#ffdddd', font=('Arial', 12))
    l.pack(padx=20, pady=20)
    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.pack(pady=10)

def popup_gen(t):
    win = tk.Toplevel()
    win.wm_title(t)
    l = tk.Label(win, text=t, wraplength=400, justify="center", padx=20, pady=20, bg='#ddffdd', font=('Arial', 12))
    l.pack(padx=20, pady=20)
    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.pack(pady=10)

def load_company_name(companyName):
    try:
        with open('template.txt', 'r') as file:
            company_name = file.readline().strip()
            companyName.set(company_name)
    except Exception as e:
        popup_err(f"Failed to load company name: {e}")

def load_patient_data(clientName_combo, update_client_list):
    global patients_data
    try:
        with open('patients.json', 'r') as file:
            patients_data = json.load(file)
            clientName_combo['values'] = [patient['name'] for patient in patients_data]
            update_client_list()
    except Exception as e:
        popup_err(f"Failed to load patient data: {e}")

def load_providers(serviceProvidedBy_combo):
    global providers_data
    try:
        with open('providers.json', 'r') as file:
            providers_data = json.load(file)
            serviceProvidedBy_combo['values'] = [provider['name'] for provider in providers_data]
    except Exception as e:
        popup_err(f"Failed to load providers data: {e}")