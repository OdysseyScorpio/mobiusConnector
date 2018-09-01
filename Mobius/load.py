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
this.msg = ""


MH_VERSION="0.0.0"


def plugin_start(plugin_dir):
    """
    Invoked when EDMC has just loaded the plug-in
    :return: Plug-in name
    """
    # sys.stderr.write("plugin_start\n")    # appears in %TMP%/EDMarketConnector.log in packaged Windows app

    #return 'Mobius Helper'
    return 'Mobius'
    


def upgrade_callback():
    # sys.stderr.write("You pushed the upgrade button\n")

    # Catch upgrade already done once
    if this.upgrade_applied:
        msginfo = ['Upgrade already applied', 'Please close and restart EDMC']
        tkMessageBox.showinfo("Upgrade status", "\n".join(msginfo))
        return

    this_fullpath = os.path.realpath(__file__)
    this_filepath,this_extension = os.path.splitext(this_fullpath)
    corrected_fullpath = this_filepath + ".py" # Somehow we might need this to stop it hitting the pyo file?

    # sys.stderr.write("path is %s\n" % this_filepath)
    try:
        response = requests.get(REMOTE_PLUGIN_FILE_URL)
        if (response.status_code == 200):

            # Check our required version number is in the response, otherwise
            # it's probably not our file and should not be trusted
            expected_version_substr="MH_VERSION=\"{REMOTE_VER}\"".format(REMOTE_VER=this.remote_version)
            if expected_version_substr in response.text:
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
                msginfo = ['Upgrade failed. Did not contain the correct version', 'Please try again']
                tkMessageBox.showinfo("Upgrade status", "\n".join(msginfo))
        else:
            msginfo = ['Upgrade failed. Bad server response', 'Please try again']
            tkMessageBox.showinfo("Upgrade status", "\n".join(msginfo))
    except:
        sys.stderr.write("Upgrade problem when fetching the remote data: {E}\n".format(E=sys.exc_info()[0]))
        msginfo = ['Upgrade encountered a problem.', 'Please try again, and restart if problems persist']
        tkMessageBox.showinfo("Upgrade status", "\n".join(msginfo))


def plugin_status_text():
    if this.upgrade_required is None:
        return "Mobius Helper {VER} OK (upgrade status unknown)".format(VER=MH_VERSION)
    elif this.upgrade_required:
        return "Mobius Helper {VER} OLD (Open Settings->HH to upgrade)".format(VER=MH_VERSION)
    else:
        return "Mobius Helper {VER} OK (up-to-date)".format(VER=MH_VERSION)


def versiontuple(v):
    return tuple(map(int, (v.split("."))))
    
def OpenUrl(UrlToOpen):
    webbrowser.open_new(UrlToOpen)

def news_update():

    this.parent.after(300000,news_update)

    try:

        response = requests.get("http://81.152.10.79:3000/api/news")
                
        updatemsg = json.loads(response.content).get("update").get("update")
             
        #sys.stderr.write("got news!'{HDLN}' and link '{LNK}'\n".format(HDLN=news_data['headline'], LNK=news_data['link']))
        if (response.status_code == 200):
            this.news_headline['text'] = updatemsg
            #this.news_headline['url'] = news_data['link']
        else:
            this.news_headline['text'] = "News refresh Failed"
    except:
        this.news_headline['text'] = "Could not update news from Mobius server"


def plugin_app(parent):

   this.parent = parent
   this.frame = tk.Frame(parent)
   this.inside_frame = tk.Frame(this.frame)
   this.inside_frame.columnconfigure(4, weight=1)
   label_string = "Pre-alpha release not for general use."
   

   this.frame.columnconfigure(2, weight=1)
   this.label = HyperlinkLabel(this.frame, text='Mobius:', url='https://elitepve.com/', underline=False)

   this.status = tk.Label(this.frame, anchor=tk.W, text=label_string)
   this.news_label = tk.Label(this.frame, anchor=tk.W, text="News:")
   this.news_headline = HyperlinkLabel(this.frame, text="", url="", underline=True)
      
   this.spacer = tk.Label(this.frame)
   this.label.grid(row = 0, column = 0, sticky=tk.W)
   this.status.grid(row = 0, column = 1, sticky=tk.W)
   this.news_label.grid(row = 1, column = 0, sticky=tk.W)
   this.news_headline.grid(row = 1, column = 1, sticky=tk.W)

   news_update()
   
   return this.frame
   
def journal_entry(cmdr, is_beta, system, station, entry, state):
    """
    E:D client made a journal entry
    :param cmdr: The Cmdr name, or None if not yet known
    :param system: The current system, or None if not yet known
    :param station: The current station, or None if not docked or not yet known
    :param entry: The journal entry as a dictionary
    :param state: A dictionary containing info about the Cmdr, current ship and cargo
    :return:
    """
    entry['commandername'] = cmdr
    entry['stationname'] = station
    entry['systemname'] = system
    entry['Mobiusappversion'] = MH_VERSION

    compress_json = json.dumps(entry)
    #transmit_json = zlib.compress(compress_json)
    transmit_json = json.dumps(entry)


    if entry['event'] == 'FSDJump':
        url_jump = 'http://81.152.10.79:3000/api/events'
        headers = {'content-type': 'application/json'}
        response = requests.post(url_jump, data=transmit_json, headers=headers, timeout=7)
    

        
    



        
def plugin_stop():
    print "Farewell cruel world!"
    

