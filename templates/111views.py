# coding:utf-8
from django.shortcuts import render, redirect
from .models import Blog
from django.http import HttpResponse
import json
from django.views.generic import CreateView,UpdateView

# Create your views here.
def show(request):
    '''
    响应客户端主页
    '''
    return render(request, 'show.html')

def search(request):
    '''
    搜索数据
    获取客户端发送过来的数据去数据库查询，然后将结果发送给senddata()函数处理发送给客户端
    '''
    name = request.GET['data']
    return senddata(request, Blog.objects.filter(name__icontains=name))


def getdata(request):
    '''
    获取所有数据
    交给senddata()处理发送给客户端
    '''
    return senddata(request, Blog.objects.all())  # 从数据库读取所有的数据


def senddata(request, result):
    '''
    接收客户端发送过来的请求，响应其请求
    :param result:  数据来源
    '''
    index = int(request.GET['index'])  # 从前端拿到的第几页
    pagesize = int(request.GET['pagesize'])  # 从前端拿到的每页显示数目
    length = len(result)
    if (index + 1) * pagesize > len(result):  # 判断是否超出所有的数目，也就是会不会越界
        sendres = result[index * pagesize:]
    else:  # 没有越界的情况
        sendres = result[index * pagesize:(index + 1) * pagesize]
    data = []
    for i in sendres:  # 转换成dict
        data.append({'id': i.id, 'name': i.name, 'tagline': i.tagline})
    senddata = {'data': data, 'page': length}  # 把总条数发送过去
    return HttpResponse(json.dumps(senddata))  # 转换成JSON发送给前端

def create(request):
    name = request.POST.get('name')
    tagline = request.POST.get('tagline')
    Blog.objects.create(name=name,tagline=tagline)
    return HttpResponse(json.dumps({'message':'创建成功！'}))

def delete(request):
    '''
    通过id删除数据
    '''
    id = request.POST['id']
    Blog.objects.get(id=id).delete()
    return HttpResponse('OK')


def modify(request):
    '''
    通过id修改数据
    '''
    id = request.POST['id']
    name = request.POST['name']
    tagline = request.POST['tagline']
    data = Blog.objects.get(id=id)
    data.name = name
    data.tagline = tagline
    data.save()
    return HttpResponse('OK')




class AddBlog(CreateView):
    model = Blog
    fields = ['name', 'tagline']
    template_name = 'AddBlog.html'
