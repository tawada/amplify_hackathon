import numpy as np
import pandas as pd

num_student = 100 # 生徒の数
ability_avg = 50  # 学力の平均
ability_sd = 10   # 学力の標準偏差
num_area = 5      # 地域の数
num_hate = 3      # 嫌いな人の数
hate_prob = 0.1   # 嫌いな人ができる確率
data_path = "./../data/all_data.csv"

# 名前を生成
last_name  = ["Togawa", "Watanabe", "Tawada",  "Tanaka", "Shirai",    "Bao",  "Oya",    "Oku",     "Kawamura", "Terada", "Atobe", "Sakamoto", "Mastuda", "Takayama",  "Nakamura", "Fukada",  "Yoshimura", "Yachi", "Sato", "Yamashita", "Tano",  "Kataoka", "Hoashi", "Mukasa", "Takasaki", "Wakaizumi", "Kurihara", "Ishizaki", "Takehara", "Nishizawa", "Nozawa", "Yoshimura", "Chiba",   "Endo",   "Kaki",   "Kakehashi", "Kanagawa", "Kitagawa", "Kuromi", "Sato", "Shibata", "Seimiya", "Tamura", "Tsutsui", "Hayakawa", "Hayashi", "Matsuo", "Yakubo", "Yumiki", "Ushio",  "Kageyama", "Kato",  "Saito", "Sasaki", "Sasaki", "Takase", "Takamoto", "Higashimura", "Kanemura", "Kawata", "Kosaka", "Tomita", "Nibu",  "Hamagishi", "Matsuda", "Miyata", "Watanabe", "Kamimura", "Takahashi", "Morimoto", "Yamaguchi"]
first_name = ["Nozomu", "Syuko",    "Masashi", "Shu",    "Tatsuhiko", "Siya", "Masaru", "Daisuke", "Kazushi",  "Kotaro", "Yuta",  "Kazunori", "Yoshiki", "Toshinori", "Yuichi",   "Keisuke", "Tomokazu",  "Yuta",  "Dai",  "Kazuki",    "Shoto", "Kei",     "Yuya",   "Yosuke", "Kazunari", "Tomoya",    "Itsuki",   "Yuta",     "Kota",     "Masato",    "Kohei",  "Natsuhito", "Yoshiki", "Sakura", "Haruka", "Sayaka",    "Saya",     "Yuri",     "Asuka",  "Rika", "Yuna",    "Rei",     "Mayu",   "Ayame",   "Seira",    "Runa",    "Miyu",   "Mio",    "Nao",    "Sarina", "Yuka",     "Shiho", "Kyoko", "Kumi",   "Mirei",  "Mana",   "Ayaka",    "Mei",         "Miku",     "Hina",   "Nao",    "Suzuka", "Akari", "Hiyori",    "Konoka",  "Manamo", "Miho",     "Hinano",   "Mikuni",    "Mari",     "Haruyo"]
name = [""] * num_student
for stu_idx in range(num_student):
    i = np.random.randint(0, len(last_name))
    j = np.random.randint(0, len(first_name))
    name[stu_idx] = last_name[i] + " " + first_name[j]

# 嫌いな人リストを生成
hate = np.zeros((num_hate, num_student), dtype=np.int_)
for i in range(num_hate):
    for stu_idx in range(num_student):
        if hate[i][stu_idx] != 0: # 既に嫌いな人がいたらスルー
            continue
        if np.random.rand() < hate_prob: # 確率満たせば嫌いな人を生成
            while True:
                hate_ppl = np.random.randint(0, num_student)+1 # 嫌いな人を生成
                for k in range(i): # 自分の嫌いな人を調査，同じならやり直し
                    if hate[k][stu_idx] == hate_ppl:
                        continue
                if hate_ppl == stu_idx+1: # もし自分ならやり直し
                    continue
                else:
                    break

            if np.random.rand() < 0.5:      # 半分の確率で一方的に嫌いになる
                hate[i][stu_idx] = hate_ppl
                # print(" one way hate: {} -> {}".format(stu_idx+1, hate_ppl))
            else:                           # 半分の確率でお互い嫌い合う
                hate[i][stu_idx] = hate_ppl
                hate[i][hate_ppl-1] = stu_idx+1
                # print("each way hate: {} <-> {}".format(stu_idx+1, hate_ppl))

df = pd.DataFrame({ "index" : range(1, num_student+1),
                    "name"  : name,
                    "sex"   : [ "M" if np.random.rand() < 0.5 else "F" for _ in range(num_student)],
                    "level" : [ int(np.random.normal(loc=ability_avg, scale=ability_sd, size=None)) for _ in range(num_student) ],
                    "area"  : np.random.randint(1, 6, size=num_student),
                    "hate1" : hate[0],
                    "hate2" : hate[1],
                    "hate3" : hate[2] })

# print(df)
df.to_csv(data_path, index=False)
