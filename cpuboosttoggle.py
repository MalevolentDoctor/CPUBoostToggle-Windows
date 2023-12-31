import os
import psutil
import time
import win32com.client

#find the active scheme
_scheme = os.popen("powercfg.exe /GETACTIVESCHEME")
scheme = _scheme.read()
start_scheme = scheme.find(':') + 1
end_scheme = scheme.find('(')
active_scheme = scheme[start_scheme:end_scheme].strip()

#query the active scheme
s1 = " 54533251-82be-4824-96c1-47b60b740d00"
s2 = " be337238-0d82-4146-a960-4f3749d470c7"
_query = os.popen("powercfg.exe /QUERY " + active_scheme + s1 + s2)
query = _query.read()

#find the state of the AC and DC modes
query_ac = query.find("Current AC Power Setting Index:") + 32
query_dc = query.find("Current DC Power Setting Index:") + 32
ac_state = query[query_ac:query_ac+10]
dc_state = query[query_dc:query_dc+10]
ac_boost_disabled = ac_state == "0x00000000"
dc_boost_disabled = dc_state == "0x00000000"

#get the state of the battery
battery_status = psutil.sensors_battery()

#set the power state
try:
    if battery_status.power_plugged:
        print("ROG ALLY is plugged in")
        if ac_boost_disabled:
            print("Enabling CPU Boost")
            os.system('powercfg.exe /SETACVALUEINDEX ' + active_scheme + s1 + s2 + ' 002')
            ac_boost_disabled = False
        else:
            print("Disabling CPU Boost")
            os.system('powercfg.exe /SETACVALUEINDEX ' + active_scheme + s1 + s2 + ' 000')
            ac_boost_disabled = True
    else:
        print("ROG ALLY is running on battery")
        if dc_boost_disabled:
            print("Enabling CPU Boost")
            os.system('powercfg.exe /SETDCVALUEINDEX ' + active_scheme + s1 + s2 + ' 002')
            dc_boost_disabled = False
        else:
            print("Disabling CPU Boost")
            os.system('powercfg.exe /SETDCVALUEINDEX ' + active_scheme + s1 + s2 + ' 000')
            dc_boost_disabled = True
except:
    print("Error: Battery not detected")
    time.sleep(3)
    exit


#apply changes
os.system('powercfg.exe -S SCHEME_CURRENT')

# ---- change icon ---- #
cd = os.getcwd()
desktop = os.path.expanduser("~\\Desktop")

#get the icon name
ac = "r"
dc = "r"
if not ac_boost_disabled: ac = "g"
if not dc_boost_disabled: dc = "g"
icon_name = ac + dc + ".ico"

#create shortcut
shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortcut("CPUBoostToggle.lnk")
shortcut.TargetPath = cd + "\\run.bat"
shortcut.IconLocation = cd + "\\icons\\" + icon_name + ",0"
shortcut.Save()

#replace old shortcut
try:
    os.replace(cd + "\\CPUBoostToggle.lnk", desktop + "\\CPUBoostToggle.lnk")
except:
    print("Error: Desktop not found in expected location (C:/Users/[your username]/Desktop)")
    time.sleep(3)
    exit