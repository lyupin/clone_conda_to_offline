
# coding: utf-8

# In[16]:


import shutil
import os

# In[13]:


def analyze_pkg_from_list(fn, skip_header = 4, debug = False, with_postfix = False):
    '''
    Analyze package names (and versions) from a list output by 'conda list --explicit > fn'
    return: (pkgs, lines), where 'pkgs' is the list of package names, and 'urls' is the list of package download urls. 
    '''
    fid = open(fn, 'r')
    lines = fid.readlines()
    n_line = len(lines)
    lines = lines[skip_header:n_line]
    if debug: 
        print(lines)
    
    urls = [line.rstrip() for line in lines]
    pkgs = [line.split('/')[-1].rstrip() for line in lines]
    if not with_postfix:
        # assume all packages end with '.tar.bz2'
        pkgs = [line[:-8] for line in pkgs]
    if debug:
        print(pkgs)
    return pkgs, urls
    


# In[17]:


fn_conda_list = 'list.txt'

# The only line left for you to modify: fill your path of package cache.
# You can know the path by command "conda info" and find the entry 'package cache'
pkg_source_dir = '/home/plyu/miniconda3/pkgs/'

pkg_dest_dir = './pkg_bak/linux-64/'
pkgs, urls = analyze_pkg_from_list(fn_conda_list)

## for test
#pkg_source_dir = './'
#pkgs = ['a']

n_pkg = len(pkgs)
for i_pkg in range(n_pkg):
    print('Working on [' + str(i_pkg+1) + ']: ' + pkgs[i_pkg])
    try:
        shutil.copy2(pkg_source_dir + pkgs[i_pkg] + '.tar.bz2', pkg_dest_dir)
    except FileNotFoundError:
        cmd_tmp = 'wget {:s} -O {:s}'.format(urls[i_pkg], os.path.join(pkg_dest_dir, pkgs[i_pkg]+'.tar.bz2'))
        print(cmd_tmp)
        os.system(cmd_tmp)

