@echo off
echo.
title ��ʼ���û�����...[�����ѻ�������]
set /p account=�������û�����
set /p passwd=���������룺
echo [����ģʽ��0 �����ٻظ����������κ��û���]
echo [����ģʽ��1 ��������״Ԫ�����û���]
echo [����ģʽ��2 ��������״Ԫ�����û���]
set /p workMode=�����빤��ģʽ��
cls
title �û���%account% [�����ѻ�������]
echo ����ʼ...
python work.py %account% %passwd% %workMode%
pause