# データ変換定義ファイルの記述方法

# 1 本書について

本書では、人流データ変換ツールで用いるiniファイルの使用、記述方法について記載しています。

# 2 使い方

ファイル名「DefinedFormat.ini」を用意し、「MFConverterMain.py」と同じ階層に配置して使用します。
人流データの変換実行時に読み込んだファイルフォーマットがプリセットで用意されている３社
([株式会社ブログウォッチャー](https://www.blogwatcher.co.jp/)、[株式会社Agoop](https://agoop.co.jp/)、[株式会社Unerry](https://www.unerry.co.jp/))
のいずれのデータでもなかった場合に設定ファイルの読み込みを行い、変換可否の判断、変換を行います。

# 3 記述方法

設定ファイルでは変換するデータの個別の値が変換元のファイルのどこに記述されているか、またその記述様式について設定します。

設定ファイルはINIファイル形式で記述され、セクションとパラメータを持ちます。<br>

パラメータは名前と値を持ち,等号「=」で区切られ、左辺が名前、右辺が値になります。
	
	name=value
	
セクションはパラメータのグループ分けに用い、セクション名は角括弧「[]」で囲って宣言します。<br>
各パラメータは直前に宣言されたセクションに属します。
	
	[section]

	
MF-JSON形式の人流データへの変換には１つの移動体情報につき、下記が必要となります。
- 移動体識別子
- 移動体検出日時
- 二次元座標(緯度,経度)

また、選択項目として下記についても規定、変換することができます。
- 性別
- 年齢

設定ファイルの記述方法は読み込むデータフォーマットによって異なります。

## 3-1. CSVファイルの変換定義

CSVファイルでは下記セクションについて設定します。

| セクション　　|　パラメータ  |　詳細  |必記要素|
|--------------|--------|----|----|
|id            |param_path| 移動体識別子　|〇|
|year          |param_path<br>date_format|年  |〇|
|month          |param_path<br>date_format|月  |〇|
|day          |param_path<br>date_format|日  |〇|
|hour         |param_path<br>date_format|時 |〇|
|minute         |param_path<br>date_format|分  |〇|
|second          |param_path<br>date_format|秒  |×|
|latitude      |param_path|緯度  |〇|
|longitude     |param_path| 経度 |〇|
|gender        |param_path| 性別 |×|
|age           |param_path| 年齢 |×|


`param_path`に各数値の列のヘッダーを設定します。<br>
日時関連のデータセクションでは`date_format`にISO8601書式で記述方法を設定します。<br>

__記述例__
***
__変換元ファイル__

|dailyid |年|月|日|時|分|秒|緯度|経度|  
|----|----|----|----|----|----|----|--------|----|
|001|2025|02|07|12|30|0|35.681236|139.767125|
|002|2025|02|07|12|32|0|35.680500|139.767140|
|003|2025|02|07|12|34|0|35.680490|139.766800|


__設定ファイル__
	
	[id]
	param_header = dailyid
	[year]
	param_header =年
	date_format=%Y
	[month]
	param_header =月
	date_format=%m
	[day]
	param_header =日
	date_format=%d
	[hour]
	param_header =時
	date_format=%H
	[minute]
	param_header =分
	date_format=%M
	[second]
	param_header =秒
	date_format=%S
	[latitude]
	param_header =緯度
	[longitude]
	param_header =経度
	

## 3-2.JSONファイルの変換定義

JSONファイルでは下記セクションについて設定します。

| セクション　　    |　パラメータ  |説明 |必記要素|
|--------------|--------|----|----|
|id            |param_path<br>param_type| 移動体識別子　|〇|
|date          |param_path<br>param_type<br>date_format|移動体検出日時 |〇|
|latitude      |param_path<br>param_type|緯度  |〇|
|longitude     |param_path<br>param_type| 経度 |〇|
|gender        |param_path<br>param_type| 性別 |×|
|age           |param_path<br>param_type| 年齢 |×|

各セクションの`param_path`に値の記述位置をJsonPath形式で設定します。<br>
`param_type`に記述形式(キー：`key`か値：`value`)を設定します。<br>
`date`については`date_format`にISO8601書式で記述方法を設定します。<br>


JsonPathでは<br>
- 「$」がRootノードを示します。<br>
- 「\.」で各要素を区切ります。<br>
- 任意要素は「\*」で記載します。<br>
- 配列要素は「\[ \]」で何番目の要素かを示します。<br>
<br>

__記述例__
***
__変換元ファイル__
	
	{
	  "timestamps": {
		"2025-02-04T12:00:00Z": [
		  {
			"pedestrian_id": 1,
			"location": { "latitude": 35.681236, "longitude": 139.767125 }
		  },
		  {
			"pedestrian_id": 2,
			"location": { "latitude": 35.680500, "longitude": 139.766800 }
		  }
		],
		"2025-02-04T12:00:01Z": [
		  {
			"pedestrian_id": 1,
			"location": { "latitude": 35.681250, "longitude": 139.767140 }
		  },
		  {
			"pedestrian_id": 2,
			"location": { "latitude": 35.680490, "longitude": 139.766800 }
		  }
		]
	  }
	}
	
__設定ファイル__

	[id]
	param_path=$.timestamps[*].*.pedestrian_id
	param_type=value
	[date]
	param_path=$.timestamps[*]
	param_type=key
	date_format=%Y-%m-%dT%H:%M:%SZ
	[latitude]
	param_path=$.timestamps[*].*.location.latitude
	param_type=value
	[longitude]
	param_path=$.timestamps[*].*.location.longitude
	param_type=value

## 3-3.XMLファイルの変換定義

XMLファイルでは下記セクションについて設定します。

| セクション　　    |　パラメータ  |説明 |必記要素|
|--------------|--------|----|----|
|id            |param_path| 移動体識別子　|〇|
|date          |param_path<br>date_format|移動体検出日時 |〇|
|latitude      |param_path|緯度  |〇|
|longitude     |param_path| 経度 |〇|
|gender        |param_path| 性別 |×|
|age           |param_path| 年齢 |×|

`param_path`に各数値のxPathを設定します。<br>
`date`については`date_format`にISO8601書式で記述方法を設定します。<br>

xPathでは
- 「\\」で各要素を区切ります。<br>
- 属性情報として保存されている値は「@」で区切ります。<br>
- 任意要素は「\*」で記載します。


__記述例__
***
__変換元ファイル__

	<PedestrianFlow>
		<Pedestrian id="1">
			<Position latitude="35.6895" longitude="139.6917" />
			<Timestamp>2025-01-30T12:00:00Z</Timestamp>
		</Pedestrian>		
		<Pedestrian id="2">
			<Position latitude="35.6880" longitude="139.6920" />
			<Timestamp>2025-01-30T12:00:05Z</Timestamp>
		</Pedestrian>
	</PedestrianFlow>
	
	
__設定ファイル__
	
	[id]
	param_path=\PedestrianFlow\Pedestrian@id
	[date]
	param_path=\PedestrianFlow\Pedestriantimestamp[*]
	date_format=%Y-%m-%dT%H:%M:%SZ
	[latitude]
	param_path=\PedestrianFlow\Pedestrian\Position@latitude
	[longitude]
	param_path=\PedestrianFlow\Pedestrian\Position@longitude

