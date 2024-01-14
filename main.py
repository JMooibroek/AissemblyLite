import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
import json


def save_project_data(key, value):
    with open(project_file_path) as file:
        data = json.load(file)
        data[key] = value
    with open(project_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def new_project():
    pass

def open_project():
    open_project_file = filedialog.askopenfilename(defaultextension=".alp",filetypes=(("AissemblyLite Project files", "*.alp"),))
    if open_project_file:
        with open(open_project_file) as file:
            data = json.load(file)
        global project_idea
        project_idea = data["idea"]
        language = data["language"]
        include_art = data["include_art"]
        messages = data["messages"]
        tasks = data["tasks"]

        if language in programming_languages_dropdown_options:
            programming_languages_dropdown.set(language)
        else:
            messagebox.showerror("Programming language not found", "The programming language '"+language+"' is not available")
            return

        if include_art:
            art_checkbox.select()
        else:
            art_checkbox.deselect()
        # global project_folder_path
        global project_folder_path
        project_folder_path = os.path.dirname(open_project_file)
        global project_file_path
        project_file_path = open_project_file
        root.title("AissemblyLite - "+ os.path.splitext(os.path.basename(open_project_file))[0])

def save_project():
    save_project_file = filedialog.asksaveasfilename(defaultextension=".alp",filetypes=(("AissemblyLite Project files", "*.alp"),))
    if save_project_file:
        with open(save_project_file, "w") as file:
            project_name = os.path.splitext(os.path.basename(save_project_file))[0]
            new_project_data["language"] = programming_languages_dropdown.get()
            new_project_data["include_art"] = art_checkbox_var.get()
            json.dump(new_project_data, file, indent=4)
        global project_folder_path
        project_folder_path = os.path.dirname(save_project_file)
        global project_file_path
        project_file_path = save_project_file
        root.title("AissemblyLite - "+ project_name)

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("200x220")

    def save_settings():
        llm_api = llm_api_entry.get()
        llm_api_code = llm_api_code_entry.get()
        image_api = image_api_entry.get()
        image_api_code = image_api_code_entry.get()

        # Save the settings to a file
        with open("settings.txt", "w") as file:
            file.write(f"LLM_API={llm_api}\n")
            file.write(f"LLM_API_CODE={llm_api_code}\n")
            file.write(f"IMAGE_API={image_api}\n")
            file.write(f"IMAGE_API_CODE={image_api_code}\n")
        load_settings()
        settings_window.destroy()

    with open("settings.txt", "r") as file:
        settings = file.read()

    # Extract the values from the settings string
    for line in settings.split("\n"):
        if line.startswith("LLM_API_CODE"):
            llm_api_code = line.split("=")[1].strip()
        elif line.startswith("LLM_API"):
            llm_api = line.split("=")[1].strip()
        elif line.startswith("IMAGE_API_CODE"):
            image_api_code = line.split("=")[1].strip()
        elif line.startswith("IMAGE_API"):
            image_api = line.split("=")[1].strip()

    # API text fields
    llm_api_label = tk.Label(settings_window, text="LLM API")
    llm_api_label.pack()
    llm_api_entry = tk.Entry(settings_window)
    llm_api_entry.insert("end", llm_api)  # Load the value from the settings
    llm_api_entry.pack()

    llm_api_code_label = tk.Label(settings_window, text="LLM API Code")
    llm_api_code_label.pack()
    llm_api_code_entry = tk.Entry(settings_window)
    llm_api_code_entry.insert("end", llm_api_code)  # Load the value from the settings
    llm_api_code_entry.pack()

    image_api_label = tk.Label(settings_window, text="Image API")
    image_api_label.pack()
    image_api_entry = tk.Entry(settings_window)
    image_api_entry.insert("end", image_api)  # Load the value from the settings
    image_api_entry.pack()

    image_api_code_label = tk.Label(settings_window, text="Image API Code")
    image_api_code_label.pack()
    image_api_code_entry = tk.Entry(settings_window)
    image_api_code_entry.insert("end", image_api_code)  # Load the value from the settings
    image_api_code_entry.pack()

    
    save_settings_button = tk.Button(settings_window, text="Save", command=save_settings)
    save_settings_button.pack()

    settings_window.focus()

def load_settings():
    with open("settings.txt", "r") as file:
        settings = file.read()
    for line in settings.split("\n"):
        if line.startswith("LLM_API_CODE"):
            global llm_api_code
            llm_api_code = line.split("=")[1].strip()
        elif line.startswith("LLM_API"):
            global llm_api
            llm_api = line.split("=")[1].strip()
        elif line.startswith("IMAGE_API_CODE"):
            image_api_code = line.split("=")[1].strip()
        elif line.startswith("IMAGE_API"):
            image_api = line.split("=")[1].strip()

def open_help():
    help_window = tk.Toplevel(root)
    help_window.title("Help")
    help_window.geometry("200x220")
    # TODO: add help

def open_about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("200x220")
    # TODO: add about

def send_message():
    global project_idea
    if project_idea == "":
        if project_folder_path == "":
            messagebox.showerror("Save location not set", "The project needs to be saved first")
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
        if project_folder_path == "":
            messagebox.showerror("Save location not set", "The project needs to be saved first")
        else:
            if project_idea == "":
                messagebox.showerror("Idea not set", "Set the idea by sending the first message")
            else:
                # TODO: start the project
                start_stop_button["text"] = "Stop"
    else:
        start_stop_button["text"] = "Start"
        # TODO: stop the project

def update_chat_tab(text):
    chat_textbox.configure(state="normal")  # Enable editing
    chat_textbox.insert("end", text + "\n")  # Insert text at the end
    chat_textbox.configure(state="disabled")  # Disable editing

def update_log_tab(text):
    log_textbox.configure(state="normal")  # Enable editing
    log_textbox.insert("end", text + "\n")  # Insert text at the end
    log_textbox.configure(state="disabled")  # Disable editing

def update_tasks_tab(text):
    tasks_textbox.configure(state="normal")  # Enable editing
    tasks_textbox.insert("end", text + "\n")  # Insert text at the end
    tasks_textbox.configure(state="disabled")  # Disable editing

# Create the main window
root = tk.Tk()
root.title("AissemblyLite")

def create_menu():
    # Create the menu bar
    menu_bar = tk.Menu(root)
    # Create the File menu and its items
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=new_project)
    file_menu.add_command(label="Open", command=open_project)
    file_menu.add_command(label="Save", command=save_project)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    # Create the Edit menu and its items
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    edit_menu.add_command(label="Settings", command=open_settings)

    # Create the Help menu and its items
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Help", command=open_help)
    help_menu.add_separator()
    help_menu.add_command(label="About", command=open_about)

    # Add the File and Edit menus to the menu bar
    menu_bar.add_cascade(label="File", menu=file_menu)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    # Configure the root window to use the menu bar
    root.config(menu=menu_bar)

def create_main_window():
    settings_frame = ttk.Frame(root)
    programming_languages_label = tk.Label(settings_frame, text="Programming Language")
    programming_languages_label.pack(side="left")
    global programming_languages_dropdown_options
    programming_languages_dropdown_options = ["Python", "C++"]
    global programming_languages_dropdown
    programming_languages_dropdown = ttk.Combobox(settings_frame, values=programming_languages_dropdown_options, state="readonly")
    programming_languages_dropdown.set(programming_languages_dropdown_options[0])
    programming_languages_dropdown.pack(side="left")

    global art_checkbox
    art_checkbox = tk.Checkbutton(settings_frame, text="Include Art", variable=art_checkbox_var)
    art_checkbox.bind
    art_checkbox.pack(side="left", padx=30)

    global start_stop_button
    start_stop_button = tk.Button(settings_frame, text="Start", command=start_stop)
    start_stop_button.pack(side="right")

    settings_frame.pack(side="top", fill="x")

    tab_control = ttk.Notebook(root)

    chat_tab = ttk.Frame(tab_control)
    global chat_textbox
    chat_textbox = tk.Text(chat_tab, state="disabled")
    chat_textbox.pack(fill="both", expand=True)
    tab_control.add(chat_tab, text="Chat")

    log_tab = ttk.Frame(tab_control)
    global log_textbox
    log_textbox = tk.Text(log_tab, state="disabled")
    log_textbox.pack(fill="both", expand=True)
    tab_control.add(log_tab, text="Log")

    tasks_tab = ttk.Frame(tab_control)
    global tasks_textbox
    tasks_textbox = tk.Text(tasks_tab, state="disabled")
    tasks_textbox.pack(fill="both", expand=True)
    tab_control.add(tasks_tab, text="Tasks")

    tab_control.pack(fill="both", expand=True)

    global message_textbox
    message_textbox = tk.Text(root, height=3)
    message_textbox.pack(side="left", fill="both")
    message_button = tk.Button(root, text="Send", command=send_message, height=3, width=12)
    message_button.pack(side="right")

project_folder_path = ""
project_file_path = ""
project_idea = ""
art_checkbox_var = tk.BooleanVar()
new_project_data = {
    "idea": "",
    "language": "",
    "include_art": "",
    "messages": [],
    "tasks": []
}

load_settings()


create_menu()
create_main_window()

update_chat_tab("Write and send an idea to get started.")
update_log_tab("This is where logs will be displayed.")
update_tasks_tab("This is where tasks will be displayed.")

# Run the main event loop
root.mainloop()