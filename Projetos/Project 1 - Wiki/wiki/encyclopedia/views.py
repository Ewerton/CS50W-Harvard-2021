from django.shortcuts import render
from django.http import Http404
from django import forms
import markdown2
from random import randrange

from . import util

class SearchForm(forms.Form): # lhs search form
    search = forms.CharField(label='', min_length=3, required=True, 
    widget = forms.TextInput(attrs={'placeholder':'Search the entire encyclopedia:', 'class':'search_input'}))

class TitleForm(forms.Form):
    title = forms.CharField(label='',
    widget = forms.TextInput(attrs={'placeholder':'Enter the title:'}))

class ContentForm(forms.Form):
    content = forms.CharField(label='',
    widget = forms.Textarea(attrs={'placeholder':'Enter the content in the Markdown format:'}))

def index(request):    
    if request.method == "GET": # default page listing the existing entries in the encyclopedia.
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
        })


def search(request):
    page_data = ""
    searchResults = []

    if request.method == "POST": # submited by the search input text...
        form = SearchForm(request.POST)

        if form.is_valid():
            page_data = form.cleaned_data["search"]

            for title in util.list_entries():
                foundExactEntry = page_data.strip().lower() == title.lower()
                if foundExactEntry: 
                    return by_title(request, title) # redirecting the user to the corresponding page (wiki/title)

                foundPotentialEntry = page_data.strip().lower() in title.lower()
                if foundPotentialEntry:
                    searchResults.append(title) # construct a list of possible matchs

        # If no results found, will return an empty list of results, the searchresults.html will handle that scenario
        return render(request, "encyclopedia/searchresults.html", {
            "results":searchResults,
        })
    
    # Any other http method than GET or POST will result in error.
    return render(request, "encyclopedia/notfound.html", {
            "message": "Internal error (Method not Supported)"
    })

# Custom page for specific entry (wiki/title)
def by_title(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/notfound.html", {
                "message": "Requested page was not found"})
    else:
        return render(request, "encyclopedia/entry.html", {
            "title":title.capitalize(),
            "entry":markdown2.markdown(util.get_entry(title)),
        })

def new_entry(request):
    title_form = TitleForm(request.POST)
    content_form = ContentForm(request.POST)

    # Preparing the page for a new entry
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "title": TitleForm(),
            "content": ContentForm()
        })

    # Saving an entry posted by the user
    if request.method == "POST":
        if title_form.is_valid() and content_form.is_valid():
            title = title_form.cleaned_data["title"]
            content = content_form.cleaned_data["content"]

            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/notfound.html", {
                "message": f"There is already an entry in this wiki for the title '{title}' "}) 
            else:
                util.save_entry(title, '#' + title.strip() + '\n' + content)
                return by_title(request, title)
    
    # Any other http method than GET or POST will result in error.
    return render(request, "encyclopedia/notfound.html", {
        "message": "Internal error (Method not Supported)"
    }) 

def edit_entry(request, title):    
    # reading the entry an preparing the form for an edit.
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "editings": ContentForm(initial={'content':content})
        })

    # Saving the user edits.
    else:
        content_form = ContentForm(request.POST)
        if content_form.is_valid():
            content = content_form.cleaned_data["content"]
            util.save_entry(title, content)
            return by_title(request, title)


def random_entry(request):
    index = randrange(len(util.list_entries()))
    return by_title(request, util.list_entries()[index])