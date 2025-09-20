[app]
title = BCC
package.name = bcc
package.domain = com.zelipro.bcc
source.dir = .
version = 2.0
requirements = python3,kivy,kivymd,pillow,requests,pandas,openpyxl,python-docx,reportlab
orientation = portrait

[buildozer]
log_level = 2

[android]
archs = arm64-v8a
api = 31
minapi = 21
ndk = 25b
