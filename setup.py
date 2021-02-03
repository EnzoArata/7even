from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('7evenAlpha.py', base=base, target_name = 'Seven')
]

installOptions = {
    'upgrade_code': "{e7a3baf0-3011-4e16-9bb3-d61186a6a0c4}",
    'add_to_path': False}

setup(name='7even',
      version = '0.02',
      description = '7even: All in One Retail Bot',
      options = {'build_exe': build_options, 'bdist_msi': installOptions},
      executables = executables)
