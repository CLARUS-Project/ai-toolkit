# Troubleshooting

## **System has not been booted with systemd as init system (PID 1). Can't operate** on WSL

1. Reboot WSL, in Admin PowerShell:

    ```powershell
    wsl --shutdown
    ```

2. Download the latest WSL version here: https://github.com/microsoft/WSL/releases

3. Add the package, in admin powershell:

    ```powershel
    Add-AppxPackage <path.to>/Microsoft.WSL_<version>_x64_ARM64.msixbundle
    ```

4. Update the wsl version, in powershell:

    ```powershell
    wsl --update
    ```

5. To enable Systemmd do this in wsl:

    ```bash
    sudo -e /etc/wsl.conf
    ```

    And paste this:

    ```
    [boot]
    systemd=true
    ```

6. Restart the wsl, on powershell:

    ```powershell
    wsl --shutdown
    ```

## failed to normalize token; must be in format K10\<CA-HASH\>::\<USERNAME\>:\<PASSWORD\> or \<PASS\>

When k3s server doesn't start it could be this error. to check it run this:
```bash
journalctl -u k3s.service | tail -n 100
```

To fix the error:
```bash
sudo rm -f /var/lib/rancher/k3s/server/token
```