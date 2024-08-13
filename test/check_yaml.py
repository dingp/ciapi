import sys
import json
import yaml

def check_yaml_syntax(file_path):
    try:
        with open(file_path, 'r') as file:
            yaml_content = yaml.safe_load(file)
            return yaml_content
    except Exception as e:
        print(f"Error: {e}")
        return None

def print_yaml_as_json(yaml_content):
    if yaml_content:
        json_content = json.dumps(yaml_content, indent=4)
        print(json_content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the path to a YAML file as an argument.")
        sys.exit(1)

    yaml_file_path = sys.argv[1]
    yaml_content = check_yaml_syntax(yaml_file_path)
    print_yaml_as_json(yaml_content)