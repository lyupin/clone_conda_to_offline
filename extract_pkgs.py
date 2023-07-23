import shutil
import os

def analyze_pkg_from_list(fn, skip_header = 4, debug = False):
    '''
    Analyze package names (and versions) from a list output by 'conda list --explicit > fn'
    '''
    fid = open(fn, 'r', encoding = 'utf-16') # utf-16 encoding is used for Windows, encoding option might be remove for Linux.
    lines = fid.readlines()
    n_line = len(lines)
    lines = lines[skip_header:n_line]
    if debug: 
        print(lines)
    
    pkgs = [line.split('/')[-1].rstrip() for line in lines]

    if debug:
        print(pkgs)
    return pkgs
    
fn_conda_list = 'list.txt'

# On a Windows Subsystem Linux
pkg_dir = './pkg_bak/win64/'
pkgs = analyze_pkg_from_list(fn_conda_list)

## for test
#pkg_source_dir = './'
#pkgs = ['a']

n_pkg = len(pkgs)
for i_pkg in range(n_pkg):
    cmd_tmp = 'conda install ' + pkg_dir + pkgs[i_pkg]
    print('Run: ' + cmd_tmp)
    os.system(cmd_tmp)

