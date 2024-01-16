import aissembly.data as data
import aissembly.view as view
import os
import json
import requests

def textgen_request(agent, message):
    with open("groups/" + view.groups_dropdown.get() + ".json", "r") as file:
        loaded_group = json.load(file)
    instruction = loaded_group[agent]["instruction"]
    instruction = replace_text(instruction, "language", view.programming_languages_dropdown.get())

    with open("templates/" + view.templates_dropdown.get() + ".txt", "r") as file:
        template = replace_text(file.read(), "instruction", instruction)
        template = replace_text(template, "prompt", message)

    data.settings_textgen["prompt"] = template
    print(data.settings_textgen)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=data.settings_api["llm_api_url"] + "/completions", headers=headers, json=data.settings_textgen, verify=False)
    if response == "<Response [500]>": # Nog testen
        return None
    else:
        return response.json()

def imagegen_request():
    pass

def new_project():
    pass

def open_project():
    open_project_file = view.open_file_dialog(".alp",(("AissemblyLite Project files", "*.alp"),))
    if open_project_file:
        with open(open_project_file) as file:
            loaded_project_data = json.load(file)
        data.project_data = loaded_project_data

        if loaded_project_data["language"] in data.programming_languages_dropdown_options:
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
            json.dump(data.project_data, file, indent=4)
        data.project_folder_path = os.path.dirname(save_project_file)
        data.project_file_path = save_project_file
        project_name = os.path.splitext(os.path.basename(save_project_file))[0]
        view.set_project_name(project_name)

def load_settings():
    with open('settings/settings_api.json', 'r') as file:
        loaded_settings_api = json.load(file)
    data.settings_api = loaded_settings_api

    with open('settings/settings_image.json', 'r') as file:
        loaded_settings_image = json.load(file)
    data.settings_image = loaded_settings_image

    with open('settings/settings_textgen.json', 'r') as file:
        loaded_settings_textgen = json.load(file)
    data.settings_textgen = loaded_settings_textgen

def load_groups():
    files = []
    for file_name in os.listdir("groups"):
        if file_name.endswith('.json'):
            files.append(file_name[:-5])
    data.groups_dropdown_options = files
    data.project_data["group"] = files[0]

def load_templates():
    files = []
    for file_name in os.listdir("templates"):
        if file_name.endswith('.txt'):
            files.append(file_name[:-4])
    data.templates_dropdown_options = files

def load_mentions():
    with open("groups/" + data.project_data["group"] + ".json") as file:
        loaded_group = json.load(file)
    data.mention_dropdown_options = list(loaded_group.keys()) 
    view.mention_dropdown['values'] = data.mention_dropdown_options
    view.mention_dropdown.set(data.mention_dropdown_options[0])

def save_settings(settings):
    with open("settings/settings_api.json", "w") as file:
        json.dump(settings, file, indent=4)
    data.settings_api = settings

def edit_text_index(index, x, y):
    index_tuple = index.split('.')  # Convert index to tuple
    index_tuple[-1] = str(int(index_tuple[-1]) + x)  # Add 2 to the last element of the tuple
    index_tuple[0] = str(int(index_tuple[0]) + y)
    new_end_index = '.'.join(index_tuple)  # Convert tuple back to index string
    return new_end_index

def send_message(text):
    mention = view.mention_dropdown.get()
    # User message
    end_index  = view.chat_textbox.index("end")
    view.update_chat_tab("User: @" + mention + " " + text)
    view.chat_textbox.tag_configure("name_tag", foreground="blue")
    view.chat_textbox.tag_add("name_tag", edit_text_index(end_index, 0, -1), edit_text_index(end_index, 4, -1))

    view.empty_message_textbox()
    data.project_data["messages"].append({"mention": mention, "text": text, "answered": False})

    # Agent message
    response = textgen_request(mention, text)
    data.project_data["messages"].append(response["choices"][0]["text"])
    end_index  = view.chat_textbox.index("end")
    view.update_chat_tab(mention + ": " + response["choices"][0]["text"])
    view.chat_textbox.tag_configure("name_tag", foreground="blue")
    view.chat_textbox.tag_add("name_tag", edit_text_index(end_index, 0, -1), edit_text_index(end_index, len(mention), -1))

def start_project():
    pass

def stop_project():
    pass

def replace_text(input, find, replace):
    output = str(input).replace("{"+find+"}", replace)
    return output

def extract_text_between_tags(input_string, tag):
    start_tag = "<" + tag + ">"
    end_tag = "</" + tag + ">"
    start_index = input_string.find(start_tag)
    end_index = input_string.find(end_tag)
    
    if start_index == -1 or end_index == -1:
        return None
    
    start_index += len(start_tag)
    return input_string[start_index:end_index].strip()