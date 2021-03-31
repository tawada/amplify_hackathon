import random

class Student:
    """
    児童を表すクラス
    """
    @classmethod
    def from_args(cls, name: str,
        gender: str, grade: str, region: str,
            dislikeA: str, dislikeB: str, dislikeC: str):
        """
        引数からStudentインスタンスを生成するメソッド
        """
        if name == '': return None
        instance = cls()
        instance.name = name
        if gender == 'M' or gender == 'male' or gender == '男' or gender == '男子':
            instance.gender = 'M'
        else:
            instance.gender = 'F'
        instance.grade = int(grade)
        instance.region = region
        if dislikeA == "0":
            dislikeA = ""
        if dislikeB == "0":
            dislikeB = ""
        if dislikeC == "0":
            dislikeC = ""
        if dislikeA == "" and dislikeC != "":
            dislikeA, dislikeC = dislikeC, dislikeA
        if dislikeA == "" and dislikeB != "":
            dislikeA, dislikeB = dislikeB, dislikeA
        if dislikeB == "" and dislikeC != "":
            dislikeB, dislikeC = dislikeC, dislikeB
        instance.dislikeA = dislikeA
        instance.dislikeB = dislikeB
        instance.dislikeC = dislikeC
        return instance

    @classmethod
    def get_students(cls, data):
        """
        (POSTされた)児童のデータをStudentインスタンスのリストに変換するメソッド
        """
        students = []
        MAX = 1000
        for i in range(MAX):
            if data.get(f'name{i}'):
                students.append(
                    cls.from_args(data.get(f'name{i}'), data.get(f'gender{i}'),
                        data.get(f'grade{i}'), data.get(f'region{i}'),
                            data.get(f'dislikeA{i}'), data.get(f'dislikeB{i}'),
                                data.get(f'dislikeC{i}')))
            else: break
        return students

    @classmethod
    def get_random_students(cls, num):
        """
        ランダムにStudentインスタンスのリストを生成するメソッド
        """
        ability_avg = 50  # 学力の平均
        ability_sd = 10   # 学力の標準偏差
        num_region = 5      # 地域の数
        num_dislike = num -1

        # 氏名のテンプレ
        last_name  = ["Togawa", "Watanabe", "Tawada",  "Tanaka", "Shirai",    "Bao",  "Oya",    "Oku",     "Kawamura", "Terada", "Atobe", "Sakamoto", "Mastuda", "Takayama",  "Nakamura", "Fukada",  "Yoshimura", "Yachi", "Sato", "Yamashita", "Tano",  "Kataoka", "Hoashi", "Mukasa", "Takasaki", "Wakaizumi", "Kurihara", "Ishizaki", "Takehara", "Nishizawa", "Nozawa", "Yoshimura", "Chiba",   "Endo",   "Kaki",   "Kakehashi", "Kanagawa", "Kitagawa", "Kuromi", "Sato", "Shibata", "Seimiya", "Tamura", "Tsutsui", "Hayakawa", "Hayashi", "Matsuo", "Yakubo", "Yumiki", "Ushio",  "Kageyama", "Kato",  "Saito", "Sasaki", "Sasaki", "Takase", "Takamoto", "Higashimura", "Kanemura", "Kawata", "Kosaka", "Tomita", "Nibu",  "Hamagishi", "Matsuda", "Miyata", "Watanabe", "Kamimura", "Takahashi", "Morimoto", "Yamaguchi"]
        first_name = ["Nozomu", "Syuko",    "Masashi", "Shu",    "Tatsuhiko", "Siya", "Masaru", "Daisuke", "Kazushi",  "Kotaro", "Yuta",  "Kazunori", "Yoshiki", "Toshinori", "Yuichi",   "Keisuke", "Tomokazu",  "Yuta",  "Dai",  "Kazuki",    "Shoto", "Kei",     "Yuya",   "Yosuke", "Kazunari", "Tomoya",    "Itsuki",   "Yuta",     "Kota",     "Masato",    "Kohei",  "Natsuhito", "Yoshiki", "Sakura", "Haruka", "Sayaka",    "Saya",     "Yuri",     "Asuka",  "Rika", "Yuna",    "Rei",     "Mayu",   "Ayame",   "Seira",    "Runa",    "Miyu",   "Mio",    "Nao",    "Sarina", "Yuka",     "Shiho", "Kyoko", "Kumi",   "Mirei",  "Mana",   "Ayaka",    "Mei",         "Miku",     "Hina",   "Nao",    "Suzuka", "Akari", "Hiyori",    "Konoka",  "Manamo", "Miho",     "Hinano",   "Mikuni",    "Mari",     "Haruyo"]
        genders = ['M', 'F']
        regions = [f'地域{r+1}' for r in range(num_region)]
        students = []
        for _ in range(num):
            students.append(cls.from_args(
                random.choice(last_name) + " " + random.choice(first_name),
                    random.choice(genders), int(random.normalvariate(mu=ability_avg,
                        sigma=ability_sd)), random.choice(regions), "", "", ""))
        for _ in range(num_dislike):
            s = random.randrange(num)
            h = random.randrange(num-1)
            if h >= s:
                h += 1  # hとsの重複をなくしている

            if (students[s].dislikeA == students[h].name or
                students[s].dislikeB == students[h].name or
                    students[s].dislikeC == students[h].name):
                pass
            elif students[s].dislikeA == "":
                students[s].dislikeA = students[h].name
            elif students[s].dislikeB == "":
                students[s].dislikeB = students[h].name
            elif students[s].dislikeC == "":
                students[s].dislikeC = students[h].name

        return students
