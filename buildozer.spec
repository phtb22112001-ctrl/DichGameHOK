[app]

# (str) Title of your application
title = Dich Game HOK

# (str) Package name
package.name = dichgamehok

# (str) Package domain (needed for android/ios packaging)
package.domain = org.game

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (Đã thêm json vào đây)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0

# (list) Application requirements (Đã bỏ pytesseract để chống văng app)
requirements = python3,kivy,pillow

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

# (list) List of architectures to build for (chỉ build 64-bit)
android.archs = arm64-v8a
