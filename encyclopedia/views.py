import random

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

from . import util

## --- VIEW ENTRIES ---

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

## --- VIEW ENTRY CONTENT ---

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

## --- SEARCH ENTRIES ---

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


## --- CREATE NEW PAGE ---
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
                duplicateEntry = util.get_entry(title)
# Check for existing entries before saving.
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
        "form": NewPageForm(),
    })


## --- EDIT PAGE ---
class EditPageForm(forms.Form):
    content= forms.CharField(label="Page Content", widget=forms.Textarea())

def edit(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)

        try:
            if form.is_valid():
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(f"/wiki/{title}")
            else:
                raise Exception("Form entry not valid.")

        except Exception as err:
                return render(request, "encyclopedia/edit.html", {
                    "form": form,
                    "title": title,
                    "err": err,
                })

# Default form render for non-POST requests.
    return render(request, "encyclopedia/edit.html", {
        "form": EditPageForm(initial={"content": util.get_entry(title)}),
        "title": title,
    })

## --- RANDOM PAGE ---
def randomPage(request):
    entries = util.list_entries()
    return entry(request, entries[random.randint(0,len(entries)-1)])