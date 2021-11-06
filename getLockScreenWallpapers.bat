:: Batch script to extract wallpapers from Windows 10's lock screens
:: This will attempt to create a temp folder, extract wallpapers
:: and place them inside a "Wallpapers" folder in the
:: current directory.

setlocal
:: Avoid copying junk files by setting minimum size to 400KB
set min.size=409600
:: Set temp name by concatenating temp-date-time, ommit /'s and :'s
set tempfoldername=temp%DATE:/=%%TIME::=%
:: Also omit .'s
set tempfoldername=%tempfoldername:.=%
md %tempfoldername%
:: Copy only the files bigger than the minimum size
robocopy %LOCALAPPDATA%\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets %tempfoldername% /min:%min.size%
:: Add .jpg extension to all copied files
cd %tempfoldername%
ren *.* *.jpg
cd ..
md Wallpapers
move ""%tempfoldername%\* Wallpapers
rd %tempfoldername%
@echo Done! :D