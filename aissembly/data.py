# --- Empty variables ---
settings_api = {}
settings_textgen = {}
settings_image = {}
project_data = {
    "language": "",
    "group": "",
    "messages": [],
    "logs": [],
    "tasks": []
}

project_file_path = ""
project_folder_path = ""

# --- Options ---
programming_languages_dropdown_options = ["Python", "C++ (WIP)"]

groups_dropdown_options = []

templates_dropdown_options = []

mention_dropdown_options = []

# --- Defaults ---
settings_api_default = {
    "llm_api_url": "",
    "image_api_url": ""
}

settings_textgen_default = {
    "prompt": "",
    "max_tokens": 500,
    "temperature": 1,
    "top_p": 0.9,
    "seed": -1
}

settings_image_default = {
    "prompt": "",
    "steps": 20,
    "tiling": False
}


project_data_default = {
    "language": "",
    "group": "",
    "messages": [],
    "logs": [],
    "tasks": []
}

# UNUSED
textgen_message = {
    "log": "",
    "tasks": [
        {
            "id": "1",
            "title": "",
            "task": ""
        },
        {
            "id": "2",
            "title": "",
            "task": ""
        }
    ],
    "write": {
        "file": "",
        "content": ""
    },
    "image": {
        "file": "",
        "prompt": "",
        "tiling": ""
    }
}