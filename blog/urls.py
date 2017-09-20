# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin
import myweb.views

myweb_view = myweb.views.MyWeb()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', myweb_view.index),
    url(r'^life_log/$', myweb_view.life_log),
    url(r'^small_note/$', myweb_view.small_note),
    url(r'^message_board/', myweb_view.message_board),
    url(r'^h5_game/', myweb_view.h5_game),
    url(r'^font_note/(?P<sort>\w+)/(?P<page>\w+)/$', myweb_view.font_note),
    url(r'^login/$', myweb_view.login),
    url(r'^login_post/$', myweb_view.login_post),
    url(r'^bm_index/$', myweb_view.bm_index),
    url(r'^bm_index/bm_intro/$', myweb_view.bm_intro),
    url(r'^bmad_frontn_ma/$', myweb_view.bmad_frontn_ma),
    url(r'^bmad_frontn_ma/add', myweb_view.bmad_frontn_add),
    url(r'^bmad_frontn_ma/del', myweb_view.bmad_frontn_del),
    url(r'^bmad_frontn_ma/edit/(?P<id>\w+)/$', myweb_view.bmad_frontn_edit),
    url(r'^bmad_frontn_ma/search', myweb_view.bmad_frontn_search),
    url(r'^bmad_life_log/$', myweb_view.bmad_life_log),
    url(r'^bmad_life_log/search', myweb_view.bmad_life_log_search),
    url(r'^bmad_life_log/del', myweb_view.bmad_life_log_del),
    url(r'^bmad_life_log/add', myweb_view.bmad_lifel_add),
    url(r'^bmad_life_log/edit/(?P<id>\w+)/$', myweb_view.bmad_lifelog_edit),
    url(r'^bmad_smalln/$', myweb_view.bmad_smalln),
    url(r'^bmad_smalln/search', myweb_view.bmad_smalln_search),
    url(r'^bmad_smalln/del', myweb_view.bmad_smalln_del),
    url(r'^bmad_smalln/add', myweb_view.bmad_smalln_add),
    url(r'^bmad_smalln/edit/(?P<id>\w+)/$', myweb_view.bmad_smalln_edit),
    url(r'^save_note/$', myweb_view.save_note),
    url(r'^upload_img/$', myweb_view.upload_img),
    url(r'^lifeupload_img', myweb_view.lifeupload_img),
    url(r'^view/(?P<id>\w+)/$', myweb_view.view_front_note),
    url(r'^save_comments/$', myweb_view.save_comments)
]
