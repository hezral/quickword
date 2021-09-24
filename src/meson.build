pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'quickword')
gnome = import('gnome')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'quickword.in',
  output: 'quickword',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

quickword_sources = [
  '__init__.py',
  'utils.py',
  'main.py',
  'main_window.py',
  'clipboard_manager.py',
  'data_manager.py',
  'noword_view.py',
  'settings_view.py',
  'updater_view.py',
  'word_lookup.py',
  'word_view.py'
]

install_data(quickword_sources, install_dir: moduledir)
