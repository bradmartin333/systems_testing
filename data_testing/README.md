# Raylib and data processing in dart

### Setting up dart-raylib
- Using Microsoft's new Dev Home, I created a `F Drive` as the dev drive
- Cloned repo to the dev drive
- Opened PowerShell at `F:\` and [installed raylib via vcpkg](https://github.com/raysan5/raylib/wiki/Working-on-Windows#installing-and-building-raylib-via-vcpkg)
    ``` sh
    git clone https://github.com/Microsoft/vcpkg.git
    cd vcpkg
    bootstrap-vcpkg.bat
    vcpkg integrate install
    vcpkg install raylib
    ```
- Looked at output of `vcpkg` to get the path: `F:\vcpkg\packages\raylib_x64-windows\bin\raylib.dll`
- Reversed slashes to make a unix-friendly filepath and used to [init dart-raylib as seen in the example](https://gitlab.com/wolfenrain/dart-raylib/-/blob/a63cea5e7b61ac62ce7181bde1f93540b1728dc3/example/lib/main.dart)