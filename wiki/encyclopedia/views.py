from django.http.response import HttpResponse
from django.shortcuts import render
import os
import re
from pathlib import Path
from . import util
import encyclopedia
from django.core.files.storage import default_storage
import markdown2
from django import forms, http

class NewPageForm(forms.Form):
    Title = forms.CharField(label='Title', max_length='20', required=True)
    Details = forms.CharField(label='Details',widget=forms.Textarea(attrs={"rows":5, "cols":50}), required=True) # Creating a text field

file_path = "./encyclopedia/templates/encyclopedia/"
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def pages(request, page):
    pages = [entry.lower() for entry in os.listdir(file_path)]
    entries = [entry.lower() for entry in util.list_entries()]
    page = page.lower()
    #page in entries
    if f'{page}.html' in pages:
        return render(request,f'encyclopedia/{page}.html')
    else:
        return render(request, "encyclopedia/error.html")


def search(request):
    search_val  = request.GET['q'] #getting q from the request passed
    list_of_pages =  [entry.lower() for entry in util.list_entries()]
    for i in range(len(list_of_pages)):
        page = os.path.splitext(list_of_pages[i])[0] #getting the page name without the extention
        list_of_pages[i]= page.lower()
    
    return_list = []
    search_val = search_val.lower()

    for pages in list_of_pages:
        if search_val == pages:
            return render(request, f'encyclopedia/{pages}.html')
        elif search_val in pages:
            return_list.append(pages)
    context =  {'result_list':return_list}
    return render(request,"encyclopedia/search.html",context)
    
           
def convert():  
    _, md_files = default_storage.listdir("entries") #upacking the tuple
     
    for file in md_files:
        file = os.path.splitext(file)[0]
        if f'{file}.html' not in os.listdir(file_path):
            details = markdown2.markdown(util.get_entry(file))
            with open(f'{file_path}{file}.html', "w") as f:
                f.write(
                    '{% extends "encyclopedia/layout.html" %}'
                    '{% block title %}'
                        f'{file}'
                    '{% endblock %}'

                    '{% block body %}'
                        f'{details}'
                    '{% endblock %}'
                )
                return True
    return False

def create_new_page(request):
    if request.method == 'GET':
        return render(request,"encyclopedia/New_Page.html",{"form":NewPageForm()})
    else:
        title = request.POST['Title'] #Getting the title from the form
        details = request.POST['Details']
        files = [file.lower() for file in os.listdir(file_path)]
        title = title.lower()
        if f'{title}.html'not in files:
            util.save_entry(title, details)
            if convert():
                return render(request, f'encyclopedia/{title}.html')
        else:
            return render(request, "encyclopedia/page_redirect.html",{"r_page":f'{title}'} )

def edit_entry(request):
    #figure out how to know when a button is pressed on a form
        #do buttons have action?
    # figure out how to populate the form fields
    #figure out the urls
    pass