powershell -command "&{Set-ExecutionPolicy RemoteSigned -force}"
cmd /c "C:\Users\WDAGUtilityAccount\Desktop\local\python3\python-3.10.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1"
cmd /c "copy C:\Users\WDAGUtilityAccount\Desktop\local\python3\frida-15.1.17-py3.10-win-amd64.egg C:\Users\WDAGUtilityAccount\frida-15.1.17-py3.10-win-amd64.egg"
cmd /c ""C:\Program Files\Python310\Scripts\pip.exe" install C:\Users\WDAGUtilityAccount\Desktop\local\python3\colorama-0.4.4.tar.gz"
cmd /c ""C:\Program Files\Python310\Scripts\pip.exe" install C:\Users\WDAGUtilityAccount\Desktop\local\python3\win32_setctime-1.1.0.tar.gz"
cmd /c ""C:\Program Files\Python310\Scripts\pip.exe" install C:\Users\WDAGUtilityAccount\Desktop\local\python3\Pygments-2.11.2.tar.gz"
cmd /c ""C:\Program Files\Python310\Scripts\pip.exe" install C:\Users\WDAGUtilityAccount\Desktop\local\python3\commonmark-0.9.1.tar.gz"
cmd /c ""C:\Program Files\Python310\Scripts\pip.exe" install C:\Users\WDAGUtilityAccount\Desktop\local\python3\frida-15.1.17.tar.gz"
cmd /c ""C:\Program Files\Python310\Scripts\pip.exe" install C:\Users\WDAGUtilityAccount\Desktop\local\python3\loguru-0.6.0-py3-none-any.whl"
cmd /c ""C:\Program Files\Python310\Scripts\pip.exe" install C:\Users\WDAGUtilityAccount\Desktop\local\python3\psutil-5.9.0-cp310-cp310-win_amd64.whl"
cmd /c ""C:\Program Files\Python310\Scripts\pip.exe" install C:\Users\WDAGUtilityAccount\Desktop\local\python3\PyYAML-6.0-cp310-cp310-win_amd64.whl"
cmd /c ""C:\Program Files\Python310\Scripts\pip.exe" install C:\Users\WDAGUtilityAccount\Desktop\local\python3\rich-12.0.0-py3-none-any.whl"
rem powershell C:\Users\WDAGUtilityAccount\Desktop\local\Windows_Calculator_2019\install.ps1
powershell C:\Users\WDAGUtilityAccount\Desktop\local\Windows_Calculator_2020\install.ps1
rem C:\Windows\System32\CExecSvc.exe directly closing CMD by force
cmd /c ""C:\Program Files\Python310\python.exe" C:\Users\WDAGUtilityAccount\Desktop\local\payload\irc.py"