# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['auction.py',
	'D:\\pythonProject\\Setting\\Base.py',
	'D:\\pythonProject\\Setting\\Publics.py'],
    pathex=['D:\\pythonProject\\Setting'],
    binaries=[],
    datas=[],
    hiddenimports=['pymysql',
	'datetime',
	'urllib3',
	'requests',
	'json',
	'os',
	'unittest'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='auction',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon=['favicon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='auction',
)
