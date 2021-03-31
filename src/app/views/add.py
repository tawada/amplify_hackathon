import io
import csv
import chardet
from flask import Blueprint, render_template, request, flash

from app.models.students import Student


app_add = Blueprint('add', __name__)


@app_add.route('/random', methods=['POST'])
def add_random_view():
    students = Student.get_students(request.form)
    num = int(request.form.get('num_add_random'))
    if num > 0:
        students_add = Student.get_random_students(num)
        students.extend(students_add)
        flash(f'ランダムに児童を{num}名追加しました', "success")
    else:
        flash('児童を追加できませんでした', "failed")
    return render_template('index.html', students=students)


@app_add.route('/one', methods=['POST'])
def add_one_view():
    students = Student.get_students(request.form)
    student_add = Student.from_args(request.form.get('nameX'),
        request.form.get('genderX'), request.form.get('gradeX'),
            request.form.get('regionX'), request.form.get('dislikeAX'),
                request.form.get('dislikeBX'), request.form.get('dislikeCX'))
    if student_add:
        students.append(student_add)
        flash('児童を1名追加しました', "success")
    else:
        flash('児童を追加できませんでした', "failed")
    return render_template('index.html', students=students)


@app_add.route('/file', methods=['POST'])
def add_file_view():
    students = Student.get_students(request.form)
    try:
        data = request.files.get('file').stream.read()
        encode = chardet.detect(data)["encoding"]
        sio = io.StringIO(data.decode(encode))
        reader = csv.reader(sio)
        next(reader)  # 最初の行をスキップ
        students_add = []
        for row in reader:
            students_add.append(Student.from_args(row[1], row[2],
                row[3], '地域'+row[4], row[5], row[6], row[7]))
        num = len(students_add)
        for i in range(num):
            if students_add[i].dislikeA != "":
                students_add[i].dislikeA = students_add[int(students_add[i].dislikeA)-1].name
            if students_add[i].dislikeB != "":
                students_add[i].dislikeB = students_add[int(students_add[i].dislikeB)-1].name
            if students_add[i].dislikeC != "":
                students_add[i].dislikeC = students_add[int(students_add[i].dislikeC)-1].name
    except:
        flash('ファイルが読み取れませんでした', "failed")
    else:
        students.extend(students_add)
        flash(f'児童を{num}名追加しました', "success")
    return render_template('index.html', students=students)


