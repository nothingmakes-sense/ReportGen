import json
from gui_helpers import popup_err, popup_gen

providers_data = []
patients_data = []  # Initialize patients_data as an empty list

def on_client_name_selected(event, clientName, clientID, clientDOB, serviceProvided, SupportPlan, serviceProvidedBy, patients_data):
    selected_name = clientName.get()
    for patient in patients_data:
        if patient['name'] == selected_name:
            clientID.set(patient['id'])
            clientDOB.set(patient['dob'])
            serviceProvided.set(patient['service'])
            SupportPlan.set(patient['support_plan'])
            serviceProvidedBy.set(patient.get('provider', ''))
            break

def save_client_data(clientName, clientID, clientDOB, serviceProvided, SupportPlan, serviceProvidedBy, clientName_combo, update_client_list):
    new_patient = {
        "name": clientName.get(),
        "id": clientID.get(),
        "dob": clientDOB.get(),
        "service": serviceProvided.get(),
        "support_plan": SupportPlan.get(),
        "provider": serviceProvidedBy.get()
    }

    # Check if the patient already exists and update their information
    for patient in patients_data:
        if patient['name'] == new_patient['name']:
            patient.update(new_patient)
            break
    else:
        # If the patient does not exist, append the new patient data
        patients_data.append(new_patient)

    try:
        with open('patients.json', 'w') as file:
            json.dump(patients_data, file, indent=4)
        popup_gen("Client saved successfully.")
        clientName_combo['values'] = [patient['name'] for patient in patients_data]
        update_client_list()
    except Exception as e:
        popup_err(f"Failed to save client data: {e}")

def delete_client_data(clientName, clientName_combo, update_client_list, clear_client_fields):
    selected_name = clientName.get()
    global patients_data
    patients_data = [patient for patient in patients_data if patient['name'] != selected_name]

    try:
        with open('patients.json', 'w') as file:
            json.dump(patients_data, file, indent=4)
        popup_gen("Client deleted successfully.")
        clientName_combo['values'] = [patient['name'] for patient in patients_data]
        update_client_list()
        clear_client_fields()
    except Exception as e:
        popup_err(f"Failed to delete client data: {e}")

def clear_client_fields(clientName, clientID, clientDOB, serviceProvided, SupportPlan, serviceProvidedBy):
    clientName.set('')
    clientID.set('')
    clientDOB.set('')
    serviceProvided.set('')
    SupportPlan.set('')
    serviceProvidedBy.set('')

def save_provider_data(serviceProvidedBy, serviceProvidedBy_combo):
    new_provider = {
        "name": serviceProvidedBy.get()
    }

    # Check if the provider already exists and update their information
    for provider in providers_data:
        if provider['name'] == new_provider['name']:
            provider.update(new_provider)
            break
    else:
        # If the provider does not exist, append the new provider data
        providers_data.append(new_provider)

    try:
        with open('providers.json', 'w') as file:
            json.dump(providers_data, file, indent=4)
        popup_gen("Provider saved successfully.")
        serviceProvidedBy_combo['values'] = [provider['name'] for provider in providers_data]
    except Exception as e:
        popup_err(f"Failed to save provider data: {e}")