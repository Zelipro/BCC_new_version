[app]
title = BCC - CEET Control
package.name = bcc
package.domain = com.ceet.bcc
source.dir = .
version = 2.1
requirements = python3,kivy,kivymd,pillow,requests,pandas,openpyxl,fpdf2
orientation = portrait

# Icône principale de l'application
icon.filename = CEET.png

# Écran de démarrage (splash screen)
presplash.filename = CEET.png

# Couleur de fond pour l'écran de démarrage (jaune CEET)
presplash.color = #FFFF00

# Permissions Android nécessaires
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# Architecture Android
android.archs = arm64-v8a,armeabi-v7a

# API Android
android.api = 31
android.minapi = 21
android.ndk = 25b

[buildozer]
log_level = 2

# Répertoire de build
# build_dir = .buildozer
# bin_dir = ./bin
