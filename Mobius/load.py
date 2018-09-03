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
this.apiURL = "http://vps583405.ovh.net:3000/api"

MH_VERSION="0.0.1c"


def plugin_start(plugin_dir):
    
    
    
    check_version()
    return 'Mobius'

def plugin_prefs(parent):
    """
    Invoked whenever a user opens the preferences pane
    Must return a TK Frame for adding to the EDMC settings dialog.
    """
    
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
    # sys.stderr.write("You pushed the upgrade button\n")
    
    # Catch upgrade already done once
    
    
    this_fullpath = os.path.realpath(__file__)
    this_filepath,this_extension = os.path.splitext(this_fullpath)
    corrected_fullpath = this_filepath + ".py" # Somehow we might need this to stop it hitting the pyo file?

    # sys.stderr.write("path is %s\n" % this_filepath)
    try:
        response = requests.get(this.apiURL + "/download")
        if (response.status_code == 200):
            # Check our required version number is in the response, otherwise
            # it's probably not our file and should not be trusted
            
            
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

def cmdr_data(data, is_beta):
	"""
	We have new data on our commander
	"""
	this.cmdr = data.get('commander').get('name')
	sys.stderr.write(json.dumps(data))

def news_update():

    this.parent.after(300000,news_update)

    try:

        response = requests.get(this.apiURL + "/news")
                
        updatemsg = json.loads(response.content).get("update").get("update")
             
        #sys.stderr.write("got news!'{HDLN}' and link '{LNK}'\n".format(HDLN=news_data['headline'], LNK=news_data['link']))
        if (response.status_code == 200):
            this.news_headline['text'] = updatemsg
            #this.news_headline['url'] = news_data['link']
        else:
            this.news_headline['text'] = "News refresh Failed"
    except:
        this.news_headline['text'] = "Could not update news from Mobius server"

def callback():
        url_jump = this.apiURL + '/influence'
        headers = {'content-type': 'application/json'}
        transmit_json = {'commander' : this.cmdr ,'INF' : this.Influence.get() , 'Count' : this.Counter.get() }
        sys.stderr.write(transmit_json['INF'])
        sys.stderr.write(transmit_json['commander'])
        sys.stderr.write(transmit_json['Count'])
        tkMessageBox.showinfo("Upgrade status", json.dumps(transmit_json))
        response = requests.post(url_jump, data=transmit_json, headers=headers, timeout=7)

def plugin_app(parent):

	this.parent = parent
	this.frame = tk.Frame(parent)
	this.inside_frame = tk.Frame(this.frame)
	this.inside_frame.columnconfigure(4, weight=1)
	label_string = "Pre-alpha release version:" + MH_VERSION + " not for general use."


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
	sys.stderr.write(json.dumps(entry))

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
try:    
	this.cmdr = cmdr 
	entry['commandername'] = cmdr
	entry['stationname'] = station
	entry['systemname'] = system
	entry['Mobiusappversion'] = MH_VERSION

	compress_json = json.dumps(entry)
	#transmit_json = zlib.compress(compress_json)
	transmit_json = json.dumps(entry)


	if entry['event'] == 'FSDJump':
	    url_jump = this.apiURL + '/events'
	    headers = {'content-type': 'application/json'}
	    response = requests.post(url_jump, data=transmit_json, headers=headers, timeout=7)
	elif entry['event'] == 'MissionAccepted' or entry['event'] =='MissionCompleted':
	    url_jump = this.apiURL + '/events'
	    headers = {'content-type': 'application/json'}
	    response = requests.post(url_jump, data=transmit_json, headers=headers, timeout=7)
except:
    sys.stderr.write("No Commander details, waiting.")	
    
    



        
def plugin_stop():
    print "Farewell cruel world!"
    




