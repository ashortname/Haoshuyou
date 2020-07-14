@echo off
echo.
title 初始化用户数据...[好书友统计中奖助手]
set /p account=请输入用户名：
set /p passwd=请输入密码：
set /p workMode=请输入起始页面：
cls
title 用户：%account% [好书友统计中奖助手]
echo 程序开始...
python countForAward.py %account% %passwd% %workMode%
pause