#!/usr/bin/python

"""
This script contains the functions for synchronization across my machines with
master as the intermediary.

"""

import subprocess
import platform
import os
import sys

local_sync_dir = "/home/john/sync_dir/"
local_backup_dir = "/home/john/backups/sync_dir_backup"

master_name = "master3"  # IP or looks up /etc/hosts
master_remote_dir = "/home/john/sync_dir/"
master_logfile = "/home/john/syncstats.txt"


def copy_local_sync_dir_to_local_backup():
    """
    Rsync local sync dir to local sync dir backup.
    """
    print("Syncing to local backup")
    cmd = "rsync -avz --delete {} {}".format(local_sync_dir, local_backup_dir)
    status = os.system(cmd)
    if status == 0:
        print("Succeeded...")
    else:
        print("Local backup failed. Exiting.")
        sys.exit()


def copy_local_sync_dir_to_master():
    """
    Rsync local sync dir to master.
    """
    print("Syncing to master")
    cmd = "rsync -avzhe ssh --delete {} {}:{}".format(local_sync_dir, 
                                                        master_name, 
                                                        master_remote_dir)
    status = os.system(cmd)
    if status == 0:
        print("Succeeded...")
    else:
        print("Push to remote failed. Exiting.")
        sys.exit()

def copy_master_to_local_sync_dir():
    """
    Rsync from master to local sync dir.
    """
    print("Syncing from master to local")
    cmd = "rsync -avzhe ssh --delete {}:{} {}".format(master_name, 
                                                master_remote_dir,
                                                local_sync_dir)
    status = os.system(cmd)
    if status == 0:
        print("Succeeded...")
    else:
        print("Push to remote failed. Exiting.")
        sys.exit()


def write_log(sync_type):
    """
    Write log of push or pull to master.

    * sync_type should be either "Push" or "Pull"
    """
    date = subprocess.check_output('date')
    date = date.decode('ascii').strip()
    this_machine = platform.node()
    output = "{} sync from {} at {}".format(sync_type, this_machine, date)
    cmd = 'echo "{}" | ssh master3 "cat >> {}"'.format(output, master_logfile)
    status = os.system(cmd)
    if status == 0:
        print("Recorded sync in remote log file {}".format(master_logfile))
    else:
        print("Log write failed!")
        sys.exit()

def display_sync_status():
    print("Showing syncs, most recent last")
    print("\n")
    remote_cmd = 'tail {}'.format(master_logfile)
    cmd = 'ssh {} "{}"'.format(master_name, remote_cmd)
    os.system(cmd)
