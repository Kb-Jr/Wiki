from django.shortcuts import render, redirect
from django.core.files import File

from . import util
from . import forms

from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# To check if entry exists in list of entries
# if the name of the entry exists in the list of entries, render the entries html page else display the errors page
def entry(request, name):
    if name.upper() in (name.upper() for name in util.list_entries()):
        context = {"name": name, 
        "markdown": util.to_html(util.get_entry(name))}

        return render(request, "encyclopedia/entries.html",context)
    else:
        context = {"error": "entry does not exist"}
        return render(request, "encyclopedia/errors.html", context)


def search(request):
    searched = request.GET['q']
    if searched.upper() in (name.upper() for name in util.list_entries()):
        return redirect("entry", name=searched)
    else:
        searchResults = [i for i in util.list_entries() if searched.upper() in i.upper()]
        context = {"searchResults":searchResults}
        return render(request, "encyclopedia/search.html", context)


def newPage(request):
    if request.method == "POST":
        form = forms.EntryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['entry_name']
            content = form.cleaned_data['entry_content']
            if name.upper() in (x.upper() for x in util.list_entries()):
                context = {"error": "entry already exists!"}
                return render(request, "encyclopedia/errors.html", context)
            else:
                with open(f'entries/{name}.md', 'w') as f:
                    file=File(f)
                    file.write(content)
                return redirect("entry", name=name)
           
    else:
        form = forms.EntryForm()
        context = {"form":form}
    return render (request, "encyclopedia/newPage.html", context)


def editEntry(request, name):
    if request.method == "POST":
        form = forms.EditForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data['entry_content']
        with open (f'entries/{name}.md', 'w') as f:
            file = File(f)
            file.write(new_content)
        return redirect("entry", name=name)
    else:
        existing_content = util.get_entry(name)
       
        form = forms.EditForm({'entry_content': existing_content})
        context = {'form':form, 'name':name}
        return render(request, 'encyclopedia/editEntry.html', context)

def randomEntry(request):
    random = choice(util.list_entries())
    return redirect ("entry", name=random)





