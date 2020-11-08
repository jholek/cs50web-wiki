from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

    content = util.get_entry(title)

    if content != None:
        return render(request, "encyclopedia/entry.html", {
            "title": f"{title}",
            "content": f"{content}",
     })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": f"{title}",
        })

def search(request):

    query = request.GET.get('q')
    entries = util.list_entries()
    matches = []

    for entry in entries:
        if entry.lower() == query.lower():
            content = util.get_entry(entry)

            return render(request, "encyclopedia/entry.html", {
            "title": f"{entry}",
            "content": f"{content}",
            })
        if query.lower() in entry.lower():
            matches.append(entry)

    return render(request, "encyclopedia/search.html", {
        "query": f"{query}",
        "entries": matches
    })
