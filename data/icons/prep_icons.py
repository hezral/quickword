import pathlib, os, shutil
from os import path
from subprocess import call

# Base application info
base_rdnn = 'com.github.hezral'
app_name = 'quickword'
app_id = base_rdnn + '.' + app_name
app_url = 'https://github.com/hezral/' + app_name
saythanks_url = 'https://saythanks.io/to/adihezral%40gmail.com'

# Setup file paths for data files
prefix = '/usr'
prefix_data = path.join(prefix, 'share')
install_path = path.join(prefix_data, app_id)
icon_path = 'icons/hicolor'
icon_sizes = ['16','24','32','48','64','128']

# Setup install data list


# Add icon data files to install data list
for size in icon_sizes:
    prefix_size = size + 'x' + size
    prefix_size2x = size + 'x' + size + '@2'
    icon_dir = path.join(prefix_data, icon_path, prefix_size, 'apps')
    icon_dir2x = path.join(prefix_data, icon_path, prefix_size2x, 'apps')
    icon_file = 'data/icons/' + size + '.svg'
    if not os.path.exists('data/icons/' + size):
        os.makedirs('data/icons/' + size)
    new_icon_file = path.join('data/icons/', size, (app_id + '.svg'))
    shutil.copyfile(icon_file, new_icon_file)
    file = (icon_dir, [new_icon_file])
    file2x = (icon_dir2x, [new_icon_file])
    print(file)
    print(file2x)