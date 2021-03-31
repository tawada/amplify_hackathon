from amplify import BinaryPoly, BinaryQuadraticModel, gen_symbols, Solver, sum_poly, pair_sum, decode_solution
from amplify.client import FixstarsClient
from amplify.constraint import equal_to
import csv
import time
import os
import copy


# 事後処理
def post(q, values, class_num, student_amount):
    ans = decode_solution(q, values)
    each_amount = [0] * class_num
    for i in range(class_num):                                    # 各クラスの「1」の数
        for j in range(student_amount):
            each_amount[i] += BinaryPoly.count(ans[i][j])
    for j in range(student_amount):
        s = 0
        for i in range(class_num):
            s += BinaryPoly.count(ans[i][j])
        if s == 0:                                                # 全て「0」の場合
            x = each_amount.index(min(each_amount))
            ans[x][j] = 1
            each_amount[x] += 1
        while s > 1:                                              # 複数「1」の場合
            each_amount_one = copy.copy(each_amount)
            for i in range(class_num):
                if ans[i][j] == 0:
                    each_amount_one[i] = 0
            x = each_amount_one.index(max(each_amount_one))
            ans[x][j] = 0
            each_amount[x] -= 1
            s -= 1
    return ans


# 学級分けの評価（五段階評価，h1~h5のscoreとしてs1~s5が対応）
def evaluation(class_num, student_amount, ans_post, sex, gakuryoku, dislike, students):
    # BinaryPolyクラス=>int．
    ans = [[0 for j in range(student_amount)] for i in range(class_num)]  
    for i in range(class_num):
        for j in range(student_amount):
            if ans_post[i][j] == 1:
                ans[i][j] = 1

    # 人数均等化 s1
    each_amount = [0] * class_num
    for i in range(class_num):
        for j in range(student_amount):
            each_amount[i] += ans[i][j]
    student_gap = max(each_amount) - min(each_amount)
    if student_gap >= 5:
        s1 = 1
    elif student_gap == 0:
        s1 = 5
    else:
        s1 = 6 - student_gap

    # 男女均等化 s2
    boy_amount = [0] * class_num
    girl_amount = [0] * class_num
    for j in range(student_amount):
        if sex[i] == 1:
            for i in range(class_num):
                boy_amount[i] += ans[i][j]
        if sex[i] == -1:
            for i in range(class_num):
                girl_amount[i] += ans[i][j]
    boy_gap = max(boy_amount) - min(boy_amount)
    girl_gap = max(girl_amount) - min(girl_amount)
    sex_gap = max(boy_gap, girl_gap)
    if sex_gap >= 5:
        s2 = 1
    elif sex_gap == 0:
        s2 = 5
    else:
        s2 = 6 - sex_gap

    # 学力均等化 s3
    gakuryoku_class = [0] * class_num
    for i in range(class_num):
        k = 0
        for j in range(student_amount):
            gakuryoku_class[i] += gakuryoku[j] * ans[i][j]
        gakuryoku_class[i] /= each_amount[i]
    gakuryoku_gap = max(gakuryoku_class) - min(gakuryoku_class)
    if gakuryoku_gap < 0.025:
        s3 = 5
    elif gakuryoku_gap < 0.05:
        s3 = 4
    elif gakuryoku_gap < 0.075:
        s3 = 3
    elif gakuryoku_gap < 0.1:
        s3 = 2
    else:
        s3 = 1

    # 地域均等化 s4
    areas = []
    for s in students:
        if s.region not in areas:
            areas.append(s.region)
    area_num = len(areas)
    area_amount = [[0 for i in range(class_num)] for k in range(area_num)]
    for i in range(class_num):
        for j in range(student_amount):
            if ans[i][j] == 1:
                area_amount[areas.index(students[j].region)][i] += 1
    area_gap = [0] * area_num
    for k in range(area_num):
        area_gap[k] = max(area_amount[k]) - min(area_amount[k])
    area_gap_ave = sum(area_gap) / len(area_gap)
    if area_gap_ave < 1:
        s4 = 5
    elif area_gap_ave < 2:
        s4 = 4
    elif area_gap_ave < 3:
        s4 = 3
    elif area_gap_ave < 4:
        s4 = 2
    else:
        s4 = 1

    # 好き嫌い勘定 s5
    dislike_sum = 0
    dislike_same = 0
    for j in range(student_amount):
        for k in range(student_amount):
            if dislike[j][k] == 1:
                dislike_sum += 1
                for i in range(class_num):
                    if ans[i][j] != ans[i][k]:
                        break
                    if i == class_num - 1:
                        dislike_same += 1
    dislike_rate = dislike_same / dislike_sum
    if dislike_rate < 0.1:
        s5 = 5
    elif dislike_rate < 0.2:
        s5 = 4
    elif dislike_rate < 0.3:
        s5 = 3
    elif dislike_rate < 0.4:
        s5 = 2
    else:
        s5 = 1

    # print(student_gap)
    # print(sex_gap)
    # print(gakuryoku_gap)
    # print(area_gap_ave)
    # print(dislike_rate)
    return s1, s2, s3, s4, s5


# -----------------------------------[入力]-----------------------------------
def get_input(students, class_num):
    student_amount = len(students)                                                 # 生徒数
    sex = []
    gakuryoku = []
    area = [[0 for j in range(student_amount)] for i in range(student_amount)]
    dislike = [[0 for j in range(student_amount)] for i in range(student_amount)]
    names = [s.name for s in students]
    for i in range(student_amount):
        s = students[i]
        if s.gender == "M":                                                        # 性別
            sex.append(1)
        else:
            sex.append(-1)
        gakuryoku.append(int(s.grade)/100)                                         # 学力（正規化必要？）
        for j in range(student_amount):                                            # 学区域
            t = students[j]
            if s.region == t.region and i != j:
                area[i][j] = 1
        if s.dislikeA != "" and s.dislikeA in names:                               # 嫌いな人
            index = names.index(s.dislikeA)
            dislike[i][names.index(s.dislikeA)] = 1
        if s.dislikeB != "" and s.dislikeB in names:                               # 嫌いな人
            dislike[i][names.index(s.dislikeB)] = 1
        if s.dislikeC != "" and s.dislikeC in names:                               # 嫌いな人
            dislike[i][names.index(s.dislikeC)] = 1
    ave_student_num = int(student_amount // class_num)                             # クラス平均人数
    ave_gakuryoku = sum(gakuryoku) / class_num                                     # 平均学力（クラスの合計学力の平均？）
    return student_amount, sex, gakuryoku, area, dislike, ave_student_num, ave_gakuryoku


# -----------------------------------[定式化]-----------------------------------
def gen_model(class_num, student_amount, sex, gakuryoku, area, dislike, ave_student_num, ave_gakuryoku):
    q = gen_symbols(BinaryPoly, class_num, student_amount)

    # h0はone-hot
    h0 = sum([equal_to(sum_poly([q[i][j] for i in range(class_num)]), 1) for j in range(student_amount)])
    # h1は人数制限
    h1 = sum_poly(class_num, lambda i: (sum_poly(student_amount, lambda j:q[i][j])-ave_student_num)**2)
    # h2は男女均等化
    h2 = sum_poly(class_num, lambda i: (sum_poly(student_amount, lambda j:sex[j]*q[i][j])**2))
    # h3は学力均等化(正規化必須?)
    h3 = sum_poly(class_num, lambda i: (sum_poly(student_amount, lambda j:gakuryoku[j]*q[i][j])-ave_gakuryoku)**2)
    # h4は地域均等化
    h4 = sum_poly(class_num, lambda i: (pair_sum(student_amount, lambda j,k:area[j][k]*q[i][j]*q[i][k])))
    # h5は好き嫌い勘定
    h5 = sum_poly(class_num, lambda i: (pair_sum(student_amount, lambda j,k:dislike[j][k]*q[i][j]*q[i][k])))

    # ハイパーパラメータ
    a1, a2, a3, a4, a5 = 1,1,10,5,20
    a0 = 20
    # Hがエネルギー関数
    H = a1*h1 + a2*h2 + a3*h3 + a4*h4 + a5*h5   # 仕様上 H=h0+h1+h2+h3+h4+h5 はできない模様．h0はBinaryConstraintsクラスで，h1~h5はBinaryPolyクラス．
    H = H + a0*h0                   # 異なるクラスの和をとるとき2つまでしか同時に加算できないと思われる．byTY

    # 論理模型設定
    model = BinaryQuadraticModel(H)
    return model, q


# -----------------------------------[実行]-----------------------------------
def solve(model):
    start = time.time()
    client = FixstarsClient()
    client.token = os.environ.get('AMPLIFY_TOKEN', 'set your token')           # 各自のトークン
    client.parameters.timeout = 100    # タイムアウト[ms]

    solver = Solver(client)
    solver.filter_solution = False       # 制約を満たさない解でも出力させる
    result = solver.solve(model)
    end = time.time()
    return result, end-start
