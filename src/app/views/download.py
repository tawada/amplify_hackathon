import io
import csv
from app.models.students import Student
from flask import Blueprint, request, make_response

app_download = Blueprint('download', __name__)


@app_download.route('/', methods=['POST'])
def download_view():
    students = Student.get_students(request.form)
    num = len(students)
    result_class = [0] * num
    for i in range(num):
        result_class[i] = request.form.get(f'class{i}')

    outputStream = io.StringIO()
    writer = csv.writer(outputStream)
    writer.writerow(["氏名", "性別", "学力", "居住地", "相性の悪い児童1",
        "相性の悪い児童2", "相性の悪い児童3", "割当クラス"])

    for i in range(num):
        s = students[i]
        writer.writerow([s.name, s.gender, s.grade, s.region, s.dislikeA,
            s.dislikeB, s.dislikeC, result_class[i]])
    CSV_MIMETYPE = 'text/csv'
    response = make_response(b'\xef\xbb\xbf' + outputStream.getvalue().encode("utf_8"))
    downloadFileName = 'download.csv'
    response.headers['Content-Disposition'] = 'attachment; filename=' + downloadFileName
    response.mimetype = CSV_MIMETYPE
    return response
