@echo off
echo.
title 初始化用户数据...[好书友回帖助手]
set /p account=请输入用户名：
set /p passwd=请输入密码：
echo [工作模式：0 ，快速回复，适用于任何用户组]
echo [工作模式：1 ，适用于状元以下用户组]
echo [工作模式：2 ，适用于状元以上用户组]
set /p workMode=请输入工作模式：
cls
title 用户：%account% [好书友回帖助手]
echo 程序开始...
python work.py %account% %passwd% %workMode%
pause