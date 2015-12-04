#!/usr/bin/python

"""
This script 

    * makes a local backup of files in sync dir
    * rsyncs from master to local sync dir
    * leave a record of the pull on master

"""

import synchronize

synchronize.copy_local_sync_dir_to_local_backup()
synchronize.copy_master_to_local_sync_dir()
synchronize.write_log("Pull")


