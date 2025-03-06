# 環境構築手順書

## 1 本書について

本書は、人流データ標準変換ツールの利用環境構築手順について記載しています。

> [!TIP]
> 本システムの構成や仕様の詳細については[技術検証レポート][TechnicalReport]も参考にしてください。

## 2 動作環境

本システムの動作環境は以下のとおりです。

| 項目| 最小動作環境| 推奨動作環境|
| - | - | - |
| OS | Microsoft Windows 10 または 11（64bit） | 同左 |
| CPU | Intel Core i5以上 | 同左 |
| メモリ | 4GB以上 | 32GB以上 |
| ストレージ | 最低30GB以上の空き容量 | SSDドライブ<br>最低60GB以上の空き容量 |
| ディスプレイ解像度 | 1920×1080以上 | 同左 |
| ネットワーク | 不要 | 同左 |

## 3 インストール手順

1. [GitHubページ][MFConverterGitHub]から「MFConverterMain.zip」をダウンロードします。
2. zipファイルを解凍し、「MFConverterMain.exe」を実行します。

## 4 ビルド手順

自身でソースファイルをダウンロードしビルドを行うことで本システムを実行することができます<br>
ソースファイルは[こちら][MFConverterGitHub]からダウンロード可能です。
GitHubからダウンロードしたソースファイルの構成は以下のようになっています。

```bash
MFConverter
  ├─FormatData
  ├─GUI
  └─Utils
```

ビルド方法は次のとおりです。<br>
本システムをビルドするには[Python 3.11][Python_official]および[pip][Python_pip]が必要です。<br>
pipはPython3.4以降には標準で付属するため、Pythonのインストールと同時にインストールされます。<br>

1. PowerShellでダウンロードした「MFConverter」フォルダに移動します。
2. 次のコマンドを実行します。

```bash
pip install -r requirements.txt
```

3. 次のコマンドを実行すると、アプリが起動します。

```bash
Python MFConverterMain.py
```

## 5 準備物一覧

アプリケーションを利用するために以下のデータを入手します。<br>
データの入力方法については操作マニュアルをご参照下さい。

|  | データ種別 | 機能| 用途| 入力方法 |
| - | - | - | - | - |
| ①|データサプライヤから人流データを調達します<br>対応しているフォーマットや独自フォーマットの定義方法については[操作マニュアル][UserMan]、[データ変換定義ファイルの記述方法][DataDefine]を参照下さい  | 人流データ変換 | 変換元データ | 本システムのUIよりファイルダイアログを開き選択|

<!---GitHubページなどは確定次第修正して下さい-->
[TechnicalReport]: https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_tech_doc_0102_ver01.pdf
[MFConverterGitHub]: https://github.com/Project-PLATEAU/MF-JSON-Converter
[UserMan]: userMan.md
[DataDefine]: dataDefineMan.md
[Python_official]: https://www.python.org/
[Python_pip]: https://docs.python.org/ja/3.11/installing/index.html
