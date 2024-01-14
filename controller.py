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

def save_project_data(key, value):
    with open(data.project_file_path) as file:
        data = json.load(file)
        data[key] = value
    with open(data.project_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def new_project():
    pass

def open_project():
    open_project_file = view.open_file_dialog(".alp",(("AissemblyLite Project files", "*.alp"),))
    if open_project_file:
        with open(open_project_file) as file:
            data = json.load(file)
        global project_idea
        project_idea = data["idea"]
        language = data["language"]
        include_art = data["include_art"]
        messages = data["messages"]
        tasks = data["tasks"]

        if language in data.programming_languages_dropdown_options:
            view.set_programming_languages_dropdown(language)
        else:
            view.show_error("Programming language not found", "The programming language '"+language+"' is not available")
            return

        data.project_folder_path = os.path.dirname(open_project_file)
        data.project_file_path = open_project_file
        view.set_project_name(os.path.splitext(os.path.basename(open_project_file))[0])

def save_project():
    save_project_file = view.save_file_dialog(".alp",(("AissemblyLite Project files", "*.alp"),))
    if save_project_file:
        with open(save_project_file, "w") as file:
            project_name = os.path.splitext(os.path.basename(save_project_file))[0]
            new_project_data["language"] = programming_languages_dropdown.get()
            new_project_data["include_art"] = art_checkbox_var.get()
            json.dump(new_project_data, file, indent=4)
        data.project_folder_path = os.path.dirname(save_project_file)
        data.project_file_path = save_project_file
        view.set_project_name(project_name)

def load_settings():
    settings = {}
    with open('settings.json', 'r') as file:
        settings = json.load(file)
    data.settings_api = settings
    return settings

# Save the settings to a file
def save_settings(settings):
    with open("settings_api.json", "w") as file:
        json.dump(settings, file, indent=4)
    data.settings_api = settings

def send_message():
    global project_idea
    if project_idea == "":
        if data.project_folder_path == "":
            view.show_error("Save location not set", "The project needs to be saved first")
        else:
            project_idea = message_textbox.get("1.0", "end").rstrip("\n")
            save_project_data("idea", message_textbox.get("1.0", "end").rstrip("\n"))
            chat_textbox.configure(state="normal")
            chat_textbox.delete("1.0", "end")
            chat_textbox.configure(state="disabled")
            update_chat_tab("Idea: " + message_textbox.get("1.0", "end").rstrip("\n"))
    else:
        update_chat_tab("User: " + message_textbox.get("1.0", "end").rstrip("\n"))
    message_textbox.delete("1.0", "end")

def start_stop():
    if start_stop_button["text"] == "Start":
        if data.project_folder_path == "":
            view.show_error("Save location not set", "The project needs to be saved first")
        else:
            if project_idea == "":
                view.show_error("Idea not set", "Set the idea by sending the first message")
            else:
                # TODO: start the project
                start_stop_button["text"] = "Stop"
    else:
        start_stop_button["text"] = "Start"
        # TODO: stop the project