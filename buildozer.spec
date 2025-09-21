[app]
title = BCC - CEET Control
package.name = bcc
package.domain = com.ceet.bcc
source.dir = .
version = 2.2

# Requirements avec versions fixes pour stabilité
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pillow,requests,pandas,openpyxl,fpdf2==3.0.0,pyjnius

orientation = portrait

# Icône et splash
icon.filename = CEET.png
presplash.filename = CEET.png
presplash.color = #FFFF00

# =============================================
# PERMISSIONS ANDROID MODERNES
# =============================================

# Permissions de base (toujours accordées)
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Permissions de stockage pour Android < 10
# Note: Ces permissions peuvent ne pas suffire pour Android 10+
android.add_permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Pour Android 11+ - Attention: peut être rejetée par Google Play
# Décommentez seulement si vraiment nécessaire
# android.add_permissions = MANAGE_EXTERNAL_STORAGE

# =============================================
# CONFIGURATION ANDROID
# =============================================

# Architecture Android
android.archs = arm64-v8a, armeabi-v7a

# API Android - Compatible avec les permissions modernes
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 31

# Configuration de compilation
android.accept_sdk_license = True

# Dépendances Gradle
android.gradle_dependencies = androidx.core:core:1.6.0, androidx.appcompat:appcompat:1.3.1

# =============================================
# CONFIGURATION POUR STOCKAGE MODERNE
# =============================================

# Utiliser le stockage scoped pour Android 10+
android.add_src = java_src

# Ajouter support pour legacy external storage (Android 10)
android.add_xml = android_xml

# Configuration P4A
p4a.branch = master
p4a.bootstrap = sdl2

# =============================================
# OPTIONS AVANCÉES
# =============================================

# Permettre l'installation depuis sources inconnues
android.allow_backup = True

# Configuration réseau et timeouts
android.logcat_filters = *:S python:D

# Configuration pour contourner les problèmes de téléchargement
[buildozer]
log_level = 2
warn_on_root = 1

# =============================================
# INSTRUCTIONS IMPORTANTES
# =============================================

# 1. Pour Android 10+ :
#    - Les fichiers seront dans le dossier privé de l'app
#    - L'utilisateur peut y accéder via le gestionnaire de fichiers
#    - Chemin typique: /Android/data/com.ceet.bcc/files/

# 2. Permissions supplémentaires :
#    - L'app demandera automatiquement les permissions au runtime
#    - L'utilisateur peut avoir besoin d'aller dans Paramètres > Apps > BCC > Permissions

# 3. Alternative sûre :
#    - Utiliser le partage de fichiers Android (Intent)
#    - Sauvegarder dans le cache de l'app
#    - Utiliser Storage Access Framework (SAF)

# 4. Test des permissions :
#    - Testez sur différentes versions d'Android
#    - Vérifiez les logs avec: adb logcat -s python
