'Define path variables
exe_directory = "C:\Phoenix\PhoenixMiner"
exe_filename = "PhoenixMiner.exe"
oc_exe_directory = "C:\Phoenix"
oc_exe_filename = "OverdriveNTool.bat"

'======== Script start ========'

'Get shell object for executing commands and reading/writing reg values
Dim WSh
Set WSh = WScript.CreateObject("WScript.shell")

'Change dir to exe dir
WSh.CurrentDirectory = exe_directory

'ASCII decimal 34 = "
quot = chr(34)

'Encapsulate path strings in quotes and build full exe path
exe_path = quot & exe_directory & "\" & exe_filename & quot
oc_exe_path = quot & oc_exe_directory & "\" & oc_exe_filename & quot

'Execute specified file and wait until exit (True). 1 = vbNormalFocus
While (True)
    WScript.Echo exe_filename & " starting at " & Now
    WSh.Run oc_exe_path, 1, False
    WSh.Run exe_path, 2, True
    WScript.Echo exe_filename & " closed at " & Now
    WScript.Sleep(5000)
Wend

'Exit with success return (0)
' Set WShell = Nothing
' WScript.Quit(0)
