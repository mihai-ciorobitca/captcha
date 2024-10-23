@echo off
setlocal

set i=1
:loop
curl -o "output$i.png" "https://famdev.ro/captcha.php"
set /a i+=1
goto loop
