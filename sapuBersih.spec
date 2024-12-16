# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('gui', 'gui'), ('resources', 'resources')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='sapuBersih',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='universal2',
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon=['resources/sapu_bersih.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='sapuBersih',
)
app = BUNDLE(
    coll,
    name='sapuBersih.app',
    icon='resources/sapu_bersih.icns',
    bundle_identifier='com.example.sapuBersih',
    version='0.0.1',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'NSHighResolutionCapable': True,
        'CFBundleName': 'sapuBersih',
        'CFBundleShortVersionString': '0.1',
        'CFBundleVersion': '0.0.1',  
        'CFBundleIdentifier': 'com.example.sapuBersih',
    },
)
