'''
   Copyright 2020 Adi Hezral (hezral@gmail.com) (https://github.com/hezral)

   This file is part of QuickWord ("Application").

    The Application is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The Application is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this Application.  If not, see <http://www.gnu.org/licenses/>.
'''

from distutils.core import setup
from distutils.command.install import install

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
icon_scalable = prefix_data + '/icons/hicolor/scalable/apps'

# Setup install data list
install_data = [(prefix_data + '/metainfo', ['data/' + app_id + '.appdata.xml']),
                (prefix_data + '/applications', ['data/' + app_id + '.desktop']),
                (prefix_data + '/glib-2.0/schemas',['data/' + app_id + '.gschema.xml']),
                (install_path + '/data/icons',['data/icons/' + app_id + '-symbolic.svg']),
                (install_path + '/data/icons',['data/icons/' + app_id + '-left.svg']),
                (install_path + '/data/icons',['data/icons/' + app_id + '-right.svg']),
                (install_path + '/data',['data/application.css']),
                (install_path,[app_name + '/application.py']),
                (install_path,[app_name + '/clipboard_manager.py']),
                (install_path,[app_name + '/custom_shortcut_settings.py'
                (install_path,[app_name + '/data_manager.py']),
                (install_path,[app_name + '/main_window.py']),
                (install_path,[app_name + '/noword_view.py']),
                (install_path,[app_name + '/settings_view.py']),
                (install_path,[app_name + '/updater_view.py']),
                (install_path,[app_name + '/word_lookup.py']),
                (install_path,[app_name + '/word_view.py']),
                (icon_scalable,['data/icons/' + app_id + '.svg']),]

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
    install_data.append(file)
    install_data.append(file2x)

# Post install commands
class PostInstall(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        # print('Updating icon cache...')
        # call(['gtk-update-icon-cache', '-qtf', path.join(prefix_data, 'icons', 'hicolor')])

        # print("Installing new Schemas")
        # call(['glib-compile-schemas', path.join(prefix_data, 'glib-2.0/schemas')])

        # print("Clean-up")
        # import shutil
        # for size in icon_sizes:
        #     shutil.rmtree('data/icons/' + size)
            
setup(
    name=app_name,  # Required
    license='GNU GPL3',
    version='1.0.0',  # Required
    url=app_url,  # Optional
    author='Adi Hezral',  # Optional
    author_email='hezral@gmail.com',  # Optional
    scripts=[app_id],
    data_files=install_data,  # Optional
    cmdclass={
        'install': PostInstall,
    }
)