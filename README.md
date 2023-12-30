# xml2Html

XML ファイルを HTML ファイルに変換する Python スクリプトです。

## 機能

- XML ファイルを HTML に変換します。
- ワイルドカードを使って特定のパターンに一致する XML ファイルまたはフォルダを指定できます。
- 引数を複数指定することにより、複数のフォルダ配下やファイルを指定できます。
- 除外するファイルまたはフォルダを指定できます。
- 指定されたフォルダの構造を保ちながら、HTML ファイルを出力します。
- 出力先のフォルダを指定できます。指定しない場合、元の XML ファイルの場所に出力します。

## 事前準備

- python のインストール  
  python をインストールして、python と pip の場所にパスを通しておきます。

- ライブラリ xmltodict のインストール
  ```
  pip install xmltodict
  ```

## 使い方

基本的な使い方は以下の通りです：

```bash
python xml2Html.py [XMLファイルまたはディレクトリのパターン] [オプション]
```

引数の XML ファイルまたはディレクイトリは、ワイルドカード（`*`）で指定可能です。  
スペース区切りで複数指定できます。（パスにスペースを含む場合は、パスを `"` で囲ってください。）

利用可能なオプションは以下の通りです：

- `-o` または `--output`: HTML ファイルの出力先ディレクトリを指定します。
- `--exclude`: 除外するファイルまたはフォルダの名前をカンマ区切りで指定します（ワイルドカード（`*`）対応）。

### 例

XML ファイルを指定して変換する場合：

```bash
python xml2Html.py sample.xml
```

ワイルドカードでファイルを指定する場合：

```bash
python xml2Html.py sample*.xml
```

フォルダ配下を再帰的に探索し、全ての XML ファイルを変換する場合：

```bash
python xml2Html.py path/to/folder/
```

複数のフォルダを指定する場合：

```bash
python xml2Html.py path/to/folderA/ path/to/folderB/
```

ワイルドカードでフォルダを指定する場合：

```bash
python xml2Html.py path/to/folder*/
```

特定のパターンに一致する XML ファイルを変換し、除外リストを指定する場合：

```bash
python xml2Html.py path/to/*.xml --exclude .git,i*
```

出力先を指定する場合：

```bash
python xml2Html.py path/to/folder -o path/to/output/
```

複雑な例：

```bash
python xml2Html.py C:/Users/user/Desktop/folder* C:/work/folderA -o C:/Users/user/Desktop/output12 --exclude .git,i*
```

## 出力例

全て成功した場合

```bash
$ python xml2Html.py /c/work/*.xml
Total: 8 / Success: 8 / Failed: 0
```

失敗を含む場合

```bash
$ python xml2Html.py /c/work/*.xml
Failed to convert C:/work/a.xml: no element found: line 4, column 0
Total: 8 / Success: 7 / Failed: 1
```
