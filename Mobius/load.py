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

RADIO_URL = "https://radio.forthemug.com/"
STATS_URL = "https://hot.forthemug.com/stats.php"
update_news_url = "http://hot.forthemug.com:4567/news.json/"


MH_VERSION="0.0.0"
REMOTE_VERSION_URL="MOBIUS_VERSION_URL"
REMOTE_PLUGIN_FILE_URL="MOBIUS_UPDATED_FILE_TO_UPGRADE_TO"

this.remote_version = None
this.upgrade_required = None # None for unknown, True for required, False for not
this.network_error_str = "" # Contains human readable network error log
this.upgrade_applied = False

def fetch_remote_version():
    #until mobius servers can provide version number , assume is ok
    this.upgrade_required = False
    try:
        response = requests.get(REMOTE_VERSION_URL, timeout=0.5)
        #sys.stderr.write("response.status_code:%d\n" % response.status_code)
        #sys.stderr.write("response.text:%s\n" % response.text)
        if response.status_code == 200:
            clean_response = response.text.rstrip()
            if len(versiontuple(clean_response)) != 3:
                # Bad format. We need a version number formatted as 1.2.3
                this.network_error_str = "Bad version format reply from server"
                return

            # Store for later
            this.remote_version = clean_response

            #sys.stderr.write("comparing remote version '{REMOTE}' to local version '{LOCAL}'\n".format(REMOTE=this.remote_version, LOCAL=MH_VERSION))
            if MH_VERSION == this.remote_version:
                this.upgrade_required = False
            else:
                this.upgrade_required = True
        else:
            this.network_error_str = "Bad response code {HTTP_RESP_CODE} from server".format(HTTP_RESP_CODE=response.status_code)
    except requests.exceptions.Timeout:
        # sys.stderr.write("requests.exceptions.Timeout\n")
        this.network_error_str = "Request to upgrade URL timed out while finding current version"
    except:
        # sys.stderr.write("generic exception\n")
        this.network_error_str = "Unknown network problem finding current version"

def plugin_start():
    """
    Invoked when EDMC has just loaded the plug-in
    :return: Plug-in name
    """
    # sys.stderr.write("plugin_start\n")	# appears in %TMP%/EDMarketConnector.log in packaged Windows app
    fetch_remote_version() # Fetch remote version information early
    #return 'Mobius Helper'
    return 'Mobius'
	
def plugin_prefs(parent): 
    ##
    ##
    ##Setting frame
    ##
    """
    Invoked whenever a user opens the preferences pane
    Must return a TK Frame for adding to the EDMC settings dialog.
    """
    # sys.stderr.write("plugin_prefs\n")
    PADX = 10 # formatting

    # We need to make another check, as we failed in plugin_start()
    if this.upgrade_required is None:
        fetch_remote_version()

    frame = nb.Frame(parent)
    frame.columnconfigure(1, weight=1)

    HyperlinkLabel(frame, text='Mobius website', background=nb.Label().cget('background'), url='https://elitepve.com/', underline=True).grid(columnspan=2, padx=PADX, sticky=tk.W)	# Don't translate

    nb.Label(frame, text="Mobius Plug-in - Public Version {VER}".format(VER=MH_VERSION)).grid(columnspan=2, padx=PADX, sticky=tk.W)
    nb.Label(frame).grid()	# spacer
    if this.upgrade_required is None:
        nb.Label(frame, text="Attempt to query for a new plug-in version failed:").grid(columnspan=2, padx=PADX, sticky=tk.W)
        nb.Label(frame, text=this.network_error_str, fg="red").grid(columnspan=2, padx=PADX, sticky=tk.W)
    elif this.upgrade_required:
        nb.Label(frame, text="Upgrade required! Hit the button below and restart EDMC").grid(columnspan=2, padx=PADX, sticky=tk.W)
        nb.Label(frame).grid()	# spacer
        nb.Button(frame, text="UPGRADE", command=upgrade_callback).grid(columnspan=2, padx=PADX, sticky=tk.W)
    else:
        nb.Label(frame, text="Fly Safe!").grid(columnspan=2, padx=PADX, sticky=tk.W)
    return frame




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
        url = "http://mobius:3000/api/news"
        tkMessageBox.showinfo("Hutton Influence Data", response)
        response = requests.get(url)
        news_data = response.json()
        #sys.stderr.write("got news!'{HDLN}' and link '{LNK}'\n".format(HDLN=news_data['headline'], LNK=news_data['link']))
        if (response.status_code == 200):
            this.news_headline['text'] = news_data['headline']
            this.news_headline['url'] = news_data['link']
        else:
            this.news_headline['text'] = "News refresh Failed"
    except:
        this.news_headline['text'] = "Could not update news from HH server"

def influence_data_call():
	try:
		url = "http://hot.forthemug.com:4567/msgbox_influence.json"
		response = requests.get(url)
		influence_data = response.json()
		#sys.stderr.write("got news!'{HDLN}' and link '{LNK}'\n".format(HDLN=news_data['headline'], LNK=news_data['link']))
		if (response.status_code == 200):
			tkMessageBox.showinfo("Hutton Influence Data", "\n".join(influence_data))
		else:
			tkMessageBox.showinfo("Hutton Influence Data", "Could not get Influence Data")
	except:
		tkMessageBox.showinfo("Hutton Influence Data", "Did not Receive response from HH Server")

def daily_info_call():
	try:
		url = "http://hot.forthemug.com:4567/msgbox_daily_update.json"
		response = requests.get(url)
		daily_data = response.json()
		#sys.stderr.write("got news!'{HDLN}' and link '{LNK}'\n".format(HDLN=news_data['headline'], LNK=news_data['link']))
		if (response.status_code == 200):
			tkMessageBox.showinfo("Hutton Daily update", "\n".join(daily_data))
		else:
			tkMessageBox.showinfo("Hutton Daily update", "Could not get Daily Update Data")
	except:
		tkMessageBox.showinfo("Hutton Daily update", "Did not Receive response from HH Server")
		
def stats_call():
	try:
		url = "http://hot.forthemug.com:4567/cmdr_stats.json/{}".format(cmdr)
		response = requests.get(url)
		daily_data = response.json()
		#sys.stderr.write("got news!'{HDLN}' and link '{LNK}'\n".format(HDLN=news_data['headline'], LNK=news_data['link']))
		if (response.status_code == 200):
			tkMessageBox.showinfo("Mobius Helper Stats", "\n".join(daily_data))
		else:
			tkMessageBox.showinfo("Mobius Helper Stats", "Could not get Daily Stats Data")
	except:
		tkMessageBox.showinfo("Mobius Helper Stats", "Did not Receive response from HH Server")
	# Something i was playing around with and could'nt get to work
	#if cmdr is None:
	#	return tkMessageBox.showinfo("Stats Information", "Load up your game so we know who to get stats for Commander!")
	#else:
	#	return tkMessageBox.showinfo("Stats Information", "Hello {cmdr} this is a placeholder until i can finish it")

def plugin_app(parent):

   this.parent = parent
   this.frame = tk.Frame(parent)
   this.inside_frame = tk.Frame(this.frame)
   this.inside_frame.columnconfigure(4, weight=1)
   label_string = plugin_status_text()
   

   this.frame.columnconfigure(2, weight=1)
   this.label = HyperlinkLabel(this.frame, text='Mobius:', url='https://elitepve.com/', underline=False)

   this.status = tk.Label(this.frame, anchor=tk.W, text=label_string)
   this.news_label = tk.Label(this.frame, anchor=tk.W, text="News:")
   this.news_headline = HyperlinkLabel(this.frame, text="", url="", underline=True)
   this.daily_button = tk.Button(this.inside_frame, text="Daily Update", command=daily_info_call)
   this.influence_button = tk.Button(this.inside_frame, text="Influence", command=influence_data_call)
   this.stats_button = tk.Button(this.inside_frame, text="Stats", command=lambda: OpenUrl(STATS_URL))
   this.radio_button = tk.Button(this.inside_frame, text="Radio", command=lambda: OpenUrl(RADIO_URL))
   this.spacer = tk.Label(this.frame)
   this.label.grid(row = 0, column = 0, sticky=tk.W)
   this.status.grid(row = 0, column = 1, sticky=tk.W)
   this.news_label.grid(row = 1, column = 0, sticky=tk.W)
   this.news_headline.grid(row = 1, column = 1, sticky=tk.W)
   this.inside_frame.grid(row = 3,column = 0, columnspan= 2,sticky=tk.W)
   #this.spacer.grid(row = 2, column = 0,sticky=tk.W)
   this.daily_button.grid(row = 0, column = 0, sticky =tk.W)
   this.influence_button.grid(row = 0, column = 1, sticky =tk.W, padx = 5,pady= 10)
   this.stats_button.grid(row = 0, column = 2, sticky =tk.W)
   this.radio_button.grid(row = 0, column = 3, sticky =tk.W,padx = 5)

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

    url_jump = 'http://mobius:3000/api/events'
    headers = {'content-type': 'application/json'}
    response = requests.post(url_jump, data=transmit_json, headers=headers, timeout=7)
    message = response.content.replace('{"message":"','').replace('"}','')
        
    this.status['text'] = message



def cmdr_data(data, is_beta):
    """
    Obtained new data from Frontier about our commander, location and ships
    :param data:
    :return:
    """
    if not is_beta:
        cmdr_data.last = data
        #this.status['text'] = "Got new data ({} chars)".format(len(str(data)))
        sys.stderr.write("Got new data ({} chars)\n".format(len(str(data))))
        data2 = json.dumps(data)
        transmit_json = zlib.compress(data2)
        url_transmit_dock = 'http://forthemug.com:4567/docked'
        headers = {'content-type': 'application/octet-stream','content-encoding': 'zlib'}
        response = requests.post(url_transmit_dock, data=transmit_json, headers=headers, timeout=7)
        cmdr_data.last = None
		
def plugin_stop():
	print "Farewell cruel world!"
	

router.get('/news',function(req,res){

        MongoClient.connect('mongodb://127.0.0.1/events', function(err,db) {

        dbo.collection('news').find({},{update:1,_id:0}).sort({timestamp:-1}).limit(1),function (err , result) {
        if (err) throw err;
        res.json({result});
        };
        };

)});


