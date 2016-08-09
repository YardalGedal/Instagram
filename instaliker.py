import re, requests, json, random
from tkinter import *
from multiprocessing.dummy import Pool as ThreadPool
global k
k = '0'

def createcookie(proxy):
    return requests.get('https://www.instagram.com/accounts/web_create_ajax/', proxies={'https':proxy.rstrip()})
def login(c, v, proxy):
    v = v.split(":")
    login = v[0]
    pwd = v[1].rstrip()
    return requests.post('https://www.instagram.com/accounts/login/ajax/', headers={'referer': 'https://www.instagram.com/accounts/login', 'x-csrftoken': c.cookies['csrftoken'],
                                  'x-instagram-ajax': '1', 'x-requested-with': 'XMLHttpRequest'}, cookies=c.cookies, data={'username': login, 'password': pwd}, proxies={'https':'http://' + proxy.rstrip()})
def follow(c, id, proxy):
    return requests.post('https://www.instagram.com/web/friendships/' + id + '/follow/', headers={'referer': 'https://www.instagram.com/', 'x-csrftoken': c.cookies['csrftoken'],
                                  'x-instagram-ajax': '1', 'x-requested-with': 'XMLHttpRequest'}, cookies=c.cookies, proxies={'https':'http://' + proxy.rstrip()})
def like(c, id, proxy):
    global link_value
    return requests.post('https://www.instagram.com/web/likes/' + id + '/like/', headers={'referer': link_value.get(), 'x-csrftoken': c.cookies['csrftoken'],
                                  'x-instagram-ajax': '1', 'x-requested-with': 'XMLHttpRequest'}, cookies=c.cookies, proxies={'https':'http://' + proxy.rstrip()})
def comment(c, id, comment_text, proxy):
    return requests.post('https://www.instagram.com/web/comments/' + id + '/add/', headers={'referer': 'https://www.instagram.com/', 'x-csrftoken': c.cookies['csrftoken'],
                                  'x-instagram-ajax': '1', 'x-requested-with': 'XMLHttpRequest'}, data={'comment_text': comment_text}, cookies=c.cookies, proxies={'https':'http://' + proxy.rstrip()})
def follow_n(loginpassword):
    global k, aid
    print(loginpassword)
    print('count: ' + count_value.get())
    print('k: ' + k)
    print('account id: ' + aid)
    try:
        if k < count_value.get():
            proxy = proxylist[random.randrange(0,len(proxylist)-1)]
            print('proxy: ' + proxy)
            cookie = createcookie(proxy)
            l = login(cookie, loginpassword, proxy)
            print('login' + l.text)
            f = follow(l, aid, proxy)
            print('follow' + f.text)
            if json.loads(f.text)["status"] == 'ok':
                k = k + 1
    except:
        pass
def like_n(loginpassword):
    global k, cid
    print(loginpassword)
    print('count: ' + count_value.get())
    print('k: ' + k)
    print('photo id: ' + cid)
    try:
        if k < count_value.get():
            proxy = proxylist[random.randrange(0, len(proxylist) - 1)]
            print('proxy: ' + proxy)
            cookie = createcookie(proxy)
            l = login(cookie, loginpassword, proxy)
            print('login: ' + l.text)
            vlike = like(l, cid, proxy)
            print('like: ' + vlike.text)
            if json.loads(vlike.text)["status"] == 'ok':
                k = k + 1
    except:
        pass
def comment_n(loginpassword):
    global k, cid
    print(loginpassword)
    print('count: ' + count_value.get())
    print('k: ' + k)
    print('photo id: ' + cid)
    try:
        if k < count_value.get():
            proxy = proxylist[random.randrange(0, len(proxylist) - 1)]
            print('proxy: ' + proxy)
            cookie = createcookie(proxy)
            l = login(cookie, loginpassword, proxy)
            print('login: ' + l.text)
            c = comment(l, cid, comments[random.randrange(0,len(comments)-1)], proxy)
            print('comment: ' + c.text)
            if json.loads(c.text)["status"] == 'ok':
                k = k + 1
    except:
        pass
def getaccountid(url):
    str = requests.get(url)
    pattern = re.compile('"owner": {"id": "(\d+)"}')
    return pattern.findall(str.text).pop(0)
def getphotoid(url):
    str = requests.get(url)
    pattern = re.compile('\?id=(\d+)"')
    return pattern.findall(str.text).pop(0)
def formexec():
    root = Tk()
    root.title('InstaFollow')
    root.minsize(width=500, height=150)
    root.maxsize(width=500, height=150)

    #global log_txt
    #log_txt = Text(root, bg="white", fg="black")
    #log_txt.place(x=5, y=150, width=490, height=100)
    #log_scrollbar = Scrollbar(log_txt)
    #log_scrollbar.pack(side=RIGHT, fill=Y)
    #log_txt.config(yscrollcommand=log_scrollbar.set)
    #log_scrollbar.config(command=log_txt.yview)

    imported_proxy_count = len(proxylist)
    proxy_lbl = Label(root, text='Импортировано прокси: ' + str(imported_proxy_count))
    proxy_lbl.place(x=5, y=5)

    imported_logins_count = len(loginlist)
    logins_lbl = Label(root, text='Импортировано логинов: ' + str(imported_logins_count))
    logins_lbl.place(x=5, y=23)

    global count_value
    count_value = StringVar(root)
    count = Entry(root, textvariable=count_value, bg="white", fg="black")
    count.place(x=135, y=60, width=240, height=20)

    global threads_value
    threads_value = StringVar(root)
    threads = Entry(root, textvariable=threads_value, bg="white", fg="black")
    threads.place(x=135, y=90, width=360, height=20)

    global link_value
    link_value = StringVar(root)
    link = Entry(root, textvariable=link_value, bg="white", fg="black", exportselection=0)
    link.place(x=135, y=120, width=360, height=20)

    global type_value
    type_value = StringVar(root)
    type_value.set('Подписчиков')
    ntype = OptionMenu(root, type_value, 'Лайков', 'Комментариев')
    ntype.place(x=365, y=57, width=130, height=25)

    count_lbl = Label(root, text="Нужно")
    count_lbl.place(x=5, y=60)

    threads_lbl = Label(root, text="Количество потоков")
    threads_lbl.place(x=5, y=90)

    link_lbl = Label(root, text="Ссылка")
    link_lbl.place(x=5, y=120)

    logo = PhotoImage(file="instagram_1_.gif")
    start_btn = Button(root, image=logo)
    start_btn.place(x=440, y=2.5)
    start_btn.bind("<Button-1>", start)

    root.mainloop()

def start(self):
    global type_value, threads_value, cid, aid
    pool = ThreadPool(int(threads_value.get()))
    if (type_value.get() == 'Подписчиков'):
        print('followers start')
        aid = getaccountid(link_value.get())
        pool.map_async(follow_n, loginlist)
    if (type_value.get() == 'Лайков'):
        print('likes start')
        cid = getphotoid(link_value.get())
        pool.map_async(like_n, loginlist)
    if (type_value.get() == 'Комментариев'):
        print('comments start')
        cid = getphotoid(link_value.get())
        pool.map_async(comment_n, loginlist)

global proxylist, loginlist, comments
proxylist = open("proxy.txt", "r").readlines()
loginlist = open("logins.txt", "r").readlines()
comments = open("comments.txt", "r").readlines()
formexec()
