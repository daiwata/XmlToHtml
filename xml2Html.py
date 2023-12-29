import os
import sys
import json
import xmltodict
from pathlib import Path

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

</style>
</head>
<body>
!!contents!!
</body>
</html>
"""


"""
Converts a JSON or YAML object into an HTML string.
"""
def obj2html(obj):
    """
    Converts a JSON or YAML object into an HTML string with stable ordering.
    Adds a class 'undefined' to <td> elements if the key does not exist in the dict.
    """
    if isinstance(obj, dict):
        html = '<table><tbody>'
        for key in sorted(obj.keys()):
            html += f'<tr><th>{key}</th><td>{obj2html(obj[key])}</td></tr>'
        html += '</tbody></table>'
    elif isinstance(obj, list):
        if all(isinstance(item, dict) for item in obj):
            keys = sorted({key for item in obj for key in item.keys()})
            html = '<table><tbody><tr>' + ''.join(f'<th>{key}</th>' for key in keys) + '</tr>'
            for item in obj:
                html += '<tr>'
                for key in keys:
                    value = item.get(key, "")
                    class_attr = ' class="undefined"' if value == "" else ""
                    html += f'<td{class_attr}>{obj2html(value)}</td>'
                html += '</tr>'
            html += '</tbody></table>'
        else:
            html = '<ul>' + ''.join(f'<li>{obj2html(item)}</li>' for item in obj) + '</ul>'
    else:
        html = str(obj).replace('\n', '<br>')
    return html

if len(sys.argv) < 2 or (not Path(sys.argv[1]).exists()):
    print("引数にファイルを渡してください")
    sys.exit()

input_xml_path = sys.argv[1]
input_xml_name = os.path.splitext(os.path.basename(input_xml_path))[0]

with open(input_xml_path, encoding='UTF-8') as f:
    input_xml_contents = f.read()
    dict_data = xmltodict.parse(input_xml_contents)

#中間jsonのファイル出力
#with open(input_xml_name + '.json', 'w',  encoding='UTF-8') as f:
#    f.write(json.dumps(dict_data))

html_contents = obj2html(dict_data)

output_html_contents = html_template.replace("!!title!!", input_xml_name).replace("!!contents!!", html_contents)

with open(input_xml_name + '.html', 'w',  encoding='UTF-8') as f:
    f.write(output_html_contents)

