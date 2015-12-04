#!/usr/bin/python

"""
This script 

    * rsyncs from local sync dir to master
    * leave a record of the push on master

"""

import synchronize

synchronize.copy_local_sync_dir_to_master()
synchronize.write_log("Push")

