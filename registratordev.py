import requests, json, random, ctypes
from tkinter import *
from multiprocessing import Pool
from os import listdir
def createcookie(proxy = 0):
    return requests.get('https://www.instagram.com/accounts/web_create_ajax/', headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2791.0 Safari/537.36'}, proxies=proxy)
def register(c,login,password,proxy = 0):
    return requests.post('https://www.instagram.com/accounts/web_create_ajax/', headers = {'referer':'https://www.instagram.com/', 'x-csrftoken':c.cookies['csrftoken'], 'x-instagram-ajax': '1', 'x-requested-with': 'XMLHttpRequest', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2791.0 Safari/537.36'}, cookies = c.cookies, data = {'email':login+'@gmail.com', 'password':password, 'username':login, 'fullName':login}, proxies=proxy)
def available(c,login,password, proxy=0):
    return requests.post('https://www.instagram.com/accounts/web_create_ajax/attempt/', headers = {'referer':'https://www.instagram.com/', 'x-csrftoken':c.cookies['csrftoken'], 'x-instagram-ajax': '1', 'x-requested-with': 'XMLHttpRequest', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2791.0 Safari/537.36'}, cookies = c.cookies, data = {'email':login+'@gmail.com', 'password':password, 'username':login, 'first_name':login}, proxies=proxy)
def uploadphoto(c,photo, proxy = 0):
    files = {'profile_pic': (photo, open('avatars/'+photo, 'rb'), 'image/jpeg')}
    return requests.post('https://www.instagram.com/accounts/web_change_profile_picture/', headers={'referer': 'https://www.instagram.com/', 'origin': 'https://www.instagram.com/', 'x-csrftoken':c.cookies['csrftoken'], 'x-instagram-ajax': '1', 'x-requested-with': 'XMLHttpRequest', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2791.0 Safari/537.36'}, cookies=c.cookies, files=files, proxies=proxy)
def userinfo(c,login,phone_number,bio,gender,external_url, proxy = 0):
    return requests.post('https://www.instagram.com/accounts/edit/',
                         headers={'referer': 'https://www.instagram.com/', 'x-csrftoken': c.cookies['csrftoken'],
                                  'x-instagram-ajax': '1', 'x-requested-with': 'XMLHttpRequest', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2791.0 Safari/537.36'}, cookies=c.cookies,
                         data={'first_name': login, 'email': login +'@gmail.com', 'username': login,
                               'phone_number': phone_number, 'gender': gender, 'biography': bio, 'external_url': external_url, 'chaining_enable': 'on'}, proxies=proxy)
def login_gen(loginlist):
    m = len(loginlist)
    line = loginlist[random.randrange(0, m - 1)]
    line = line.split(":")
    return line
 
loginlist = open("login.txt", "r").readlines()
photolist = listdir('avatars')
forgender = {'Мужской': '1', 'Женский': '2', 'Не указано':'3'}
 
def nf(proxy):
    try:
        global loginlist
        lp = login_gen(loginlist)
        login = lp[0]
        password = lp[1].rstrip()
        cookie = createcookie({'https':proxy.rstrip()})
        available_r = available(cookie,login,password, {'https':proxy.rstrip()})
        
        try:
            login = json.loads(available_r.text)['username_suggestions'][0]
        except:
            pass
        
        r = register(available_r,login,password,{'https':proxy.rstrip()})
        print('Account registration attempt ' + login + ':' + password + ' with proxy ' + proxy.rstrip() + '\n availability: ' + str(json.loads(available_r.text)) + '\n response: ' + str(json.loads(r.text)) + '\n')
        jsonlr = json.loads(r.text)
        invalid_txt.insert(END, proxy + ' | '+ str(jsonlr))
        if jsonlr['account_created'] == True:
            valids = open("valids.txt", "a")
            valid_txt.insert(END, login + ':' + password + '\n')
            valids.write(login + ':' + password + '\n')
            valids.close()
            global photolist
            u = userinfo(r, login, i_p_n.get(), bio.get(), forgender[gender_v.get()], e_u.get(), {'https':proxy.rstrip()})
            print(u.text)
            photo = photolist[random.randrange(0, len(photolist) - 1)]
            p = uploadphoto(u, photo, {'https':proxy.rstrip()})
            print('p ' + p.text)
    except:
        pass
 
 
proxylist = open("proxy.txt", "r").readlines()
global root
root = Tk()
root.title('Авторегистратор аккаунтов в инстаграме')
root.minsize(width=1000,height=400)
root.maxsize(width=1000,height=400)
 
def buttonreg(event):
    pool = Pool(int(cthreads.get()))
    pool.map_async(nf, proxylist, callback=ctypes.windll.user32.MessageBoxW(None,"Выполнение завершено","Регистратор",0x40 | 0x0))
    pool.close()

invalid_txt = Listbox(root, bg="white", fg="black")
valid_txt = Text(root, bg="white", fg="black")
invalid_lbl = Label(root, text="Лог работы:")
valid_lbl = Label(root, text="Успешные регистрации:")
 
i_p_n = StringVar(root)
info_phone_number = Entry(root, textvariable = i_p_n, bg="white", fg="black")
info_phone_number.pack()
info_phone_number.place(x=850, y=1, width=150, height=20)
 
phone_lbl = Label(root, text="Номер телефона:")
phone_lbl.pack()
phone_lbl.place(x=745, y=1)
 
cthreads = StringVar(root)
cthreads_txt = Entry(root, textvariable=cthreads, bg="white", fg="black")
cthreads_txt.insert(0, '5')
cthreads_txt.pack()
cthreads_txt.place(x=250, y=1, width=23, height=20)
 
cthreads_lbl = Label(root, text="Количество потоков: ")
cthreads_lbl.pack()
cthreads_lbl.place(x=125, y=1)
 
logo = PhotoImage(file="insta108.gif")
start_btn = Button(root, image=logo)
start_btn.place(x=5, y=1, heigh=68)
start_btn.bind("<Button-1>", buttonreg)
 
e_u = StringVar(root)
external_url = Entry(root, textvariable = e_u, bg="white", fg="black")
external_url.pack()
external_url.place(x=850, y=50, width=150, height=20)
 
eu_lbl = Label(root, text="Личный сайт:")
eu_lbl.pack()
eu_lbl.place(x=745, y=49)
 
gender_v = StringVar(root)
gender_v.set('Не указано')
gender = OptionMenu(root, gender_v, 'Мужской', 'Женский')
gender.pack()
gender.place(x=850, y=20, width=150, height=30)
 
gender_lbl = Label(root, text="Гендер:")
gender_lbl.pack()
gender_lbl.place(x=745, y=25)
 
bio = StringVar(root)
biography = Entry(root, textvariable = bio, bg="white", fg="black")
biography.pack()
biography.place(x=475, y=25, width=250, height=45)
 
bio_lbl = StringVar(root)
biography = Label(root, text="О себе:")
biography.pack()
biography.place(x=575, y=1)
 
valid_lbl.pack()
valid_lbl.place(x=510, y=65)
 
imported_proxy_count = len(proxylist)
proxy_lbl = Label(root, text='Импортировано прокси: ' + str(imported_proxy_count))
proxy_lbl.pack()
proxy_lbl.place(x=125, y=40)
 
imported_logins_count = len(loginlist)
logins_lbl = Label(root, text='Импортировано логинов: ' + str(imported_logins_count))
logins_lbl.place(x=125, y=60)
 
validslist = open("valids.txt","r").readlines()
imported_valids_count = len(validslist)
valids_lbl = Label(root, text='Всего аккаунтов зарегистрировано: ' + str(imported_valids_count))
valids_lbl.place(x=125, y=20)
 
invalid_lbl.pack()
invalid_lbl.place(x=10, y=65)
 
invalid_txt.pack()
invalid_txt.place(x=5, y=85, width=495, height=300)
 
valid_txt.pack()
valid_txt.place(x=500, y=85, width=495, height=300)
 
 
invalid_scrollbar = Scrollbar(invalid_txt)
invalid_scrollbar.pack(side=RIGHT, fill=Y)
invalid_txt.config(yscrollcommand=invalid_scrollbar.set)
invalid_scrollbar.config(command=invalid_txt.yview)
 
valid_scrollbar = Scrollbar(valid_txt)
valid_scrollbar.pack(side=RIGHT, fill=Y)
valid_txt.config(yscrollcommand=valid_scrollbar.set)
valid_scrollbar.config(command=valid_txt.yview)
 
gui = Pool(1)
gui.map_async(root.mainloop())
