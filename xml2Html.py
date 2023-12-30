import os
import sys
import json
import xmltodict
from pathlib import Path
import argparse
import fnmatch
import glob

"""
xml2html.py

引数で渡された xml ファイルを解析し、html化するプログラム。

【使い方】
python xml2html sample.xml

動作には python, pip, xmltodict が必要
（python, pip の場所にパスを通す必要あり）

xmltodict のインストール方法
pip install xmltodict
"""

html_template = """
<html>
<head>
<title>!!title!!</title>
<meta charset="UTF-8">
<style>
table, tr, th, td {
    font-size: 12px;
    border: 1px solid #cccccc;
    border-collapse: collapse;
    vertical-align: top;
    padding: 2px 3px;
}
th {
    background-color: #dddddd;
    min-width: 50px;
    max-width: 120px;
    word-break: break-all;
}
td.undefined{
    background-color: #eeeeee;
}
ul {
    margin:0 0 0 -20px;
}

</style>
</head>
<body>
!!contents!!
</body>
</html>
"""


def obj2html(obj):
    """
    Converts a JSON or YAML object into an HTML string.
    Preserves the order of keys as they appear in the object.
    Adds a class 'undefined' to <td> elements if the key does not exist in the dict.
    """
    if isinstance(obj, dict):
        html = "<table><tbody>"
        for key, value in obj.items():
            html += f"<tr><th>{key}</th><td>{obj2html(value)}</td></tr>"
        html += "</tbody></table>"
    elif isinstance(obj, list):
        if all(isinstance(item, dict) for item in obj):
            # Collect all unique keys in the order they appear
            keys = []
            for item in obj:
                for key in item.keys():
                    if key not in keys:
                        keys.append(key)

            html = (
                "<table><tbody><tr>"
                + "".join(f"<th>{key}</th>" for key in keys)
                + "</tr>"
            )
            for item in obj:
                html += "<tr>"
                for key in keys:
                    value = item.get(key, "")
                    class_attr = ' class="undefined"' if value == "" else ""
                    html += f"<td{class_attr}>{obj2html(value)}</td>"
                html += "</tr>"
            html += "</tbody></table>"
        else:
            html = (
                "<ul>" + "".join(f"<li>{obj2html(item)}</li>" for item in obj) + "</ul>"
            )
    else:
        html = str(obj).replace("\n", "<br>")
    return html


def is_excluded(path, exclude_patterns):
    name = os.path.basename(path)
    return any(fnmatch.fnmatch(name, pattern) for pattern in exclude_patterns)


def find_xml_files(patterns, exclude_patterns):
    for pattern in patterns:
        for file_path in glob.glob(pattern, recursive=True):
            if is_excluded(file_path, exclude_patterns):
                continue
            if os.path.isfile(file_path) and file_path.endswith(".xml"):
                yield file_path
            elif os.path.isdir(file_path):
                for root, dirs, files in os.walk(file_path):
                    dirs[:] = [d for d in dirs if not is_excluded(d, exclude_patterns)]
                    for file in files:
                        if fnmatch.fnmatch(file, "*.xml") and not is_excluded(
                            file, exclude_patterns
                        ):
                            yield os.path.join(root, file)


def process_xml_file(xml_file_path, output_directory, base_input_directory):
    # Function to process a single XML file
    with open(xml_file_path, encoding="UTF-8") as f:
        input_xml_contents = f.read()
        dict_data = xmltodict.parse(input_xml_contents)

    html_contents = obj2html(dict_data)
    input_xml_name = os.path.splitext(os.path.basename(xml_file_path))[0]
    output_html_contents = html_template.replace("!!title!!", input_xml_name).replace(
        "!!contents!!", html_contents
    )

    # Determine the output file path, maintaining the input folder structure
    if output_directory:
        relative_path = os.path.relpath(xml_file_path, base_input_directory)
        output_file_path = os.path.join(
            output_directory, os.path.splitext(relative_path)[0] + ".html"
        )
    else:
        output_file_path = os.path.splitext(xml_file_path)[0] + ".html"

    # Creating output directory if it does not exist
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, "w", encoding="UTF-8") as f:
        f.write(output_html_contents)


def main():
    parser = argparse.ArgumentParser(description="XML to HTML converter")
    parser.add_argument(
        "patterns", nargs="+", help="Wildcard patterns for XML files or directories"
    )
    parser.add_argument(
        "--exclude",
        help="Comma-separated list of file or folder names to exclude (supports wildcards)",
        default="",
    )
    parser.add_argument(
        "-o", "--output", help="Output directory for HTML files", default=""
    )
    args = parser.parse_args()

    exclude_patterns = args.exclude.split(",") if args.exclude else []
    input_patterns = args.patterns
    output_directory = args.output if args.output else ""

    base_input_directories = [
        os.path.dirname(os.path.commonprefix(glob.glob(pattern, recursive=True)))
        for pattern in input_patterns
    ]

    for pattern in input_patterns:
        base_input_directory = os.path.dirname(
            os.path.commonprefix(glob.glob(pattern, recursive=True))
        )
        for xml_file in find_xml_files([pattern], exclude_patterns):
            process_xml_file(xml_file, output_directory, base_input_directory)


if __name__ == "__main__":
    main()
