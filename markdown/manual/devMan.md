# 環境構築手順書

## 1 本書について

本書は、人流データ変換ツール（以下「本システム」という。）の利用環境構築手順について記載しています。

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

1. [GitHubページ][MFConverterGitHub]から「MFConverterMain.exe」をダウンロードします。
2. 「MFConverterMain.exe」を実行します。

## 4 ビルド手順

自身でソースファイルをダウンロードしビルドを行うことでプラグインを生成することができます<br>
ソースファイルは[こちら][MFConverterGitHub]からダウンロード可能です。
GitHubからダウンロードしたソースファイルの構成は以下のようになっています。

```bash
MFConverter
  ├─FormatData
  ├─GUI
  └─Utils
```

ビルド方法は次のとおりです。<br>
本システムをビルドするにはPython 3.11が必要です。

> [!TIP]
> 仮想環境を作成して作業することを推奨します。

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
| 1|人流データ | 人流データ | 変換元データ | 各自でご用意下さい<br>対応しているフォーマットや独自フォーマットの定義方法については[操作マニュアル][UserMan]、[任意データの定義][DataDefine]を参照下さい |

<!---GitHubページなどは確定次第修正して下さい-->
[TechnicalReport]: https://www.mlit.go.jp/plateau/news/
[MFConverterGitHub]: https://www.mlit.go.jp/plateau/news/
[UserMan]: userMan.md
[DataDefine]: dataDefineMan.md
