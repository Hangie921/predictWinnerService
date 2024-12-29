from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import MyModel
import json

def index(request):
    return render(request, 'index.html')

def localhost_only(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.META['REMOTE_ADDR'] != '127.0.0.1':
            return HttpResponseForbidden("Access denied")
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

@localhost_only
def get_resource(request):
    if request.method == 'GET':
        data = list(MyModel.objects.all().values())
        return JsonResponse(data, safe=False)

@csrf_exempt
@localhost_only
def post_resource(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_item = MyModel.objects.create(**data)
        return JsonResponse({"message": "POST request received", "data": new_item.id})

@csrf_exempt
@localhost_only
def put_resource(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        item = MyModel.objects.get(id=data['id'])
        for key, value in data.items():
            setattr(item, key, value)
        item.save()
        return JsonResponse({"message": "PUT request received", "data": item.id})

@csrf_exempt
@localhost_only
def delete_resource(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        item = MyModel.objects.get(id=data['id'])
        item.delete()
        return JsonResponse({"message": "DELETE request received"})