# 1. Create pwcheck.bat (in your current folder)
@'
@echo off
python "%~dp0pwcheck.py" %*
'@ | Out-File -FilePath pwcheck.bat -Encoding ascii

# 2. TEST IT!
.\pwcheck.bat "password123"