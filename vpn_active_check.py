'''
    Wait for VPN to launch before launching other scripts
'''

import urllib2,os,re,sys,time

commands = [
	"C:\Program Files (x86)\example\example1.exe",
	"C:\Program Files (x86)\example\example2.exe /MINIMIZED &",
]

def main():
    #wait 5 minutes before checking IP to give system time to have everything setup
    print "Waiting 5 minutes before continuing"
    time.sleep(300)

    response = urllib2.urlopen('http://ipecho.net/plain')
    ip = response.read()

    print "IP is: {0}".format(ip)

    matches=re.match('(\d+).\d+.\d+.\d+', ip)

    #24.xx.xx.xx = comcast
    #not a great match but in my case it's good enough
    if matches:
	if matches.group(1) != 24:
	    #if IP doesn't match Comcast IP, vpn is active
	    print "VPN is active, running commands"
	    for command in commands:
                print command
                handle=os.popen(command)
	else:
	    print "VPN does not appear to be active, will not run commands"

    print "exiting"
    sys.exit(0)

if __name__ == "__main__":
    main()
