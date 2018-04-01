"""定义learning_logs的URL模式"""

from django.conf.urls import url

from learning_logs import views

urlpatterns = [
    # 主页
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    # 主题
    url(r'^topics/$', views.topics, name='topics'),
    # 搜索主题
    url(r'^search_topic/$',views.search_topic,name='search_topic'),
    # 内容
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    # 添加新主题的网页
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    # 添加新条目的网页
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    # 编辑条目的网页
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),

]
