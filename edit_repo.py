#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
from pathlib import Path

rhel_release = Path('/etc/redhat-release')
alt_release = Path('/etc/altlinux-release')
deb_repo_list = '/etc/apt/sources.list'
rpm_repo_config = '/etc/yum.repos.d/sn-local.repo'

def run_bash_command(bashCommand):
    process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE)
    output, err = process.communicate()
    ret_code = process.wait()
    return output, ret_code


def write_new_line(filename, data):
    f = open(filename, 'a')
    f.write(data)
    f.close()


def check_input_args():
    if len(sys.argv) < 2:
        print('Path not specified')
        exit(1)

def edit_repo(repo_dir):
    if rhel_release.exists() and alt_release.exists() is False:
        repo_str = '''[sn-local]
		name=Local Secret Net LSP Repository
		baseurl=file://{}
		enabled=1
		gpgcheck=0'''.format(repo_dir)
        write_new_line(rpm_repo_config, repo_str)
    elif alt_release.exists():
        repo_str = '\nrpm-dir file://{} x86-64 dir'.format(repo_dir)
        write_new_line(deb_repo_list, repo_str)
    else:
        repo_str = '\ndeb [trusted=yes] file://{} ./'.format(repo_dir)
        write_new_line(deb_repo_list, repo_str)


if __name__ == "__main__":
    check_input_args()
    path = sys.argv[1]
    edit_repo(path)

    if rhel_release.exists() is False or alt_release.exists():
        run_bash_command('apt-get update')
