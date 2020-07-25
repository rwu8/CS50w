from . import util
from django.shortcuts import render
from django import forms
from markdown2 import Markdown
import random

def index(request):
    # if user is searching for content
    query = request.GET.get('q')
    if query:
        content = util.get_entry(query)

        # found match in our content
        if content:
            return render(request, "encyclopedia/entry.html", {
            "content": content,
            "title": query
        })
        else:
            # get list of all current content
            all_pages = util.list_entries()
            
            # track partial matches
            matches = []

            # loop through each page
            for page in all_pages:
                if query.lower() in page.lower():
                    matches.append(page)

            # no matches found, show error page
            if len(matches) == 0:
                return render(request, "encyclopedia/error.html", {
                    "error": "403",
                    "title": query
                })
            # found some partial matches, display result page for user
            else:
                return render(request, "encyclopedia/result.html", {
                    "matches": matches,
                    "title": query
                })
    
    # display main page
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def entry(request, title):
    # if user is searching for content
    query = request.GET.get('q')
    if query:
        content = util.get_entry(query)

        # found match in our content
        if content:
            return render(request, "encyclopedia/entry.html", {
            "content": content,
            "title": query
        })
        else:
            # get list of all current content
            all_pages = util.list_entries()
            
            # track partial matches
            matches = []

            # loop through each page
            for page in all_pages:
                if query.lower() in page.lower():
                    matches.append(page)

            # no matches found, show error page
            if len(matches) == 0:
                return render(request, "encyclopedia/error.html", {
                    "error": "403",
                    "title": query
                })
            
            # found some partial matches, display result page for user
            else:
                return render(request, "encyclopedia/result.html", {
                    "matches": matches,
                    "title": query
                })
    
    # bring up page user selected
    else:
        content = util.get_entry(title)
        if not content:
            return render(request, "encyclopedia/error.html", {
                "error": "403",
                "title": title
            })
        else:
            return render(request, "encyclopedia/entry.html", {
                "content": Markdown().convert(content),
                "title": title
            })


# class NewPageForm(forms.Form):
#     title = forms.CharField(label="Title")
#     content = forms.CharField(widget=forms.Textarea, label="Content")


def create(request):
    # if user is searching for content
    query = request.GET.get('q')
    if query:
        content = util.get_entry(query)

        # found match in our content
        if content:
            return render(request, "encyclopedia/entry.html", {
            "content": content,
            "title": query
        })
        else:
            # get list of all current content
            all_pages = util.list_entries()
            
            # track partial matches
            matches = []

            # loop through each page
            for page in all_pages:
                if query.lower() in page.lower():
                    matches.append(page)

            # no matches found, show error page
            if len(matches) == 0:
                return render(request, "encyclopedia/error.html", {
                    "error": "403",
                    "title": query
                })
            
            # found some partial matches, display result page for user
            else:
                return render(request, "encyclopedia/result.html", {
                    "matches": matches,
                    "title": query
                })
    
    # bring up create page
    else:
        # Check if method is POST
        if request.method == "POST":
            # print(request.POST)
            title = request.POST["title"]
            content = request.POST["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "error": "duplicate",
                    "title": title
                })
            else:
                util.save_entry(title, content)
                return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries()
                })
        else:
            return render(request, "encyclopedia/create.html", {
        })

def edit_page(request, title):
    # if user is searching for content
    query = request.GET.get('q')
    if query:
        content = util.get_entry(query)

        # found match in our content
        if content:
            return render(request, "encyclopedia/entry.html", {
            "content": content,
            "title": query
        })
        else:
            # get list of all current content
            all_pages = util.list_entries()
            
            # track partial matches
            matches = []

            # loop through each page
            for page in all_pages:
                if query.lower() in page.lower():
                    matches.append(page)

            # no matches found, show error page
            if len(matches) == 0:
                return render(request, "encyclopedia/error.html", {
                    "error": "403",
                    "title": title
                })
            
            # found some partial matches, display result page for user
            else:
                return render(request, "encyclopedia/result.html", {
                    "matches": matches,
                    "title": query
                })
    
    # bring up edit page
    else:
        if request.method == "POST":
            title = request.POST["title"]
            content = request.POST["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })
        else:
            content = util.get_entry(title)
            print(content)
            return render(request, "encyclopedia/edit.html", {
                    "content": content,
                    "title": title
                })



def random_page(request):
    # if user is searching for content
    query = request.GET.get('q')
    if query:
        content = util.get_entry(query)

        # found match in our content
        if content:
            return render(request, "encyclopedia/entry.html", {
            "content": content,
            "title": query
        })
        else:
            # get list of all current content
            all_pages = util.list_entries()
            
            # track partial matches
            matches = []

            # loop through each page
            for page in all_pages:
                if query.lower() in page.lower():
                    matches.append(page)

            # no matches found, show error page
            if len(matches) == 0:
                return render(request, "encyclopedia/error.html", {
                    "error": "403",
                    "title": query
                })
            
            # found some partial matches, display result page for user
            else:
                return render(request, "encyclopedia/result.html", {
                    "matches": matches,
                    "title": query
                })
    
    # bring up a random page
    else:
        # get list of all current content
        all_pages = util.list_entries()
        random_title = random.choice(all_pages)
        content = util.get_entry(random_title)
        return render(request, "encyclopedia/entry.html", {
                    "content": Markdown().convert(content),
                    "title": random_title
                })