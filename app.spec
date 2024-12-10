# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['app.py'],
             pathex=['C:\\Users\\Raz_Z\\Projects\\Shmuel\\posac'],
             binaries=[],
             datas=[('lib/assets', 'lib/assets'), ('lib/assets/toolbar', 'lib/assets/toolbar'),
             ('lib/assets/navigation', 'lib/assets/navigation'),
			 ('lib/scripts/IdoPosac/*','lib/scripts/IdoPosac/'),
			 ('README.md', '.'),
			 ('lib/gui/components/editable_tree_view/assets/*',
			 'lib/gui/components/editable_tree_view/assets'),
             ('.env', '.')  # Include .env file in the root of the bundle
			 ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tests', '*.SCR'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Posac',
          debug=False,
          bootloader_ignore_signals=False,
		  uac_admin=False,
          strip=False,
          upx=True,
          console=False,
		  icon='lib\\assets\\icon.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Posac',
               )
