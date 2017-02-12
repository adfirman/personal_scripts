'''
Created on May 24, 2016

@author: adfirman

Uses Handbrake CLI to encode any videos found in the specified path

'''

import os
import subprocess
import shutil
import sys
import re

class log_writer:
 
    def __init__(self, stdout, filename):
        self.stdout = stdout
        self.logfile = file(filename, 'a')
 
    def write(self, text):
        self.stdout.write(text)
        self.logfile.write(text)
 
    def close(self):
        self.stdout.close()
        self.logfile.close()
 
writer = log_writer(sys.stdout, r'C:\python_data\dvr_transcoder.log')
sys.stdout = writer

def parse_options():

    from optparse import OptionParser

    global _opt_

    parser = OptionParser()
    parser.add_option('--handbrakecli_path', dest='handbrakecli_path', help='Path to handbrakecli file')
    parser.add_option('--recordings_path', dest='recordings_path', help='Path to recordings directory')    
    parser.add_option('--preset', dest='preset', help='HandBrakeCLI preset to use')    
    parser.add_option('--encoder_to_use', dest='encoder_to_use', help='handbrake encoder to use (h264, h265, qsv_h264, qsv_h265')
    parser.add_option('--extra_args', dest='extra_args', help='any additional cmdline args for handbrakecli')        

    (_opt_, args) = parser.parse_args() 

def encode_file(file_path, file_name):
    
    matches = re.search('(.*)(?=\.[\w\d]+$)', file_name)
    #matches = re.search((?=\.[\w\d]+\$), file_name)
    if matches:
        new_file_name = "{0}.mp4".format(matches.group(1))
    
    command = "{0} -i \"{1}\" -o \"{2}\" -Z \"{3}\"".format(_opt_.handbrakecli_path, 
                                                            file_path + os.sep + file_name, 
                                                            _opt_.recordings_path + os.sep + new_file_name,
                                                            _opt_.preset)
    
    #windows systems don't seem to like the quicksync encoded files, so use x264 for now
    #encode time appears similar
    if _opt_.encoder_to_use == 'qsv_h264':
        command = "{0} -e qsv_h264".format(command)
        
    if _opt_.encoder_to_use == 'x264':
        command = "{0} -e x264".format(command)      
        
    if _opt_.extra_args:
        command = "{0} {1}".format(command, _opt_.extra_args)
    
    print "Encoding using command {0}".format(command)
    #ret=subprocess.Popen(command)
    ret = os.system(command)
    
    #handbrakecli is returning non-zero codes for successful jobs
    #need to look at which are error codes
    return True

def walk_path(path):
    
    for root, dirs, files in os.walk(path):
        if root == _opt_.recordings_path or re.search('.grab', root):
            print "Skipping {0}".format(root)
            continue        
        
        print "Looking in {0}".format(root)        
        #if sub-directories, go down
        for directory in dirs:
            walk_path(root + os.sep + directory)
            
        #no sub-directories left, start processing file
        #process all the files in this directory 
 
        for item in files:
            print "Found {0}".format(item)
            encode_file(root, item)

            #delete files when done
            path = os.path.join(root, item)
            print "os.remove({0})".format(path)
            os.remove(path)          
            
        #nothign left in this directory, clean up
        print "Deleting {0}".format(root)
        shutil.rmtree(root)

def main():
    parse_options()
    walk_path(_opt_.recordings_path)

if __name__ == '__main__':
    main()
