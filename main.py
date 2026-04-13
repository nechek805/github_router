import json
from pathlib import Path

config_path = Path(r"C:\Users\boben\.ssh\config")
data_path = Path("./data.json")


def get_config():
    with open(config_path, "r", encoding="utf-8") as config_file:
        return config_file.read()


def get_data():
    with open(data_path, "r", encoding="utf-8") as data_file:
        return json.load(data_file)


def get_config_identity_file():
    lines = get_config().splitlines()

    inside_github_block = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("Host "):
            inside_github_block = (stripped == "Host github.com")
            continue

        if inside_github_block and stripped.startswith("IdentityFile"):
            parts = stripped.split(maxsplit=1)
            if len(parts) == 2:
                return parts[1]
            raise ValueError("IdentityFile found, but value is missing")

    raise ValueError("IdentityFile for Host github.com not found")


def write_config_identity_file(identity_file):
    lines = get_config().splitlines()

    inside_github_block = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("Host "):
            inside_github_block = (stripped == "Host github.com")
            continue

        if inside_github_block and stripped.startswith("IdentityFile"):
            indent = line[:len(line) - len(line.lstrip())]
            lines[i] = f"{indent}IdentityFile {identity_file}"
            break
    else:
        raise ValueError("IdentityFile for Host github.com not found")

    with open(config_path, "w", encoding="utf-8") as config_file:
        config_file.write("\n".join(lines) + "\n")


data = get_data()
current_config_identity_file = get_config_identity_file()

for item in data:
    if item["sshPath"] == current_config_identity_file:
        print(f"{item['id']=}. {item['mail']=} *selected*")
    else:
        print(f"{item['id']=}. {item['mail']=}")

input_data = input("Enter the num: ").strip()
if not input_data.isdigit():
    raise ValueError("Invalid input")

int_input_data = int(input_data)

if int_input_data not in [item["id"] for item in data]:
    raise KeyError("Invalid input")

selected_item = next(item for item in data if item["id"] == int_input_data)
write_config_identity_file(selected_item["sshPath"])
print("Config updated successfully.")