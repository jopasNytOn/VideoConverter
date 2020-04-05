#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import msvcrt
import os
import re
import shutil
import sys
import time

application_version = 0.08

# customer settings

def ExaminePaths():
    rec_path = projectx_path = mplex_path = staxrip_path = ""
    file = open('VideoConverter_Paths.txt', 'r')
    paths = re.compile('^.+= "(?P<path>.+)"$')
    for line in file:
        if line.find("rec_path") != -1:
            result = paths.match(line)
            rec_path = result.group(1)
        elif line.find("projectx_path") != -1:
            result = paths.match(line)
            projectx_path = result.group(1)
        elif line.find("mplex_path") != -1:
            result = paths.match(line)
            mplex_path = result.group(1)
        elif line.find("staxrip_path") != -1:
            result = paths.match(line)
            staxrip_path = result.group(1)
    return rec_path, projectx_path, mplex_path, staxrip_path

rec_path, projectx_path, mplex_path, staxrip_path = ExaminePaths()
dir_list = os.listdir(rec_path)

# main program

python_major, python_minor, python_micro, releaselevel, serial = sys.version_info
print('\nVideoConverter %.2f' % (application_version))
print('converts a REC file downloaded from Topfield DVB to a AVI/MPG file\n\n')

print('Python environment:')
print('sys.platform:          %s' % sys.platform)
major, minor, build, platform, text = sys.getwindowsversion()
print('sys.getwindowsversion: %d.%d.%d %s' % ( major, minor, build, text))
print('sys.version_info:      %d.%d.%d' % ( python_major, python_minor, python_micro))
print('sys.prefix:            %s' % sys.prefix)

for filename in dir_list:

    if filename.endswith(".rec"):

        print('\n\n\nFile %s\n\n' % filename)
        if filename.find(' ') != -1:
            print('Space is not accepted in the file name!\n\n')
            continue

        print('\n\n\nPhase 1\n\n')

        yle_pages = [451, 452, 453, 454, 771, 779]

        print('Note: if subtitles needed:')
        print('        Presettings -> subtitle:')
        print('          re-build TTX-PTS from 1st MpgAudio str...')
        print('          teletext pages to decode:')
        print('            Yleisradio TV1   %d' % yle_pages[0])
        print('                       TV2   %d' % yle_pages[1])
        print('                       Teema %d' % yle_pages[2])
        print('                       24    %d' % yle_pages[3])
        print('                       FST   %d/%d' % (yle_pages[4], yle_pages[5]))
        print('          1. subtitle export formats: SRT')
        print('\n\n')
        time.sleep(2)

        os.system("java -jar %s\\ProjectX.jar %s\\%s -gui" % (projectx_path, rec_path, filename)) 
        time.sleep(2)

        print('\n\n\nPhase 2\n\n')

        filename = filename.replace(".rec", "")

        yle_video = False
        for yle_page in yle_pages:
            if os.path.isfile("%s\\%s[%d].srt" % (rec_path, filename, yle_page)):
                if staxrip_path.find("1.1.7.0"):
                    print('Note: Use the following steps:')
                    print('      - Choose the hyperlink Source and choose Single Or Merge')
                    print('      - Choose the m2v file and press Open and OK')
                    print('      - Choose the hyperlink DivX Plus and choose XviD')
                    print('      - Press the hyperlink AAC VBR ~96 kbps and choose Just Mix')
                    print('      - Choose Tools -> Hardcoded Subtitle...')
                    print('      - Choose the srt file and press Open')
                    print('      - Press Next and then Start')
                    print('      - Operation takes many minutes (percentage of the progress at Taskbar)')
                elif staxrip_path.find("1.1.2.0"):
                    print('Note: Use the following steps:')
                    print('      - Choose File -> Open Source... -> Single Or Merge')
                    print('      - Choose the m2v file and press Open and OK')
                    print('      - Choose Profiles -> Encoder -> XviD -> Constant Quality')
                    print('      - Choose Profiles -> Container -> AVI')
                    print('      - Press the hyperlink AAC 50-90 kbps in Audio and choose Add Existing File')
                    print('      - Choose Tools -> Add hardcoded subtitle')
                    print('      - Choose the srt file and press Open')
                    print('      - Press Next 4 times and then Start')
                    print('      - Operation takes many minutes (percentage of the progress at Taskbar)')
                else:
                    print('\n\nThere is currently no help for the StaxRip version installed\n\n')
                time.sleep(2)

                os.system("%s\\StaxRip.exe" % staxrip_path)
                yle_video = True

        if yle_video == False:
            os.system("%s\\mplex1.exe %s\\%s.m2v %s\\%s.mp2" % (mplex_path, rec_path, filename, rec_path, filename))

        print('\n\n\nPhase 3\n\n')

        # remove temporary files

        extensions = [".avs", ".d2v", ".log", ".m2v", ".rip", \
                      ".mp2", "[1].mp2", "[2].mp2", "-02.mp2", \
                      ".sup", "[1].sup", "-02.sup", ".sup.IFO", "[1].sup.IFO", "-02.sup.IFO", \
                      "_AutoCrop.avs", "_DGIndex.log", "_log.txt", "_SecondPass.vcf", "_Source.avs", "_StaxRip.log"]

        for extension in extensions:
            if os.path.isfile("%s\\%s%s" % (rec_path, filename, extension)):
                os.remove("%s\\%s%s" % (rec_path, filename, extension))

        for yle_page in yle_pages:
            if os.path.isfile("%s\\%s[%d].srt" % (rec_path, filename, yle_page)):
                os.remove("%s\\%s[%d].srt" % (rec_path, filename, yle_page))

        if os.path.isdir("%s\\%s temp files" % (rec_path, filename)):
            shutil.rmtree("%s\\%s temp files" % (rec_path, filename))

while msvcrt.kbhit(): # read earlier key strokes to prevent
    msvcrt.getch()    # temporary DOS window from disappearing
if int(python_major) < 3:
    raw_input('\n\nPress ENTER to quit...')
else:
    input('\n\nPress ENTER to quit...')
