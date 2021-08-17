'Define desired variables
exe_directory = "C:\Program Files (x86)\Steam\steamapps\common\Worms Armageddon"
exe_filename = "WA.exe"
res_x = 800
res_y = 600

'======== Script start ========

'Quit with error return (1) if not a .WAgame file
replay_file = WScript.Arguments(0)
If right(replay_file, 7) <> ".WAgame" Then
    WScript.echo "Not a .WAgame file, quitting..."
    WScript.Quit(1)
End If

'Get shell object for executing commands and reading/writing reg values
Dim WSh
Set WSh = WScript.CreateObject("WScript.shell")

'Change dir to WA exe dir
WSh.CurrentDirectory = exe_directory

'ASCII decimal 34 = "
quot = chr(34)

'Encapsulate path strings in quotes and build full WA exe path
replay_file = quot & replay_file & quot
exe_path = quot & exe_directory & "\" & exe_filename & quot

'WA options key path and values types
reg_key_path = "HKEY_CURRENT_USER\Software\Team17SoftwareLTD\WormsArmageddon\Options"
reg_value_type = "REG_DWORD"

'Get previous values from options key and set new ones
prev_res_x = WSh.RegRead(reg_key_path & "\DisplayXSize")
WSh.RegWrite reg_key_path & "\DisplayXSize", res_x, reg_value_type

prev_res_y = WSh.RegRead(reg_key_path & "\DisplayYSize")
WSh.RegWrite reg_key_path & "\DisplayYSize", res_y, reg_value_type

'Build WA play command
wa_play_cmd = exe_path & " /play " & replay_file

'Play specified replay file with WA and wait until exit (True). 1 = vbNormalFocus
WSh.Run wa_play_cmd, 1, True

'Restore old reg values
WSh.RegWrite reg_key_path & "\DisplayXSize", prev_res_x, reg_value_type
WSh.RegWrite reg_key_path & "\DisplayYSize", prev_res_y, reg_value_type

'Exit with success return (0)
WScript.Quit(0)