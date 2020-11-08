from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

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

class NewPageForm(forms.Form):
    title= forms.CharField(label="Page Title")
    content= forms.CharField(label="Page Content", widget=forms.Textarea())

def new(request):

    if request.method == "POST":
        form = NewPageForm(request.POST)

        try:
            if form.is_valid():
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
            
# Check for existing entries before saving.
                duplicateEntry = util.get_entry(title)

                if not duplicateEntry:
                    util.save_entry(title, content)
                    return HttpResponseRedirect(f"/wiki/{title}")
                else:
                    raise Exception(f"Entry {duplicateEntry} already exists.")

            else:
                raise Exception("Form entry not valid.")

        except Exception as err:
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "err": err,
                })

# Default form render for non-POST requests.
    return render(request, "encyclopedia/new.html", {
        "form": NewPageForm()
    })
