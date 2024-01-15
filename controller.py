import data
import view
import os
import json
import requests

def textgen_request(url, prompt, prompt_settings):
    prompt_settings["prompt"] = prompt
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=f'{url}/completions', headers=headers, json=prompt_settings, verify=False)
    return response.json()

def new_project():
    pass

def open_project():
    open_project_file = view.open_file_dialog(".alp",(("AissemblyLite Project files", "*.alp"),))
    if open_project_file:
        with open(open_project_file) as file:
            loaded_project_data = json.load(file)
        data.project_data["idea"] = loaded_project_data["idea"]

        if loaded_project_data["language"] in data.programming_languages_dropdown_options:
            data.project_data["language"] = loaded_project_data["language"]
            view.programming_languages_dropdown.set(loaded_project_data["language"])
        else:
            view.show_error("Programming language not found", "The programming language '"+loaded_project_data["language"]+"' is not available")
            return

        data.project_folder_path = os.path.dirname(open_project_file)
        data.project_file_path = open_project_file
        view.set_project_name(os.path.splitext(os.path.basename(open_project_file))[0])

def save_project():
    save_project_file = view.save_file_dialog(".alp",(("AissemblyLite Project files", "*.alp"),))
    if save_project_file:
        with open(save_project_file, "w") as file:
            project_name = os.path.splitext(os.path.basename(save_project_file))[0]
            data.project_data["language"] = view.programming_languages_dropdown.get()
            json.dump(data.project_data, file, indent=4)
        data.project_folder_path = os.path.dirname(save_project_file)
        data.project_file_path = save_project_file
        view.set_project_name(project_name)

def load_settings():
    settings = {}
    with open('settings_api.json', 'r') as file:
        settings = json.load(file)
    data.settings_api = settings
    return settings

def save_settings(settings):
    with open("settings_api.json", "w") as file:
        json.dump(settings, file, indent=4)
    data.settings_api = settings

def send_message(text):
    if data.project_data["idea"] == "":
        if data.project_folder_path == "":
            view.show_error("Save location not set", "The project needs to be saved first")
        else:
            data.project_data["idea"] = text
            view.empty_chat_tab()
            view.update_chat_tab("Idea: " + text)
    else:
        view.update_chat_tab("User: " + text)
    view.empty_message_textbox()

def start_project():
    pass

def stop_project():
    pass