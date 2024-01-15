import data
import controller
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font

# Create the main window
root = tk.Tk()
root.title("AissemblyLite")

def save_file_dialog(defaultextension, filetypes):
    location = filedialog.asksaveasfilename(defaultextension=defaultextension,filetypes=filetypes)
    return location

def open_file_dialog(defaultextension, filetypes):
    location = filedialog.askopenfilename(defaultextension=defaultextension,filetypes=filetypes)
    return location

def show_error(title, text):
    messagebox.showerror(title, text)

def set_project_name(name):
    root.title("AissemblyLite - " + name)

def create_menu():
    # Create the menu bar
    menu_bar = tk.Menu(root)
    # Create the File menu and its items
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=controller.new_project)
    file_menu.add_command(label="Open", command=controller.open_project)
    file_menu.add_command(label="Save", command=controller.save_project)
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
    def start_stop_button_clicked():
        if start_stop_button["text"] == "Start":
            if data.project_folder_path == "":
                show_error("Save location not set", "The project needs to be saved first")
            else:
                if data.project_data["project_idea"] == "":
                    show_error("Idea not set", "Set the idea by sending the first message")
                else:
                    start_stop_button["text"] = "Stop"
                    controller.start_project()
        else:
            start_stop_button["text"] = "Start"
            controller.start_project()
    
    def message_button_clicked():
        controller.send_message(message_textbox.get("1.0", "end").rstrip("\n"))

    settings_frame = ttk.Frame(root)

    programming_languages_label = tk.Label(settings_frame, text="Programming Language")
    programming_languages_label.pack(side="left")
    global programming_languages_dropdown
    programming_languages_dropdown = ttk.Combobox(settings_frame, values=data.programming_languages_dropdown_options, state="readonly")
    programming_languages_dropdown.set(data.programming_languages_dropdown_options[0])
    programming_languages_dropdown.pack(side="left")

    start_stop_button = tk.Button(settings_frame, text="Start", command=start_stop_button_clicked)
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
    message_button = tk.Button(root, text="Send", command=message_button_clicked, height=3, width=12)
    message_button.pack(side="right")

def empty_message_textbox():
    message_textbox.delete("1.0", "end")

def empty_chat_tab():
    chat_textbox.delete("1.0", "end")

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

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("200x220")

    def save_settings_button_clicked():
        settings = {"llm_api_url": llm_api_entry.get(), "image_api_url": image_api_entry.get()}
        controller.save_settings(settings)
        settings_window.destroy()

    controller.load_settings()
    # API text fields
    llm_api_label = tk.Label(settings_window, text="LLM API URL")
    llm_api_label.pack()
    llm_api_entry = tk.Entry(settings_window)
    llm_api_entry.insert("end", data.settings_api["llm_api_url"])  # Load the value from the settings
    llm_api_entry.pack()

    image_api_label = tk.Label(settings_window, text="Image API")
    image_api_label.pack()
    image_api_entry = tk.Entry(settings_window)
    image_api_entry.insert("end", data.settings_api["image_api_url"])  # Load the value from the settings
    image_api_entry.pack()
  
    save_settings_button = tk.Button(settings_window, text="Save", command=save_settings_button_clicked)
    save_settings_button.pack()

    settings_window.focus()

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
