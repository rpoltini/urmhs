set OSGEO4W_ROOT=C:\Program Files\QGIS 3.16

call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
call "%OSGEO4W_ROOT%\bin\qt5_env.bat"
call "%OSGEO4W_ROOT%\bin\py3_env.bat"

path %OSGEO4W_ROOT%\apps\bin;%OSGEO4W_ROOT%\apps\grass\grass76\lib;%OSGEO4W_ROOT%\apps\grass\grass76\bin;%PATH%

cd /d %~dp0

@ECHO ON
call pyuic5 --from-imports -o urmhs_set_history_date_ui.py urmhs_set_history_date.ui
call pyuic5 --from-imports -o urmhs_wrk_session_create_ui.py urmhs_wrk_session_create.ui
call pyuic5 --from-imports -o urmhs_layers_ui.py urmhs_layers.ui
call pyuic5 --from-imports -o urmhs_wrk_session_list_ui.py urmhs_wrk_session_list.ui
call pyuic5 --from-imports -o urmhs_user_confirm_ui.py urmhs_user_confirm.ui
call pyuic5 --from-imports -o urmhs_wrk_session_details_ui.py urmhs_wrk_session_details.ui
call pyuic5 --from-imports -o urmhs_enable_stack_ui.py urmhs_enable_stack.ui
call pyuic5 --from-imports -o urmhs_user_list_ui.py urmhs_user_list.ui
call pyuic5 --from-imports -o urmhs_user_ui.py urmhs_user.ui
call pyuic5 --from-imports -o urmhs_dbconnection_list_ui.py urmhs_dbconnection_list.ui
call pyuic5 --from-imports -o urmhs_set_executer_ui.py urmhs_set_executer.ui