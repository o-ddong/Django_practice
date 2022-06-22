from cgitb import html
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

topics = [
    {'id': 0, 'title': "routing", 'body': 'Routing is ...'},
    {'id': 1, 'title': "view", 'body': 'View is ...'},
    {'id': 2, 'title': "Model", 'body': 'Model is ...'},
]

def HTMLTemplate(articleTag):
    global topics
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'

    return HttpResponse(f'''
    <html>
    <body>
        <h1><a href="/">Django</a></h1>
        <ol>
            {ol}
        </ol>
        {articleTag}
    </body>
    <ul>
        <li><a href="/create">create</a></li>
    </ul>
    </html>
    ''')

def index(request):
    article = '''
    <h2>Welcome</h2>
        hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))
    

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic["id"] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article))

@csrf_exempt
def create(request):
    print('request.method', request.method)
    article = '''
        <form action="/create" method="post">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <input type="submit">
        </form>
    '''
    return HttpResponse(HTMLTemplate(article))

