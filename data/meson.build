desktop_file = i18n.merge_file(
  input: 'com.github.hezral.quickword.desktop.in',
  output: 'com.github.hezral.quickword.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = i18n.merge_file(
  input: 'com.github.hezral.quickword.appdata.xml.in',
  output: 'com.github.hezral.quickword.appdata.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'metainfo')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

install_data('com.github.hezral.quickword.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif

install_data('application.css',
  install_dir: join_paths(pkgdatadir, project_short_name, 'data')
)

# install_data(
#     join_paths('icons', '128', meson.project_name() + '.svg'),
#     install_dir: join_paths(get_option ('datadir'), 'icons', 'hicolor', 'scalable', 'apps'),
#     rename: meson.project_name() + '.svg'
# )

install_data(
    join_paths('icons', meson.project_name() + '-' + 'symbolic' + '.svg'),
    install_dir: join_paths(get_option ('datadir'), 'icons', 'hicolor', 'symbolic', 'apps'),
)

other_icon_sources = [
  join_paths('icons', meson.project_name() + '-' + 'left' + '.svg'),
  join_paths('icons', meson.project_name() + '-' + 'right' + '.svg'),
  join_paths('icons', meson.project_name() + '-' + 'symbolic' + '.svg'),
  join_paths('icons', meson.project_name() + '-' + 'coffee' + '.svg'),
]
iconsdir = join_paths(pkgdatadir, project_short_name, 'data', 'icons')
install_data(other_icon_sources, install_dir: iconsdir)

icon_sizes = ['16', '24', '32', '48', '64', '128']
foreach i : icon_sizes
    install_data(
        join_paths('icons', i + '.svg'),
        rename: meson.project_name() + '.svg',
        install_dir: join_paths(get_option ('datadir'), 'icons', 'hicolor', i + 'x' + i, 'apps')
    )
    install_data(
        join_paths('icons', i + '.svg'),
        rename: meson.project_name() + '.svg',
        install_dir: join_paths(get_option ('datadir'), 'icons', 'hicolor', i + 'x' + i + '@2', 'apps')
    )
endforeach