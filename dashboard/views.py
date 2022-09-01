import requests
from django.contrib import messages
from django.shortcuts import render,reverse,redirect
import wikipedia
# Create your views here.
from django.views.generic import *
from .forms import NotesForm, HomeworkForm, DashboardForm, TodoForm, UserRegistrationForm
from .models import Notes, Homework, Todo
from youtubesearchpython import VideosSearch


class HomeView(ListView):
    template_name = "dashboard/home.html"

    def get_queryset(self):
        pass

def notesAdd(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            user = request.user
            notes = Notes.objects.create(user=user, title=title, description=description)
            notes.save()
            messages.success(request, f"Notes Added Successfully from {request.user.username}")
            return redirect("dashboard:Notes")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {
        'form' : form,
        'notes': notes,
    }
    return render(request, 'dashboard/notes.html', context)

def deletenote(request, pk=None):
    note = Notes.objects.get(id=pk)
    note.delete()
    return redirect("dashboard:Notes")

class NoteDetailView(DetailView):
    model = Notes

def HomeworkFormView(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            subject = request.POST['subject']
            title = request.POST['title']
            description = request.POST['description']
            due = request.POST['due']
            is_finished = finished
            homework = Homework.objects.create(user=request.user, subject=subject, title=title, description=description,
                                               due=due, is_finished=is_finished)
            homework.save()
            messages.success(request, f"Homework Added Successfully from {request.user.username}")
            return redirect("dashboard:Home_work")
    else:
        form = HomeworkForm()
    homeworks = Homework.objects.filter(user=request.user)
    context ={
        'form' : form,
        'homeworks' : homeworks
    }
    return render(request, 'dashboard/homework.html', context)

def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect("dashboard:Home_work")

def delete_homework(requeat, pk=None):
    homework = Homework.objects.get(id=pk)
    homework.delete()
    return redirect("dashboard:Home_work")

def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],

            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form' : form,
                'results': result_list
            }
        return render(request, 'dashboard/youtube.html',context)
    else:
        form = DashboardForm()
    context = {
        'form': form
    }
    return render(request, "dashboard/youtube.html",context)

def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo.objects.create(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()
            messages.success(request, f"Todo Added from {request.user.username}" )
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    context = {
        'todos': todo,
        'form': form,
    }

    return render(request, "dashboard/todo.html", context)

def todo_delete(request, pk=None):
    todo = Todo.objects.get(id=pk)
    todo.delete()
    return redirect('dashboard:todo')

def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect("dashboard:todo")

def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('count'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink')
            }

            result_list.append(result_dict)
            context = {
                'form' : form,
                'results': result_list
            }
        return render(request, 'dashboard/books.html',context)
    else:
        form = DashboardForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/books.html',context)

def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']

            context = {
                'form' : form,
                'input': text,
                'phonetics' : phonetics,
                'definition' : definition,
                'example': example,
                'synonyms': synonyms,
                'audio': audio,
            }
        except:
            context = {
                'form': form,
                'input': ''
            }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context={'form' : form}
    return render(request, 'dashboard/dictionary.html', context)

def wiki(request):
    if request.method == "POST":
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)

        context = {
            'form': form,
            'title': search.title,
            'link': search.links,
            'details': search.summary
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form
        }
    return render(request, 'dashboard/wiki.html',context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account Created Successfully for {username}")
            return redirect('dashboard:Home')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/register.html', context)


def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)

    context = {
        'homeworks' : homeworks,
        'todos': todos
    }

    return render(request, 'dashboard/profile.html', context)