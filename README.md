# amplify_hackathon

## 実行方法

1. 環境変数 `AMPLIFY_TOKEN` にアクセストークンを入力する

```shell
$ export AMPLIFY_TOKEN=XXXX
```

2. *src/app.py* を実行する

```shell
$ python src/app.py
```

3. `http://localhost:5000` にブラウザでアクセスする（ポート番号は適時変更）



# テーマ
学校のクラス分け

# 制約
1. 各生徒はただ1つのクラスのみ在籍する
2. クラス間で男女数を均等にする
3. 各クラス間で学力差を均等にする
4. クラス間で学区のばらつきを均等にする
5. 相性が合わない生徒同士を同じクラスにしない

- その他(今回は考えない)
	- モンスターペアレンツなどの問題のある保護者の振り分け
	- 学習障害，発達障害など特別な支援を要する児童の振り分け
	- 相性が合わない親同士の振り分け
	- 運動能力差が出ないような振り分け

> 参考URL
> 
> https://makomako108.net/2016/10/21/syougakkou-classwake/#:~:text=%E5%9F%BA%E6%9C%AC%E7%9A%84%E3%81%AA%E8%80%83%E3%81%88%E6%96%B9%E3%81%AF,%E5%9F%BA%E6%9C%AC%E7%9A%84%E3%81%AA%E8%80%83%E3%81%88%E6%96%B9%E3%81%A7%E3%81%99%E3%80%82


# 入力データ
ファイルで入力する場合のデータはCSVとする．
例を以下に示す．
``` 
$ input.csv

index,name,sex,level,area,hate1,hate2,hate3
1,Fukada Keisuke,M,59,2,0,0,0
2,Yoshimura Tomokazu,M,52,2,18,0,0
3,Yachi Yuta,M,42,1,0,62,0
4,Tawada Masashi,M,63,3,0,0,0
5,Sato Hanako,F,47,5,0,0,0
.
.
.
```

| カラム名 | 型 | 説明 | カラムが取る値 |
|:--|:--|:--|:--|
| index | int | 生徒の出席番号 | 1~(生徒数) |
| name | string | 生徒の名前 |  |
| sex | string | 性別 | M/Fの2値 |
| level | int | 生徒の学力 | 平均μ，標準偏差σの正規分布の整数値 |
| area | int | 生徒の学区 | 1~(学区数) |
| hate1 | int | 相性の悪い生徒その1 | 相性の悪い生徒のindex |
| hate2 | int | 相性の悪い生徒その2 | 同上 |
| hate3 | int | 相性の悪い生徒その3 | 同上 |

# License
The source code is licensed MIT. The website content is licensed CC BY 4.0,see LICENSE.