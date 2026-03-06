@echo off
echo Attempting to fix UniFlowLMS Database...
venv\Scripts\python.exe manage.py migrate core --noinput
echo If you see 'OK' above, the fix worked.
echo.
pause
