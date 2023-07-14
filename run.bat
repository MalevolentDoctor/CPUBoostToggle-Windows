@echo off

if exist install_reqs.bat (
	CALL install_reqs.bat
)

python cpuboosttoggle.py