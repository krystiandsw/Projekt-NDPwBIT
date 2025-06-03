import sys
import os

def get_format(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".json"]:
        return "json"
    elif ext in [".yml", ".yaml"]:
        return "yaml"
    elif ext == ".xml":
        return "xml"
    else:
        raise ValueError("Unsupported file format: " + ext)

def main():
    if len(sys.argv) != 3:
        print("Usage: program.exe input_file.x output_file.y")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    input_format = get_format(input_path)
    output_format = get_format(output_path)

    try:
        # Read input
        if input_format == "json":
            data = read_json(input_path)
        elif input_format == "yaml":
            data = read_yaml(input_path)
        elif input_format == "xml":
            data = read_xml(input_path)
        else:
            raise ValueError("Unsupported input format")

        # Write output
        if output_format == "json":
            write_json(data, output_path)
        elif output_format == "yaml":
            write_yaml(data, output_path)
        elif output_format == "xml":
            write_xml(data, output_path)
        else:
            raise ValueError("Unsupported output format")

        print(f"âœ”ï¸ Converted {input_format} â†’ {output_format} successfully!")

    except Exception as e:
        print("âŒ Error:", e)

if __name__ == "__main__":
    main()

import json

def read_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise ValueError(f"Invalid JSON file: {e}")

def write_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
