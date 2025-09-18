[app]
title = BCC Control
package.name = BCC
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 2.0
requirements = python3,kivy,kivymd,pillow,sqlite3,requests,hashlib,pathlib,datetime,pandas,openpyxl,python-docx,reportlab
icon.filename = %(source.dir)s/CEET.png

[buildozer]
log_level = 2

[android]
api = 34
minapi = 21
ndk = 25b
sdk = 34
android.permissions = INTERNET
android.archs = arm64-v8a, armeabi-v7a
orientation = all
android.orientation = all
