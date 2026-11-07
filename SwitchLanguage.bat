@echo off
chcp 936 >nul
setlocal
set "INI=%~dp0KidGame\Config\KidEngine.ini"
if not exist "%INI%" (
  echo [ERROR] KidEngine.ini not found:
  echo   %INI%
  echo Put this bat in the game root, next to the KidGame folder.
  pause
  exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -Command "$p='%INI%'; $e=[Text.Encoding]::GetEncoding(28591); $s=$e.GetString([IO.File]::ReadAllBytes($p)); if($s -match 'Language=INT'){ $s=$s.Replace('Language=INT','Language=JPN'); $m='Traditional Chinese (JPN slot)' } else { $s=$s.Replace('Language=JPN','Language=INT'); $m='Simplified Chinese (INT slot)' }; [IO.File]::WriteAllBytes($p,$e.GetBytes($s)); Write-Host ('Language -> ' + $m)"
echo.
echo Done. Start the game to apply.
pause
