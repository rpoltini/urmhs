set OSGEO4W_ROOT=C:\Program Files\QGIS 3.16

call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
call "%OSGEO4W_ROOT%\bin\qt5_env.bat"
call "%OSGEO4W_ROOT%\bin\py3_env.bat"

path %OSGEO4W_ROOT%\apps\bin;%OSGEO4W_ROOT%\apps\grass\grass76\lib;%OSGEO4W_ROOT%\apps\grass\grass76\bin;%PATH%

cd /d %~dp0

@ECHO ON
call pyrcc5 -o urmhs_rc.py urmhs.qrc