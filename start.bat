@echo off
echo.
title 初始化用户数据...[好书友回帖助手]
set /p account=请输入用户名：
set /p passwd=请输入密码：
cls
title 用户：%account% [好书友回帖助手]
echo 程序开始...
python work.py %account% %passwd% 0
pause