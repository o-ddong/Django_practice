from cgitb import html
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

nextId = 4
topics = [
    {'id': 0, 'title': "routing", 'body': 'Routing is ...'},
    {'id': 1, 'title': "view", 'body': 'View is ...'},
    {'id': 2, 'title': "Model", 'body': 'Model is ...'},
]

def HTMLTemplate(articleTag, id=None):
    global topics
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li>
                <form action="/delete" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
            <li><a href="/update/{id}">update</a></li>
        '''
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
        <ul>
            <li><a href="/create">create</a></li>
            {contextUI}
        </ul>
    </body>
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
    return HttpResponse(HTMLTemplate(article, id))

@csrf_exempt
def create(request):
    global nextId
    # print('request.method', request.method)
    # print('request.method', type(request.method))

    if request.method == 'GET': # GET 일 때
        article = '''
        <form action="/create" method="post">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <input type="submit">
        </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == 'POST': # POST 일 때
        # print(request.POST)

        title = request.POST["title"]
        body = request.POST["body"]
        newTopic = {"id": nextId, "title": title, "body": body}
        topics.append(newTopic)
        url = "read/" + str(nextId)
        nextId += 1
        return redirect(url)
        # return HttpResponse(HTMLTemplate(article))

@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        newTopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics
        print('id', id)
    return redirect('/')

# Get으로 받은 데이터를 자기 자신에게 POST로 전달해서 값 처리 해주고 Read로 전달
@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = {
                    "title": topic['title'],
                    "body": topic['body']
                }
        article = f'''
            <form action="/update/{id}/" method="post">
                <p><input type="text" name="title" value="{selectedTopic['title']}"></p>
                <p><textarea name="body">{selectedTopic['body']}</textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article, id))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body

        return redirect(f'/read/{id}')