#NoEnv ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.

; For this script to work correctly, W:A must be using
; borderless windowed mode, the wkSuperFrontendHD module,
; and the following Windows Magnifier options must be set:
;   Change zoom level:
;   	 100% [Default]
;   Enable Magnifier to follow:
;   	 [Disable all]
;   Smooth edges of images and text:
;   	 Disable [recommended, unless you want anti-aliasing]
;   Keep the mouse cursor:
;   	 Within the edges of the screen
;   Keep the text cursor:
;   	 Within the edges of the screen

; SysGet, MonitorCount, MonitorCount
; SysGet, MonitorPrimary, MonitorPrimary
; MsgBox, Monitor Count:`t%MonitorCount%`nPrimary Monitor:`t%MonitorPrimary%
; Loop, %MonitorCount%
; {
;   SysGet, MonitorName, MonitorName, %A_Index%
;   SysGet, Monitor, Monitor, %A_Index%
;   SysGet, MonitorWorkArea, MonitorWorkArea, %A_Index%
;   MsgBox, Monitor:`t#%A_Index%`nName:`t%MonitorName%`nLeft:`t%MonitorLeft% (%MonitorWorkAreaLeft% work)`nTop:`t%MonitorTop% (%MonitorWorkAreaTop% work)`nRight:`t%MonitorRight% (%MonitorWorkAreaRight% work)`nBottom:`t%MonitorBottom% (%MonitorWorkAreaBottom% work)
; }

SysGet, PrimaryMonitor, Monitor
ResolutionX := PrimaryMonitorRight - PrimaryMonitorLeft
ResolutionY := PrimaryMonitorBottom - PrimaryMonitorTop
AnchorXPos := PrimaryMonitorLeft + (ResolutionX / 2)
AnchorYPos := PrimaryMonitorTop + (ResolutionY - 1)

isZoomed := false
#IfWinActive Worms Armageddon

  ^z::
    {
      if (isZoomed) {
        Send, #{NumpadSub}
        isZoomed := false
      } else {
        Send, ^g
        Sleep, 50
        MouseMove, %AnchorXPos%, %AnchorYPos%, 0
        Sleep, 50
        Send, #{NumpadAdd}
        Sleep, 250
        Click
        isZoomed := true
      }
      Return
    }
