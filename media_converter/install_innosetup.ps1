# Download InnoSetup
$url = "https://files.jrsoftware.org/is/6/innosetup-6.2.2.exe"
$output = "innosetup-installer.exe"
Invoke-WebRequest -Uri $url -OutFile $output

# Install InnoSetup silently
Start-Process -FilePath $output -ArgumentList "/VERYSILENT" -Wait

# Clean up
Remove-Item $output
