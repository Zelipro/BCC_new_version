[app]
title = BCC - CEET Control
package.name = bcc
package.domain = com.ceet.bcc
source.dir = .
version = 2.2
requirements = python3,kivy,kivymd,pillow,requests,pandas,openpyxl,fpdf2
orientation = portrait

# Icône principale de l'application
icon.filename = CEET.png

# Écran de démarrage (splash screen)
presplash.filename = CEET.png

# Couleur de fond pour l'écran de démarrage (jaune CEET)
presplash.color = #FFFF00

# Permissions Android COMPLÈTES pour les fichiers
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE,MANAGE_EXTERNAL_STORAGE

# Architecture Android
android.archs = arm64-v8a,armeabi-v7a

# API Android
android.api = 31
android.minapi = 21
android.ndk = 25b

# Configuration de compilation
android.accept_sdk_license = True

# Target SDK pour Android 11+ (nécessaire pour MANAGE_EXTERNAL_STORAGE)
android.gradle_dependencies = androidx.core:core:1.6.0

[buildozer]
log_level = 2
