from distutils.log import debug
from flask import Flask, render_template, request, flash, url_for, redirect
import requests
import subprocess
import sys 
from bs4 import BeautifulSoup as soup
# from flaskwebgui import FlaskUI
import json
from os import path
import webbrowser

# app=Flask(__name__,template_folder='templates')
app = Flask(__name__)
# b_path = path.join(path.dirname(__file__), 'Browsor', 'chrome.exe')
# ui = FlaskUI(app)
# ui = FlaskUI(app, start_server='flask')
app.secret_key = "SL"

# global variables
temp_lst = []
t_lst = []
s_lst=[]

# webbrowser.open('http://127.0.0.1:5000/', new=2)

#################################################################################################

# global methods
def _extract(titles, links, _size, _titles_lst, _links_lst, _size_lst, _filter, fil):
    for i in range(len(_filter)):
        fil.append(_filter[i].find("a").contents[0])

    for i in range(len(titles)):
        if((i%2 != 0)):
            _t = titles[i].find_all("a")
            if((len(_t)!=0) and (str(_t[0].get("href"))[:5] == "https")):
                t = len(_titles_lst)
                if(((fil[t] == "Video > HD - Movies") or (fil[t] == "Video > Movies") or (fil[t] == "Video > HD - TV shows") or (fil[t] == "Video > TV shows"))):
                    _titles_lst.append(_t[0].contents[0])

    for i in range(len(links)):
        if(str(links[i].get("href"))[:6] == "magnet"):
            t = len(_links_lst)
            if(((fil[t] == "Video > HD - Movies") or (fil[t] == "Video > Movies") or (fil[t] == "Video > HD - TV shows") or (fil[t] == "Video > TV shows"))):
                _links_lst.append(links[i].get("href"))
    
    for i in range(len(_size)):
        if(((str(_size[i].contents[0])[-3:]) == "GiB") or ((str(_size[i].contents[0])[-3:]) == "MiB") or ((str(_size[i].contents[0])[-3:]) == "KiB")):
            t = len(_size_lst)
            if(((fil[t] == "Video > HD - Movies") or (fil[t] == "Video > Movies") or (fil[t] == "Video > HD - TV shows") or (fil[t] == "Video > TV shows"))):
                _size_lst.append(_size[i].contents[0])

def run_file(magnet_link: str, download: bool):
    if sys.platform.startswith('linux'):
        cmd = []
        cmd.append("webtorrent")
        cmd.append(magnet_link)
        if not download:
            # print('streamming...')
            cmd.append('--vlc')
        subprocess.call(cmd)

    elif sys.platform.startswith('win32'):
        cmd = ""
        cmd= cmd + "webtorrent"
        cmd=cmd+" download "
        cmd=cmd+'"{}"'.format(magnet_link)
        if not download:
            # print('streamming...')
            cmd=cmd+' --vlc'
        subprocess.call(cmd, shell=True)

#################################################################################################

#Routing
@app.route("/", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        if request.form['submit_button'] == "submit_name":
            movie_search = request.form["m_name"]
            return redirect(url_for("name", nm = movie_search))
    else:
        return render_template("search.html")


@app.route("/<nm>/", methods=["POST", "GET"])
def name(nm):
    # con = Console()
    if request.method == "POST":
        if request.form['submit_button1'] == "submit_name1": 
            movie_search = request.form["m_name1"]
            return redirect(url_for("name", nm = movie_search))
    res = requests.get('https://thepiratebay.party/search/'+''.join(nm))
    se=soup(res.text, 'html.parser')
    titles = se.find_all("td")
    links = se.find_all(["nobr" , "a"])
    _size = se.find_all("td", {"align":"right"})
    _filter = se.find_all("td", {"class":"vertTh"})
    _titles_lst = []
    _links_lst = []
    _size_lst = []
    fil = []
    _extract(titles, links, _size, _titles_lst, _links_lst, _size_lst, _filter, fil)
    if len(_links_lst) == 0:
        flash('Sorry, search NOT FOUND :(')
        return redirect(url_for("search"))
    else:
        temp_lst.clear()
        t_lst.clear()
        s_lst.clear()
        _filter.clear()
        for i in range(len(_links_lst)):
            temp_lst.append(_links_lst[i])
            t_lst.append(_titles_lst[i])
            s_lst.append(_size_lst[i])
            _filter.append(fil[i])
        return render_template("disp_tab.html", _titles_lst= _titles_lst, _size_lst = _size_lst, _links_lst=_links_lst, fil = fil, movie_search=nm)
    

@app.route("/<nm>/<string:_id>/", methods = ["POST", "GET"]) 
def get_id(_id, nm):
    _id = json.loads(_id) #<int> type
    lnk = temp_lst[_id-1]
    if request.method == "POST":
        # stream = render_template("streaming.html")
        run_file(lnk, False)
    return render_template("streaming.html")
    # return redirect(url_for("name", nm = nm))

@app.route("/requirement")
def req():
    n_cmd = 'npm install webtorrent-cli -g'
    subprocess.call(n_cmd, shell=True)
    return redirect(url_for("search"))


#Error handlers
@app.errorhandler(404)
def error_404(error):
    return "404", 404


@app.errorhandler(403)
def error_403(error):
    return "200", 403


@app.errorhandler(500)
def error_500(error):
    return "500", 500

#################################################################################################

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
    # ui.run()