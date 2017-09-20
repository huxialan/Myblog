# -*- coding: utf-8 -*-
from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import HttpResponse, Http404
from myweb.models import *
from django.forms.models import model_to_dict
from django.conf import settings
import traceback, json, uuid, os
import math, random, datetime


class MyWeb(object):
    def get_note_menu(self):
        note_sort = []
        new_obj = hf_artile_sort.objects.all()
        for item in new_obj:
            note_sort.append({"text": item.hf_sort_name, "id": item.id})
        return note_sort

    def index(self, request):
        note_sort = self.get_note_menu()
        data = {
            "page": "index",
            "note_sort": note_sort
        }
        return render(request, 'index.html', context=data)

    def life_log(self, request):
        note_sort = self.get_note_menu()
        objs = h_lifelogs.objects.all()
        data = {
            "page": "life_log",
            "objs": objs,
            "note_sort": note_sort
        }
        return render(request, 'life_log.html', data)

    def small_note(self, request):
        note_sort = self.get_note_menu()
        objs = h_smallnotes.objects.all()
        data = {
            "page": "small_note",
            "objs":objs,
            "note_sort": note_sort
        }
        return render(request, 'small_note.html', data)

    def message_board(self, request):
        note_sort = self.get_note_menu()
        fwobjs = h_fwebs.objects.all()
        data = {
            "page": "message_board",
            "note_sort": note_sort,
            "fwobjs":fwobjs
        }
        return render(request, 'message_board.html', data)

    def h5_game(self, request):
        note_sort = self.get_note_menu()
        data = {
            "page": "h5_game",
            "note_sort": note_sort
        }
        return render(request, 'h5_game.html', context=data)

    def font_note(self, request, *args, **kwargs):
        note_sort = self.get_note_menu()
        fwobjs = h_fwebs.objects.all()
        sort = kwargs.get("sort")
        page = kwargs.get("page")
        try:
            sort = int(sort)
            page = int(page)
        except:
            raise Exception("传入参数不正确！")
        if page < 0:
            return render(request, '404.html')
        new_obj = h_frontnotes.objects.filter(hf_artile_cate_id=str(sort)).order_by("-hf_artile_time")[
                  page * 8:(page + 1) * 8]
        count_num = h_frontnotes.objects.filter(hf_artile_cate_id=str(sort)).count()
        page_count = int(math.ceil(float(count_num) / 8))
        if page >= page_count:
            return render(request, '404.html')
        page_active = page + 1
        # page_btm = page_active - 2 if page_active - 2 > 0 else 0
        page_foo = page_active + 2 if page_active + 2 < page_count else page_count
        # page_arr = range(page_btm, page_foo)
        # page_arr = [item + 1 for item in page_arr]

        noteids = []
        frontnotes = []
        for item in new_obj:
            frontnotes_dict = model_to_dict(item)
            frontnotes_dict["artile_date"] = str(item.hf_artile_time)[:19]
            frontnotes.append(frontnotes_dict)
            noteids.append(item.id)

        title_obj = h_frontnotes.objects.filter().order_by("-hf_artile_time")[:5]
        title_number = 1
        title_list = []
        for item in title_obj:
            title_list.append({"number": title_number, "title": item.hf_artile_title, "id": item.id})
            title_number = title_number + 1
        note_comm_objs = hf_artile_comments.objects.filter(note_id__in=noteids).values("note_id").annotate(
            Count('note_id'))
        comm_count = {}
        for item in note_comm_objs:
            comm_count[item["note_id"]] = item["note_id__count"]
        for item in frontnotes:
            if comm_count.has_key(item["id"]):
                item["comm"] = comm_count[item["id"]]
                reading = random.randint(comm_count[item["id"]], comm_count[item["id"]] + 20)
            else:
                item["comm"] = 0
                reading = random.randint(0, 20)
            item["reading"] = reading

        data = {
            "page": "font_note",
            "note_sort": note_sort,
            "frontnotes": frontnotes,
            "title_list": title_list[:5],
            "page_active": page_active,
            # "page_arr": page_arr,
            "sort_id": sort,
            "page_previous": page_active - 2 if page_active - 2 > 0 else 0,
            "page_next": page_active,
            "page_foo": page_foo,
            "fwobjs": fwobjs

        }
        return render(request, 'front_note.html', context=data)

    def login(self, request):
        data = {
            "page": "login"
        }
        return render(request, 'login.html', {'data': data})

    def login_post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/bm_index/')
            else:
                return render(request, 'login.html', {"active_msg": u'账户被禁用'})
        else:
            return render(request, 'login.html', {"psd_msg": u'密码错误'})

    def bm_index(self, request):
        user = request.user
        return render(request, 'bm_index.html', {'user': user})

    def bm_intro(self, request):
        return render(request, 'bm_introduction.html')

    def get_fields(self, all_objs):
        # 动态获取数据表中的定义字段信息
        all_fields = all_objs.model._meta.fields
        all_f_notes_data = []
        show_fields, list_fields = [], []
        for field in all_fields:
            if field.name not in ['hf_artile_img', 'hf_artile_content', 'pic', 'hsn_cate']:
                show_fields.append(field.verbose_name)
                list_fields.append(field.name)

                # 组织数据
        for item in all_objs:
            value_dict = {}
            for field in list_fields:
                value = getattr(item, field)
                if isinstance(value, models.Model):
                    value = str(value)
                elif isinstance(value, (datetime.date, datetime.datetime)):
                    value = str(value)[:19]
                value_dict[field] = value
            all_f_notes_data.append(value_dict)
        return show_fields, list_fields, all_f_notes_data

    # 后台管理

    # 前端笔记
    def bmad_frontn_ma(self, request):
        all_f_notes_objs = h_frontnotes.objects.all().order_by("-id")
        show_fields, list_fields, all_f_notes_data = self.get_fields(all_f_notes_objs)
        content = {
            'title': u'前端笔记管理',
            'data': json.dumps(all_f_notes_data),
            'show_fields': show_fields,
            'list_fields': json.dumps(list_fields),
            'path': request.path
        }
        return render(request, 'bmad_frontn_manage.html', content)

    def bmad_frontn_add(self, request):
        if request.method.lower() == 'get':
            note_sort = hf_artile_sort.objects.all()
            return render(request, 'bmad_front_note.html', {'note_sort': note_sort})
        elif request.method.lower() == 'post':
            pass

    def bmad_frontn_del(self, request, *args, **kwargs):
        id = request.GET.get('id')
        h_frontnotes.objects.filter(id=id).delete()
        return HttpResponse("OK")

    def bmad_frontn_search(self, request):
        value = request.GET.get('data')
        res_obj = h_frontnotes.objects.filter(hf_artile_title__icontains=value)
        show_fields, list_fields, all_f_notes_data = self.get_fields(res_obj)
        return HttpResponse(json.dumps(all_f_notes_data))

    # 前端笔记-------完

    # 生活日志
    def bmad_life_log(self, request):
        all_lifelogs_objs = h_lifelogs.objects.all().order_by("-id")
        show_fields, list_fields, all_lifelogs_data = self.get_fields(all_lifelogs_objs)
        content = {
            'title': u'生活日志管理',
            'data': json.dumps(all_lifelogs_data),
            'show_fields': show_fields,
            'list_fields': json.dumps(list_fields),
            'path': request.path
        }
        return render(request, 'bmad_frontn_manage.html', content)

    def bmad_life_log_search(self, request):
        value = request.GET.get('data')
        res_obj = h_lifelogs.objects.filter(title__icontains=value)
        show_fields, list_fields, all_lifelogs_data = self.get_fields(res_obj)
        return HttpResponse(json.dumps(all_lifelogs_data))

    def bmad_life_log_del(self, request):
        id = request.GET.get('id')
        h_lifelogs.objects.filter(id=id).delete()
        return HttpResponse('OK')

    @csrf_exempt
    def bmad_lifel_add(self, request):
        result = {}
        if request.method.lower() == 'get':
            return render(request, 'bmad_life_logpe.html')
        elif request.method.lower() == 'post':
            user = request.user
            title = request.POST.get("title")
            content = request.POST.get("lifel_htm")
            pic = request.POST.get("pic_path")
            path = "/static/images/company-img-2.jpg" if not pic else pic
            try:
                obj = h_lifelogs.objects.get_or_create(title=title)[0]
                obj.content = content
                obj.pic = path
                obj.save()
                result["sucess"] = u'保存成功'
            except Exception, e:
                result['error'] = u'保存出错'
            finally:
                return HttpResponse(json.dumps(result))

    # 生活日志---完

    # 闲言碎语
    def bmad_smalln(self, request):
        all_smallnotes_objs = h_smallnotes.objects.all().order_by("-id")
        show_fields, list_fields, all_smallnotes_data = self.get_fields(all_smallnotes_objs)
        content = {
            'title': u'闲言碎语管理',
            'data': json.dumps(all_smallnotes_data),
            'show_fields': show_fields,
            'list_fields': json.dumps(list_fields),
            'path': request.path
        }
        return render(request, 'bmad_frontn_manage.html', content)

    def bmad_smalln_search(self, request):
        value = request.GET.get('data')
        res_obj = h_smallnotes.objects.filter(hsn_content__icontains=value)
        show_fields, list_fields, all_smallnotes_data = self.get_fields(res_obj)
        return HttpResponse(json.dumps(all_smallnotes_data))

    def bmad_smalln_del(self, request):
        id = request.GET.get('id')
        h_smallnotes.objects.filter(id=id).delete()
        return HttpResponse("OK")

    @csrf_exempt
    def bmad_smalln_add(self, request):
        result = {}
        if request.method.lower() == 'get':
            return render(request, 'bmad_smalln_pe.html', {'action': 'add'})
        elif request.method.lower() == 'post':
            text_value = request.POST.get('text_value')
            user = request.user
            result = {}
            try:
                h_smallnotes.objects.create(hu=user, hsn_content=text_value)
            except Exception, e:
                result['error'] = u'保存出错'
            finally:
                return HttpResponse(json.dumps(result))

    # 闲言碎语----完



    def save_note(self, request):
        result = {}
        try:
            user = request.user
            note_htm = request.POST.get("note_htm")
            note_txt = request.POST.get("note_txt")
            note_sort = request.POST.get("note_sort")
            title = request.POST.get("title")
            tag = request.POST.get("tag")
            note_path = request.POST.get("image_path")
            path = "/static/images/company-img-1.jpg" if not note_path else note_path
            new_obj = h_frontnotes.objects.get_or_create(hf_artile_title=title, hf_artile_cate_id=note_sort)[0]
            new_obj.hf_artile_content = note_htm
            new_obj.hf_artile_content_txt = note_txt
            new_obj.hf_artile_label = tag if tag else "没有标签"
            new_obj.hf_artile_img = path
            new_obj.save()
            result["sucessful"] = True
        except Exception, e:
            _trackback = traceback.format_exc()
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result['error_msg'] = err_msg
            result['trackback'] = _trackback
        finally:
            return HttpResponse(json.dumps(result))

    def upload_img(self, request):
        result = None
        try:
            action = request.POST.get("action")
            if action == "front_note":
                file_obj = request.FILES.get("file")
            else:
                file_obj = request.FILES.get("wangEditorH5File")
            if not file_obj:
                raise Exception("没有获取到文件对象！")
            if not request.user.is_authenticated():
                raise Exception("登录用户才可以上传文件！")

            user = request.user
            file_name = str(uuid.uuid1()) + "_" + user.username + '.' + str(file_obj.name.split('.')[-1])
            folder = os.path.join(settings.BASE_DIR, "static", "media", "images")
            if not os.path.exists(folder):
                os.makedirs(folder)
            path = os.path.join(folder, file_name)
            # 保存文件
            fobj = open(path, 'wb')
            for ck in file_obj.chunks():
                fobj.write(ck)
            fobj.close()  # 文件保存完毕
            result = "/".join(["", "static", "media", "images", file_name])
        except Exception, e:
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result = "error|" + err_msg
        finally:
            return HttpResponse(result)

    def view_front_note(self, request, *args, **kwargs):
        note_sort = self.get_note_menu()
        id = kwargs.get("id")
        try:
            new_obj = h_frontnotes.objects.get(id=id)
        except:
            return render(request, '404.html')

        title_obj = h_frontnotes.objects.all().order_by("-hf_artile_time")[:5]
        title_list = []
        title_number = 1
        for item in title_obj:
            title_list.append({"number": title_number, "title": item.hf_artile_title, "id": item.id})
            title_number = title_number + 1

        note = {
            "title": new_obj.hf_artile_title,
            "content": new_obj.hf_artile_content,
            "time": str(new_obj.hf_artile_time)[:19],
            "label": new_obj.hf_artile_label,
            "id": new_obj.id
        }
        comments_obj = hf_artile_comments.objects.filter(note_id=new_obj.id)
        comment_list = []
        for item in comments_obj:
            comment_dict = {
                "name": item.name,
                "content": item.content,
                "time": str(item.time)[:19]
            }
            comment_list.append(comment_dict)
        data = {
            "page": "font_note",
            "note_sort": note_sort,
            "note": note,
            "title_list": title_list,
            "comment_list": comment_list
        }
        return render(request, 'front_notede.html', context=data)

    def save_comments(self, request):
        result = {}
        try:
            email = request.POST.get("email")
            text = request.POST.get("text")
            name = request.POST.get("name")
            note = request.POST.get("note")
            email = email.encode("utf8")
            try:
                note = int(note)
            except:
                return render(request, '404.html')
            try:
                new_obj = hf_artile_comments.objects.create(note_id=note, name=name, email=email, content=text)
                result["sucessful"] = True
                result["time"] = str(new_obj.time)[:19]
            except:
                result["sucessful"] = False
        except Exception, e:
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result = "error|" + err_msg
        finally:
            return HttpResponse(json.dumps(result))

    def lifeupload_img(self, request):
        result = None
        try:
            action = request.POST.get("action")
            if action == "life_log":
                file_obj = request.FILES.get("file")
            else:
                file_obj = request.FILES.get("wangEditorH5File")
            if not file_obj:
                raise Exception("没有获取到文件对象！")
            if not request.user.is_authenticated():
                raise Exception("登录用户才可以上传文件！")

            user = request.user
            file_name = str(uuid.uuid1()) + "_" + user.username + '.' + str(file_obj.name.split('.')[-1])
            folder = os.path.join(settings.BASE_DIR, "static", "media", "images")
            if not os.path.exists(folder):
                os.makedirs(folder)
            path = os.path.join(folder, file_name)
            # 保存文件
            fobj = open(path, 'wb')
            for ck in file_obj.chunks():
                fobj.write(ck)
            fobj.close()  # 文件保存完毕
            result = "/".join(["", "static", "media", "images", file_name])
        except Exception, e:
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result = "error|" + err_msg
        finally:
            return HttpResponse(result)

            # 前端笔记编辑

    def bmad_frontn_edit(self, request, *args, **kwargs):
        if request.method == 'GET':
            id = kwargs.get('id')
            obj = h_frontnotes.objects.get(id=id)
            note_sort = hf_artile_sort.objects.all()
            return render(request, 'bmad_front_note.html',
                          {'obj': obj, "action": 'edit/' + id + '/', 'note_sort': note_sort})

    def bmad_lifelog_edit(self, request, *args, **kwargs):
        if request.method == 'GET':
            id = kwargs.get('id')
            obj = h_lifelogs.objects.get(id=id)
            return render(request, 'bmad_life_logpe.html', {'obj': obj, "action": 'edit/' + id + '/'})

    @csrf_exempt
    def bmad_smalln_edit(self, request, *args, **kwargs):
        if request.method == 'GET':
            id = kwargs.get('id')
            obj = h_smallnotes.objects.get(id=id)
            # data = { 'hsn_content':hsn_content }
            return render(request, 'bmad_smalln_pe.html', {'obj': obj, "action": 'edit/' + id + '/'})
        elif request.method == 'POST':
            id = kwargs.get('id')
            text_value = request.POST['text_value']
            result = {}
            try:
                obj = h_smallnotes.objects.get(id=id)
                obj.hsn_content = text_value
                obj.save()
            except Exception:
                result['error'] = u'修改失败'
            finally:
                return HttpResponse(json.dumps(result))
