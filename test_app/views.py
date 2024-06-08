import random
import uuid

from django.http import JsonResponse

from test_app.models import Grade, Student

def grade(request):
    # 增加班级
    if request.method == "POST":
        name = str(uuid.uuid4())[:8]
        number = random.randint(20, 50)
        Grade.objects.create(name=name, number=number)
        return JsonResponse({"msg": "insert grade(%s) success"%(name)})
    # 获取所有班级
    elif request.method == "GET":
        grade_list = Grade.objects.all().values()
        return JsonResponse({"success": True, "grades": list(grade_list)})


def student(request):
    print(request.method)
    # 增加学生
    if request.method == "POST":
        name = str(uuid.uuid4())[:8]
        age = random.randint(15, 25)
        Student.objects.create(name=name, age=age)
        return JsonResponse({"msg": "insert student(%s) success" % (name)})
    # 获取所有学生信息
    elif request.method == "GET":
        print("get student")
        student_list = Student.objects.all().values()
        return JsonResponse({"success": True, "students": list(student_list)})