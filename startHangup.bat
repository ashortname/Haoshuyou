@echo off
echo.
title ��ʼ���û�����...[�����ѹһ�����]
set /p account=�������û�����
set /p passwd=���������룺
cls
title �û���%account% [�����ѹһ�����]
echo ����ʼ...
python workHangup.py %account% %passwd% 0
pause