Write-Host " "
Write-Host " "
$swList = Get-WmiObject -Class Win32_Product | Select-Object -Property Name
if ($swList.Name|Select-String "emet")
{
	$emetVersion = ($swList.Name|Select-String "emet")
	Write-Host "EMET found: $emetVersion" -foregroundcolor "green"
}
else
{
	Write-Host "No EMET found." -background "black" -foreground "red"
}

Write-Host " "
$ieVersion = New-Object -TypeName System.Version -ArgumentList (
    Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Internet Explorer').Version
$ieVersion = New-Object -TypeName System.Version -ArgumentList (
    # switch major and minor
    $ieVersion.Minor, $ieVersion.Major, $ieVersion.Build, $ieVersion.Revision)
if ($ieVersion.Major -lt 11)
{
    Write-Host "Internet Explorer 11 or later required. Installed version is $ieVersion" -foreground "red"
}
else
{
	Write-Host "Installed IE is $ieVersion" -foregroundcolor "green"
}
Write-Host " "
$flashVersion = Get-ItemProperty 'HKLM:\SOFTWARE\Macromedia\FlashPlayer'

if (($flashVersion.CurrentVersion - 0) -lt 2000267)
{
	Write-Host "Flash Player is out of date. Installed version is $($flashVersion.CurrentVersion)" -foreground "red"
}
else
{
	Write-Host "Installed Flash Player is $($flashVersion.CurrentVersion)" -foregroundcolor "green"
}
Write-Host " "

$winVersion = [System.Environment]::OSVersion.Version
if ($winVersion.Major -gt 6)
{
	Write-Host "Running something newer than 8.1" -foreground "red"
}
elseif ($winVersion.Major -eq 6)
{
	if ($winVersion.Minor -eq 0)
	{
		Write-Host "Windows Vista? How are you even alive?" -foreground "red"
	}
	elseif ($winVersion.Minor -eq 1)
	{
		Write-Host "Windows 7 - time for a major upgrade." -foreground "red"
	}
	elseif ($winVersion.Minor -eq 2)
	{
		Write-Host "Windows 8, but needs to be updated to 8.1" -foreground "red"
	}
	elseif ($winVersion.Minor -eq 3)
	{
		Write-Host "Running Windows 8.1" -foregroundcolor "green"
	}
}
elseif ($winVersion.Major -lt 6)
{
Write-Host "Running XP or older. You are likely to be eaten by a Grue." -foreground "red"
}
else
{
	Write-Host "Cannot determine your OS version." -foreground "red" 
}

Write-Host " "
if (([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
	if (manage-bde -status c:|Select-String "Unlocked")
	{
		Write-Host "BitLocker not active. Check for Seagate FDE by rebooting into BIOS." -foreground "yellow"
	}
	else 
	{
		manage-bde -status
	}
}
else
{
	Write-Host "Not running as Administrator, cannot check BitLocker status." -foreground "red"
}
Write-Host " "
Write-Host " "

Set-ExecutionPolicy Restricted

