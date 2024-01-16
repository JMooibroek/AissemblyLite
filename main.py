from aissembly.controller import *
from aissembly.view import *
from aissembly.data import *


# Load settings
load_settings()
load_groups()
load_templates()

# Create menu and main window
create_menu()
create_main_window()


update_chat_tab("Write and send a text to get started.")
update_log_tab("This is where logs will be displayed.")
update_tasks_tab("This is where tasks will be displayed.")

# Run the main event loop
root.mainloop()