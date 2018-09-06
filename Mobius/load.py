import sys
import os
import ttk
import Tkinter as tk
import tkMessageBox
from ttkHyperlinkLabel import HyperlinkLabel
from config import applongname, appversion
import myNotebook as nb
import json
import requests
import zlib
import re
import webbrowser

this = sys.modules[__name__]
this.apiURL = "http://vps583405.ovh.net:3000/api"

MH_VERSION="0.0.1e1"

def plugin_start(plugin_dir):
    check_version()
    return 'Mobius'

def plugin_prefs(parent):
    PADX = 10 # formatting
    frame = nb.Frame(parent)
    frame.columnconfigure(1, weight=1)
    HyperlinkLabel(frame, text='Mobius PVE website', background=nb.Label().cget('background'), url='https://elitepve.com/', underline=True).grid(columnspan=2, padx=PADX, sticky=tk.W)  # Don't translate
    nb.Label(frame, text="Mobius Plug-in - pre-alpha release Version {VER}".format(VER=MH_VERSION)).grid(columnspan=2, padx=PADX, sticky=tk.W)
    nb.Label(frame).grid()  # spacer
    nb.Button(frame, text="UPGRADE", command=upgrade_callback).grid(columnspan=2, padx=PADX, sticky=tk.W)
    return frame

def check_version():
    response = requests.get(this.apiURL + "/version")
    version = json.loads(response.content).get("version")
    if version != MH_VERSION:
        upgrade_callback()
      
def upgrade_callback():
    this_fullpath = os.path.realpath(__file__)
    this_filepath,this_extension = os.path.splitext(this_fullpath)
    corrected_fullpath = this_filepath + ".py" 
    try:
        response = requests.get(this.apiURL + "/download")
        if (response.status_code == 200):
            with open(corrected_fullpath, "wb") as f:
                f.seek(0)
                f.write(response.content)
                f.truncate()
                f.flush()
                os.fsync(f.fileno())
                this.upgrade_applied = True # Latch on upgrade successful
                msginfo = ['Upgrade has completed sucessfully.', 'Please close and restart EDMC']
                tkMessageBox.showinfo("Upgrade status", "\n".join(msginfo))
            sys.stderr.write("Finished plugin upgrade!\n")
            
        else:
            msginfo = ['Upgrade failed. Bad server response', 'Please try again']
            tkMessageBox.showinfo("Upgrade status", "\n".join(msginfo))
    except:
        sys.stderr.write("Upgrade problem when fetching the remote data: {E}\n".format(E=sys.exc_info()[0]))
        msginfo = ['Upgrade encountered a problem.', 'Please try again, and restart if problems persist']
        tkMessageBox.showinfo("Upgrade status", "\n".join(msginfo))

def news_update():
    this.parent.after(300000,news_update)
    try:
        response = requests.get(this.apiURL + "/news")
        updatemsg = json.loads(response.content).get("update").get("update")
        link = json.loads(response.content).get("update").get("link")
        versionmsg = json.loads(response.content).get("update").get("versionmsg")
        motd = json.loads(response.content).get("update").get("motd")
        response = requests.get(this.apiURL + "/listening")
        this.listening = json.loads(response.content)
        if (response.status_code == 200):
            this.news_headline['text'] = updatemsg
            this.news_headline['url'] = link
            statusmsg = "%s%s%s%s" % (versionmsg,this.MH_VERSION," ",motd)
            this.status['text'] = statusmsg
        else:
            this.news_headline['text'] = "News refresh Failed"
    except:
        this.news_headline['text'] = "Could not update news from Mobius server"

def plugin_app(parent):

    this.parent = parent
    this.frame = tk.Frame(parent)
    this.inside_frame = tk.Frame(this.frame)
    this.inside_frame.columnconfigure(4, weight=1)
    label_string = MH_VERSION 
    this.frame.columnconfigure(2, weight=1)
    this.label = HyperlinkLabel(this.frame, text='Mobius:', url='https://elitepve.com/', underline=False)
    this.status = tk.Label(this.frame, anchor=tk.W, text=label_string , wraplengt=200)
    this.news_label = tk.Label(this.frame, anchor=tk.W, text="News:")
    this.news_headline = HyperlinkLabel(this.frame, text="" , wraplengt=200, url="", underline=True)
    this.spacer = tk.Label(this.frame)
    this.label.grid(row = 0, column = 0, sticky=tk.W)
    this.status.grid(row = 0, column = 1, sticky=tk.W)
    this.news_label.grid(row = 1, column = 0, sticky=tk.W)
    this.news_headline.grid(row = 1, column = 1, sticky="ew")
    news_update()
    return this.frame

def dashboard_entry(cmdr, is_beta, entry):
    this.cmdr = cmdr

def journal_entry(cmdr, is_beta, system, station, entry, state):
    this.cmdr = cmdr 
    entry['commandername'] = cmdr
    entry['Mobiusappversion'] = MH_VERSION

    transmit_json = json.dumps(entry)
    for event in this.listening["items"]:
        try:
            x = entry['event']
            eventURL = event[x]
            url_jump = this.apiURL + '/' + eventURL
            headers = {'content-type': 'application/json'}
            response = requests.post(url_jump, data=transmit_json, headers=headers, timeout=7)
            break
        except:
            continue
        
def plugin_stop():
    print "Good bye commander"
