[app]
title = BCC Control
package.name = BCC
package.domain = org.example
source.dir = .
requirements.source.python3 = 3.10
source.include_exts = py,png,jpg,kv,atlas,db
version = 2.0
requirements = python3,kivy,kivymd,pillow,requests,pandas,openpyxl,python-docx,,reportlab==4.2.2
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
# Supprimer cette ligne dupliquée :
# orientation = all
android.orientation = portrait
# Ajouter ces lignes pour éviter les problèmes de permissions :
android.accept_sdk_license = True
android.skip_update = False
