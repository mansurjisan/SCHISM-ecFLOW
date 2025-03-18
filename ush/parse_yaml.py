import yaml
import sys
import os


def get_yaml_value(yaml_file, key_path):
    """Extract a value from YAML file using dot notation key path"""
    try:
        with open(yaml_file, 'r') as f:
            config = yaml.safe_load(f)

        # Navigate through nested keys
        keys = key_path.split('.')
        value = config
        for k in keys:
            value = value[k]

        print(value)
        return 0
    except Exception as e:
        print(f"Error parsing YAML: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./parse_yaml.py config.yml 'key.path'", file=sys.stderr)
        sys.exit(1)

    yaml_file = sys.argv[1]
    key_path = sys.argv[2]
    sys.exit(get_yaml_value(yaml_file, key_path))
