@echo off
echo.
set /p account=请输入用户名：
set /p passwd=请输入密码：
cls
title %account%
echo 程序开始...
python work.py %account% %passwd% 0
pause