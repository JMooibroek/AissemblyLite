from controller import *
from view import *
from data import *

# Define project-related variables
project_folder_path = ""
project_file_path = ""
project_idea = ""
art_checkbox_var = tk.BooleanVar()


# Load settings
load_settings()

# Create menu and main window
create_menu()
create_main_window()

update_chat_tab("Write and send an idea to get started.")
update_log_tab("This is where logs will be displayed.")
update_tasks_tab("This is where tasks will be displayed.")

# Run the main event loop
root.mainloop()