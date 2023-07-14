@echo off

Set Shortcut=CPUBoostToggle.lnk
echo set WshShell = WScript.CreateObject("WScript.Shell")>DecodeShortCut.vbs
echo set Lnk = WshShell.CreateShortcut(WScript.Arguments.Unnamed(0))>>DecodeShortCut.vbs
echo wscript.Echo Lnk.TargetPath>>DecodeShortCut.vbs
set vbscript=cscript //nologo DecodeShortCut.vbs
For /f "delims=" %%T in ( ' %vbscript% "%Shortcut%" ' ) do set target=%%T
del DecodeShortCut.vbs

if NOT "%target%" == "" (
	cd "%target:~0,-8%"
)

if exist install_reqs.bat (
	CALL install_reqs.bat
)

python cpuboosttoggle.py

pause