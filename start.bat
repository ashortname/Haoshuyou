@echo off
echo.
title ��ʼ���û�����...[�����ѻ�������]
set /p account=�������û�����
set /p passwd=���������룺
cls
title �û���%account% [�����ѻ�������]
echo ����ʼ...
python work.py %account% %passwd% 0
pause