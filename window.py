import os, re, sys, time
from subprocess import PIPE, Popen
import platform

os_platform = platform.system()
if(os_platform == 'Windows'):
    from win32gui import GetWindowText, GetForegroundWindow
    microsoft_windows_list = ['Microsoft Teams', 'Prompt','Outlook','Google Chrome','Task Switching','Visual Studio Code','Word','Skype']
    microsft_chrome_list = ['Google Calendar']

window_dictionary = {'Nautilus':'File Manager','X-terminal-emulator':'Terminal','Code':'Visual Studio','Google-chrome':'Google-Chrome'}
websites_dictionary = {'Overleaf, Editor de LaTeX online ':'Overleaf','Buscar con Google ':'Google Search','gmail.com ':'Gmail','Google Chrome':'Other','Overleaf':'Overleaf','Stack Overflow':'Stack Overflow'}
linux_chrome_list = ['Buscar con Google ', 'Overleaf','gmail.com ','Stack Overflow']

def get_current_window():
    if('Windows'==os_platform):
        return GetWindowText(GetForegroundWindow())
    else:
        root = Popen( ['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout = PIPE )
        stdout, stderr = root.communicate()
        m = re.search( b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout )

        if m is not None:

            window_id   = m.group( 1 )

            windowname  = None
            window = Popen( ['xprop', '-id', window_id, 'WM_NAME'], stdout = PIPE )
            stdout, stderr = window.communicate()
            wmatch = re.match( b'WM_NAME\(\w+\) = (?P<name>.+)$', stdout )
            if wmatch is not None:
                windowname = wmatch.group( 'name' ).decode( 'UTF-8' ).strip( '"' )

            processname1, processname2 = None, None
            process = Popen( ['xprop', '-id', window_id, 'WM_CLASS'], stdout = PIPE )
            stdout, stderr = process.communicate()
            pmatch = re.match( b'WM_CLASS\(\w+\) = (?P<name>.+)$', stdout )
            if pmatch is not None:
                processname1, processname2 = pmatch.group( 'name' ).decode( 'UTF-8' ).split( ', ' )
                processname1 = processname1.strip( '"' )
                processname2 = processname2.strip( '"' )

            try:
                processname2 = window_dictionary[processname2]
            except:
                window_dictionary[processname2] = processname2
        
            return processname2, windowname

        return None

def get_chrome_website(website):
    if(os_platform == 'Windows'):
        for url_website in microsft_chrome_list:
            website_in_list  = url_website in website
            if(website_in_list):
                return url_website
    else: 
        for url_website in linux_chrome_list:
            website_in_list  = url_website in website
            if(website_in_list):
                url_website = websites_dictionary[url_website]
                return url_website
        
    string_list = website.split('-')
    string_split_list = string_list[1].split(' ',1)
    try:
        new_split_list = string_split_list[1].split('@')
        new_split_list = new_split_list[0] if len(new_split_list) < 2 else new_split_list[1]
        string_split_list[1] = websites_dictionary[new_split_list]
    except:
        websites_dictionary[string_split_list[1]] = string_split_list[1]
    return string_split_list[1]


def get_microsoft_current_window(window_name):
    for window in microsoft_windows_list:
        window_in_list  = window in window_name
        if(window_in_list):
            return window
    return 'Other'




