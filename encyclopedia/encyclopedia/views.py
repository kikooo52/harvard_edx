import json
import random as rdm
from django.shortcuts import render
from django.shortcuts import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def detail(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/detail.html", {
            "content": entry, "title": title
        })
    else:
        return render(request, "encyclopedia/404.html", {
            "message": "Page Not Found"
        })


def create(request):
    if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            util.save_entry(title, content)
            return render(request, "encyclopedia/detail.html", {
                "content": content, "title": title
            })
    else:
        return render(request, "encyclopedia/create.html")


def edit(request, title):
    if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            util.save_entry(title, content)
            return render(request, "encyclopedia/detail.html", {
                "content": content, "title": title
            })
    else:
        return render(request, "encyclopedia/edit.html", {
            "content": util.get_entry(title), "title": title
        })


def search_results(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    matching = filter(lambda x: query.lower() in x.lower(), entries)
    return render(request, "encyclopedia/index.html", {
        "entries": matching, "query": query
    })


def random(request):
    entries = util.list_entries()
    rdm_title = rdm.choice(entries)
    return render(request, "encyclopedia/detail.html", {
        "content": util.get_entry(rdm_title), "title": rdm_title
    })


def check_entry(request, title):
    if util.check_entry_exist(title):
        return HttpResponse(json.dumps({'entry_exist': True}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'entry_exist': False}), content_type="application/json")
