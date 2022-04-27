# Hooking Windows 10 Calculator 64-bit

[![CI/CD](https://github.com/Siss3l/Calculaception/workflows/Pylint/badge.svg?branch=main)](https://github.com/Siss3l/Calculaception/actions/workflows/pylint.yml)

## Installation

[Windows Calculator](./local/Windows_Calculator_2020/install.ps1) must be installed to work knowing that it is not by default on **Windows Sandbox**.

## Requirement

**Python 3** needs the following latest packages to work:

-   [Frida](https://github.com/frida/frida-python)
-   [Loguru](https://github.com/Delgan/loguru)
-   [Psutil](https://github.com/giampaolo/psutil)
-   [PyYAML](https://github.com/yaml/pyyaml)
-   [Rich](https://github.com/Textualize/rich)

## Usage

Run the following command in order to be able to launch **Calculator** in **Calculator**:
```cmd
python.exe C:\Users\WDAGUtilityAccount\Desktop\local\payload\irc.py
```

There is the default relative path of `WindowsCalculator` editable.

See the [part](./local/payload/irc.py#L27) here:
```python
ex = r"explorer.exe shell:AppsFolder\Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"
```

## Configuration

You have to change the username **test** in the sandbox [configuration file](./local/config.wsb#L7) if you want to run it on **Windows Sandbox**.
```cmd
<HostFolder>C:\Users\test\Desktop\local</HostFolder>
```

![Version](https://i.imgur.com/DjFwYZn.png)

[Windows Sandbox](https://github.com/microsoft/Windows-Sandbox-Utilities) or a Virtual Machine (on **QEMU**, **VirtualBox**, **VMware**, etc.) can be used as a test environment inspected with `VirusTotal`.
