from main.main import get_input,gen_model, solve, post, evaluation
from app.models.students import Student
from flask import Blueprint, render_template, request, flash, redirect, url_for

app_solve = Blueprint('solve', __name__)


@app_solve.route('/', methods=['POST'])
def solve_view():
    students = Student.get_students(request.form)
    if len(students) == 0:
        flash("リストは空です", "failed")
        return redirect(url_for('index'))

    num_class = int(request.form.get('num_class'))

    student_amount, sex, gakuryoku, area, dislike, ave_student_num, ave_gakuryoku = get_input(students, num_class)
    model, q = gen_model(num_class, student_amount, sex, gakuryoku, area, dislike, ave_student_num, ave_gakuryoku)

    try:
        result, time = solve(model)
    except:
        flash("イジングマシンの実行に失敗しました", "failed")
        return render_template('index.html', students=students)

    ans_post = post(q, result[0].values, num_class, student_amount)
    score = evaluation(num_class, student_amount, ans_post, sex, gakuryoku, dislike, students)

    result_class = [0] * student_amount
    for i in range(student_amount):
        for j in range(num_class):
            if ans_post[j][i] == 1:
                result_class[i] = f'クラス{j+1}'
                break

    return render_template('solve/index.html', students=students,
        result=result_class, score=score, num_class=num_class)
