<div align="center">

# Hooking Windows 10 Calculator 64-bit in Python 3

[![CI/CD](https://github.com/Siss3l/Calculaception/workflows/Pylint/badge.svg?branch=main)](https://github.com/Siss3l/Calculaception/actions/workflows/pylint.yml)
[![CI/CD](https://github.com/Siss3l/Calculaception/workflows/PythonCI/badge.svg?branch=main)](https://github.com/Siss3l/Calculaception/actions/workflows/ci.yml)
[![Known_Vulnerabilities](https://snyk.io/test/github/Siss3l/Calculaception/badge.svg?branch=main)](https://snyk.io/test/github/Siss3l/Calculaception)

</div>

## ⚖️ Disclaimer

> **The code within this repository comes with no guarantee, the use of this code is your responsibility.
Author(s) have no responsibility/liability for how you choose to use any of the source code available here.
By using any of the files available in this repository, you understand that you are agreeing to use at your own risk.
Once again, all files available here are for education/research purposes only.**

## 🧩 Installation

[**Windows Calculator**](./local/Windows_Calculator_2020/install.ps1) must be installed to work, knowing that it is not by default on [**Windows Sandbox**](https://github.com/microsoft/Windows-Sandbox-Utilities).

## ✨ Prerequisite

**Python 3** needs the following packages:

-   [Frida](https://github.com/frida/frida-python) (main package)
-   [Loguru](https://github.com/Delgan/loguru)
-   [Psutil](https://github.com/giampaolo/psutil)
-   [Rich](https://github.com/Textualize/rich)

## 🚀 Usage

Run one of the following commands in order to be able to start a **Calculator** process in **Calculator** by clicking on their **Send feedback** button:
```cmd
python .\local\payload\irc.py

python.exe C:\Users\WDAGUtilityAccount\Desktop\local\payload\irc.py
```

There is a default relative path of `WindowsCalculator` editable.\
See this [part](./local/payload/irc.py#L44) here:
```python
r"explorer.exe shell:AppsFolder\Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"
```

## ⚙ Configuration

If you want to use the default configuration, you have to change the username **test** by yours in the sandbox [configuration file](./local/config.wsb#L7) to run it correctly on **Windows Sandbox** environment.
```cmd
<HostFolder>C:\Users\test\Desktop\local</HostFolder>
```

Functional tested versions on **Calculator** are:

-   `10.2103.8.0`
-   `10.1804.11545.0`

There are also several alternatives to run a **Calculator** application:
-   [Windows Sandbox](https://github.com/microsoft/Windows-Sandbox-Utilities) with prior installation of **Calculator**
-   A Virtual Machine ([QEMU](https://github.com/qemu/qemu), [VirtualBox](https://github.com/mirror/vbox), [VMware](https://github.com/vmware/open-vm-tools), etc.) can be used as a test environment, including [Windows 10 ISO](https://www.microsoft.com/en-us/software-download/windows10) possibly inspected with [VirusTotal](https://github.com/VirusTotal/vt-cli)
-   Usage of [Wine](https://github.com/wine-mirror/wine) allowing to launch **Windows** applications (without adding [HyperV](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v), [FlareVM](https://github.com/mandiant/flare-vm) or [HiddenVM](https://github.com/aforensics/HiddenVM))
-   [Uno Platform](https://github.com/unoplatform/calculator) should also be adapted to the needs
