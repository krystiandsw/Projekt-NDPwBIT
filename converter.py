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

import yaml

def read_yaml(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise ValueError(f"Invalid YAML file: {e}")

def write_yaml(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)

import xml.etree.ElementTree as ET

def read_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return etree_to_dict(root)
    except Exception as e:
        raise ValueError(f"Invalid XML file: {e}")

def etree_to_dict(element):
    result = {element.tag: {} if element.attrib else None}
    children = list(element)

    if children:
        dd = {}
        for child in map(etree_to_dict, children):
            for k, v in child.items():
                if k in dd:
                    if isinstance(dd[k], list):
                        dd[k].append(v)
                    else:
                        dd[k] = [dd[k], v]
                else:
                    dd[k] = v
        result = {element.tag: dd}

    if element.attrib:
        result[element.tag].update(("@" + k, v) for k, v in element.attrib.items())

    if element.text and element.text.strip():
        if children or element.attrib:
            result[element.tag]["#text"] = element.text.strip()
        else:
            result[element.tag] = element.text.strip()

    return result

def write_xml(data, file_path):
    root = dict_to_etree("root", data)
    tree = ET.ElementTree(root)
    tree.write(file_path, encoding="utf-8", xml_declaration=True)

def dict_to_etree(tag, d):
    elem = ET.Element(tag)
    if isinstance(d, dict):
        for key, val in d.items():
            if key.startswith("@"):
                elem.set(key[1:], str(val))
            elif key == "#text":
                elem.text = str(val)
            elif isinstance(val, list):
                for item in val:
                    elem.append(dict_to_etree(key, item))
            else:
                elem.append(dict_to_etree(key, val))
    else:
        elem.text = str(d)
    return elem
