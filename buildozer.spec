[app]
title = Part Number Search
package.name = partnumbersearch
package.domain = org.partnumbersearch
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xlsx
source.include_patterns = data/*.xlsx
version = 1.0

requirements = python3,kivy==2.2.1,pandas,openpyxl,xlrd

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.arch = arm64-v8a
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.presplash_color = #FFFFFF
android.orientation = portrait

# Optional: Uncomment to add an icon
#android.presplash.filename = %(source.dir)s/data/presplash.png
#android.icon.filename = %(source.dir)s/data/icon.png

p4a.branch = master
p4a.bootstrap = sdl2