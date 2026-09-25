[app]

# (str) Title of your application
title = Dich Game HOK

# (str) Package name
package.name = dichgamehok

# (str) Package domain (needed for android/ios packaging)
package.domain = org.game

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy,pillow,pytesseract

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (bool) Accept SDK license
android.accept_sdk_license = True

# (list) List of architectures to build for (chỉ build 64-bit để tránh lỗi và tăng tốc)
android.archs = arm64-v8a
