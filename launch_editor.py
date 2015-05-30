#!/usr/bin/env python
# encoding: utf-8

import os
from subprocess import check_call
from uuid import uuid4

editor = os.environ['EDITOR']

def read_from_editor():
    tmpfile = 'tmp.' + str(uuid4()) + '.markdown'
    cmd = ' '.join([editor, tmpfile])
    check_call(cmd, shell=True)

    # check if tmp file exists and read it if it exists
    tmp_file_exists = os.path.exists(tmpfile)
    if tmp_file_exists:
        s = open(tmpfile).read().strip()
    else:
        s = None

    if tmp_file_exists:
        os.remove(tmpfile)

    return s

if __name__ == '__main__':
    print read_from_editor()
