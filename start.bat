@echo off
echo.
set /p account=�������û�����
set /p passwd=���������룺
cls
title %account%
echo ����ʼ...
python work.py %account% %passwd% 0
pause