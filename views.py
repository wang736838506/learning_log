from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .forms import TopicForm, EntryForm
from .models import Topic, Entry


# Create your views here.
def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """显示所有类型"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def search_topic(request):
    """按主题名搜索"""
    topic = request.session.get('topic', '')
    search_topic_name = request.GET.get("topic", "")
    topic_list = Topic.objects.filter(text=search_topic_name)
    context = {"topic": topic,
               "topics": topic_list, }

    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """显示单个主题及所有条目"""
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建新表单
        form = TopicForm()
    else:
        # POST提交的数据
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """添加新的条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据：创建新表单
        form = EntryForm()
    else:
        # POST提交数据
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """编辑条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # 未提交数据：创建新表单
        form = EntryForm(instance=entry)
    else:
        # POST提交数据
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
