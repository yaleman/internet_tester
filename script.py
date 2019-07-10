#!/usr/bin/env python3
def ping(endpoint):
    command = "/sbin/ping -c 5 {}".format(endpoint)
    response = sub_run(command.split(), stdout=DEVNULL)
    
    response = response.returncode
    #and then check the response...
    if response == 0:
        return True
    else:
        return False

def getroute():
    command = "netstat -rn".split()
    response = check_output(command)
    return response

def get_default_route():
    routes = getroute()
    default_route = [ route for route in routes.decode('utf-8').split('\n') if 'default' in route and 'fe80' not in route ]
    if len(default_route) != 1:
        txt.insert('insert',"More than one default route set? Eek.")
    gateway = default_route[0].split()[1]
    return gateway

def get_nameservers():
    with open('/etc/resolv.conf', 'r') as fh:
        content = fh.read()
    ns = [ line.split()[1] for line in content.split('\n') if line.startswith('nameserver ')]
    return ns

def heading(text):

    txt.insert('insert',"#"*(len(text)+3))

    txt.insert('insert',"\n")
    txt.insert('insert',text)
    txt.insert('insert',"\n")
    txt.insert('insert',"#"*(len(text)+3))
    txt.insert('insert',"\n")

def dns_resolve_test(hostname, resolver):
    """ tries a dns resolution of the hostname using dig, 
    returns True if it got a valid response """
    command = "/usr/bin/dig +short {} @{}".format(hostname, resolver).split()
    response = sub_run(command, stdout=DEVNULL)
    if response.returncode == 0:
        return True
    return False
def dotests():
 if BASICS:
    heading("Basic Connectivity")
    root.update()
    txt.insert('insert',"Testing ping of default route... ")
    root.update()

    if( ping(get_default_route())):
        txt.insert('insert',"OK\n")
    else:
        txt.insert('insert', "Failed, check connection to network\n")
    txt.insert('insert',"Testing ping of google DNS (8.8.8.8)...")
    root.update()
    if( ping('8.8.8.8')):
        txt.insert('insert',"OK\n")
    else:
        txt.insert('insert',"Failed, check the router/connection\n")
        return False
# end basics
    root.update()

    heading("DNS Tests")
    if not get_nameservers():
        txt.insert('insert',"DNS Servers not set? That's weird. Stopping")
        return False
    root.update()
    if DNSPING:
        txt.insert('insert',"Checking connection to nameservers... ping first\n")
        for nameserver in get_nameservers():
            txt.insert('insert',"\t{}".format(nameserver), )
            if ping(nameserver):
                txt.insert('insert'," OK\n")
            else:
                txt.insert('insert'," Failed\n")
    root.update()
    if DNSRESOLVE:
        txt.insert('insert',"Checking resolution against nameservers\n")
        nameservers_good = 0
        for nameserver in get_nameservers():
            txt.insert('insert',"\t{} ".format(nameserver))
            if dns_resolve_test('google.com', nameserver):
               txt.insert('insert'," OK\n")
               nameservers_good = nameservers_good+1
            else:
                txt.insert('insert',"Failed\n")
        if nameservers_good != len(get_nameservers()):
            txt.insert('insert',"One or more nameservers failed to resolve google.com\n")
        elif nameservers_good == 0:
            txt.insert('insert',"No nameservers resolved google.com successfully\n")
            return False

    root.update()
    testfilenames = {
        'ten' : [ 'http://mirror.internode.on.net/pub/test/10meg.test',
            'http://mirror.internode.on.net/pub/test/10meg.test1',
    #        'http://mirror.internode.on.net/pub/test/10meg.test2',
    #        'http://mirror.internode.on.net/pub/test/10meg.test3',
     #       'http://mirror.internode.on.net/pub/test/10meg.test4',
      #      'http://mirror.internode.on.net/pub/test/10meg.test5',
            ]
        }


    root.update()

    if DOWNLOADTEST:
        heading("Download speed test")
        txt.insert('insert',"downloading {} 10 MB files. This could take some time.".format(len(testfilenames['ten'])))    
        root.update()
        failed = 0
        times = []
        for url in testfilenames['ten']:
            import time
            startime = time.time()
            req = get(url)
            endtime = time.time()
            times.append((len(req.text), endtime - startime ))
            try:
                req.raise_for_status()
                txt.insert('insert',".")
                root.update()
            except:
                failed = failed + 1
                txt.insert('insert',"\nFile {} failed: {}\n".format(url, req.status_code))
                root.update()
        if not failed:
            txt.insert('insert',"Test OK!\n")
        #txt.insert('insert',"Times:")
        #txt.insert('insert',times)
        #txt.insert('insert','\n')
        speeds = [ round((size / float(time)/1024), 3) for size, time in times ]
        for speed in speeds:
            txt.insert('insert',"{}kb/s\n".format(speed))

        speed_average = sum(speeds) / float(len(speeds))
        txt.insert('insert',"Average speed: {}kb/s\n".format(speed_average))


    txt.insert('insert', "All tests complete")

    root.update()
    print("Done!")


try:



    from requests import get
    from subprocess import run as sub_run
    from subprocess import DEVNULL, check_output
    #import os
    from sys import exit
    import traceback
    import time

    # what to check flags
    BASICS = True
    DNSPING = True 
    DNSRESOLVE = True
    DOWNLOADTEST = True
    # end what to check flags

    from tkinter import *
    from tkinter import scrolledtext
    from tkinter import ttk


    root = Tk()
    root.title("Internet Troubleshooter")
    root.geometry('700x500')
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0,sticky=(N,W,E,S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    btn = ttk.Button(root, text="Test", command=dotests)
    btn.grid(column=0, row=0, sticky=S)


    txt = scrolledtext.ScrolledText(mainframe,width=80,height=30)
    txt.grid(column=0,row=0)
    txt.pack(fill='both', expand=True, padx=8, pady=20)

    root.mainloop()

except:
    y,mn,d,h,m,s,a,b,c = time.localtime()
    print("==================="+str(mn)+'/'+str(d)+' '+
               str(h)+':'+str(m)+':'+str(s)+
               "=====================")
    traceback.print_last()
    sys.exit()



