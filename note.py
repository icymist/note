#!/usr/bin/env python
# encoding: utf-8

import yaml
import argparse
from datetime import datetime
from uuid import uuid4
import os, shutil
import subprocess as sp
import shutil

cfg_notes_file = 'proj-notes.txt'
cfg_notes_files_list = os.path.join(os.environ['HOME'], 'work/notes-files-list')
cfg_root_dir = os.path.join(os.environ['HOME'], 'work')


def longest_leading_common_directory(dir1, dir2):
    dir1 = dir1.split(os.path.sep)
    dir2 = dir2.split(os.path.sep)
    common = []
    for s1, s2 in zip(dir1, dir2):
        if s1 == s2:
            common.append(s1)
    return os.path.sep.join(common)


def get_notes_file():
    proj_notes_files = open(cfg_notes_files_list).readlines()

    # find the best match
    pwd = os.getcwd()
    common_directories = []
    for proj_notes_file in proj_notes_files:
        tmp_str = longest_leading_common_directory(proj_notes_file, pwd)
        common_directories.append(tmp_str)

    # return the longest directory
    longest_dir = ''
    for d in common_directories:
        print d, len(d)
        if len(d) > len(longest_dir):
            longest_dir = d

    return os.path.join(longest_dir, cfg_notes_file)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='note taking while working with vasp')
    
    parser.add_argument('-n', '--note', help='Note to be taken')
    parser.add_argument('-u', '--update', action='store_true', help='Update list of proj-notes files')
    
    args = parser.parse_args()


    uid = uuid4()

    date, time = datetime.now().isoformat('T').split('T')
    time = time[:8]
    timestamp = ' '.join([date, time])
    pwd = os.getcwd()

    entry = """
- uid: {uid}
  timestamp: {timestamp}
  note: {note}
  context: {pwd}
  """.format(uid=uid, timestamp=timestamp, note=args.note, pwd=pwd)

    print entry
    
    if args.note:
        notes_file = get_notes_file()
        if os.path.exists(notes_file):
            # create backup
            shutil.copy(notes_file, notes_file+'~')  
            # then add the note
            with open(notes_file, 'a') as f:
                f.write(entry)
        else:
            print '{notes_file} does not exist'.format(notes_file=notes_file)


    if  args.update:
        cmd = ['find',
                cfg_root_dir,
                '-name',
                cfg_notes_file,
               '>',
               cfg_notes_files_list
               ]
        cmd = ' '.join(cmd)
        sp.check_output(cmd, stderr=sp.PIPE, shell=True)
