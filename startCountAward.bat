@echo off
echo.
title ��ʼ���û�����...[������ͳ���н�����]
set /p account=�������û�����
set /p passwd=���������룺
set /p workMode=��������ʼҳ�棺
cls
title �û���%account% [������ͳ���н�����]
echo ����ʼ...
python countForAward.py %account% %passwd% %workMode%
pause