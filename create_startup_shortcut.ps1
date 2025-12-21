$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('C:\Users\biren\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\OpenAgentsStartup.lnk')
$Shortcut.TargetPath = 'C:\Users\biren\Documents\trae_projects\ai\start_openagents.bat'
$Shortcut.WorkingDirectory = 'C:\Users\biren\Documents\trae_projects\ai'
$Shortcut.Save()
Write-Host "Shortcut created successfully!"
