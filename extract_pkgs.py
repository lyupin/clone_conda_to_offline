
# coding: utf-8

# In[16]:


import shutil
import os

# In[13]:


def analyze_pkg_from_list(fn, skip_header = 4, debug = False, with_postfix = False):
    '''
    Analyze package names (and versions) from a list output by 'conda list --explicit > fn'
    '''
    fid = open(fn, 'r')
    lines = fid.readlines()
    n_line = len(lines)
    lines = lines[skip_header:n_line]
    if debug: 
        print(lines)
    
    pkgs = [line.split('/')[-1].rstrip() for line in lines]
    if not with_postfix:
        # assume all packages end with '.tar.bz2'
        pkgs = [line[:-8] for line in pkgs]
    if debug:
        print(pkgs)
    return pkgs
    


# In[17]:


fn_conda_list = 'list.txt'

# On a Windows Subsystem Linux
pkg_dir = './pkg_bak/linux-64/'
pkgs = analyze_pkg_from_list(fn_conda_list)

## for test
#pkg_source_dir = './'
#pkgs = ['a']

n_pkg = len(pkgs)
for i_pkg in range(n_pkg):
    print('Extracting on [' + str(i_pkg+1) + ']: ' + pkgs[i_pkg] + '.tar.bz2')
    fn_tmp = pkg_dir + pkgs[i_pkg]
    os.makedirs(fn_tmp, exist_ok = True)
    cmd_tmp = 'tar -xjf ' + fn_tmp + '.tar.bz2' + ' -C '+fn_tmp
    print(cmd_tmp)
    os.system(cmd_tmp)

