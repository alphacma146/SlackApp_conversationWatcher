# -*- mode: python ; coding: utf-8 -*-


from kivy_deps import sdl2, glew
block_cipher = None


a = Analysis(
    ['launch.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('view_layout.kv','.'),
        ('LICENSE','.'),
        ('cripto_token.dat','.'),
    ],
    hiddenimports=['win32file', 'win32timezone'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['IPython', 'kivy_install'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    name='SlackLogAccumulator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['favicon.ico'],
)

coll = COLLECT(
    exe, Tree('.'),
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    name='cash'
)
