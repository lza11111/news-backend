from django.http import HttpResponse

def hello(request):
    return HttpResponse("你好呀~ ")