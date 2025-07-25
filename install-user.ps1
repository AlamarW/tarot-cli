# Tarot CLI User Installation Script for Windows
# Downloads and installs the latest release from GitHub

# Enable strict error handling
$ErrorActionPreference = "Stop"

# Configuration
$REPO = "AlamarW/tarot-cli"  # Replace with actual GitHub repo
$BINARY_NAME = "tarot.exe"
$INSTALL_DIR = "$env:USERPROFILE\.local\bin"

# Color functions for output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Info($message) { Write-ColorOutput Blue $message }
function Write-Success($message) { Write-ColorOutput Green $message }
function Write-Warning($message) { Write-ColorOutput Yellow $message }
function Write-Error($message) { Write-ColorOutput Red $message }

Write-Info "Tarot CLI Installer"
Write-Info "==================="

Write-Warning "Detected platform: Windows"

# Get latest release URL
Write-Info "Fetching latest release information..."
$DOWNLOAD_URL = "https://github.com/$REPO/releases/latest/download/tarot-windows.exe"
Write-Warning "Download URL: $DOWNLOAD_URL"

# Create install directory
if (!(Test-Path $INSTALL_DIR)) {
    Write-Warning "Creating install directory: $INSTALL_DIR"
    New-Item -ItemType Directory -Path $INSTALL_DIR -Force | Out-Null
}

# Download the binary
Write-Info "Downloading tarot CLI..."
$TEMP_FILE = [System.IO.Path]::GetTempFileName()

try {
    Invoke-WebRequest -Uri $DOWNLOAD_URL -OutFile $TEMP_FILE -UseBasicParsing
} catch {
    Write-Error "Error: Download failed"
    Write-Error "Please check that the release exists at: $DOWNLOAD_URL"
    Write-Error "Error details: $($_.Exception.Message)"
    Remove-Item $TEMP_FILE -ErrorAction SilentlyContinue
    exit 1
}

# Check if download was successful
if ((Get-Item $TEMP_FILE).Length -eq 0) {
    Write-Error "Error: Download failed or file is empty"
    Write-Error "Please check that the release exists at: $DOWNLOAD_URL"
    Remove-Item $TEMP_FILE -ErrorAction SilentlyContinue
    exit 1
}

# Install the binary
Write-Info "Installing tarot CLI..."
$INSTALL_PATH = Join-Path $INSTALL_DIR $BINARY_NAME
Copy-Item $TEMP_FILE $INSTALL_PATH -Force

# Clean up
Remove-Item $TEMP_FILE

Write-Success "✓ Tarot CLI installed to $INSTALL_PATH"

# Check PATH
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($userPath -notlike "*$INSTALL_DIR*") {
    Write-Warning "⚠ Warning: $INSTALL_DIR is not in your PATH"
    Write-Info ""
    Write-Info "To add it to your PATH:"
    Write-Info "1. Press Win+R, type 'sysdm.cpl', press Enter"
    Write-Info "2. Click 'Environment Variables'"
    Write-Info "3. Under 'User variables', select 'Path' and click 'Edit'"
    Write-Info "4. Click 'New' and add: $INSTALL_DIR"
    Write-Info "5. Click OK to save"
    Write-Info ""
    Write-Info "Or run this PowerShell command as Administrator:"
    Write-Info "`$userPath = [Environment]::GetEnvironmentVariable('PATH', 'User')"
    Write-Info "[Environment]::SetEnvironmentVariable('PATH', `"`$userPath;$INSTALL_DIR`", 'User')"
    Write-Info ""
    Write-Info "Then restart your terminal"
} else {
    Write-Success "✓ $INSTALL_DIR is already in your PATH"
}

# Test installation
Write-Info ""
Write-Info "Testing installation..."
try {
    & $INSTALL_PATH --help | Out-Null
    Write-Success "✓ Installation successful!"
    Write-Info ""
    Write-Info "Try it out:"
    Write-Info "  tarot -s `"draw one`" -p `"What should I focus on today?`""
    Write-Info "  tarot -s `"past present future`" -p `"Career guidance`""
} catch {
    Write-Error "✗ Installation test failed"
    Write-Error "The binary may not be compatible with your system."
    Write-Error "Error: $($_.Exception.Message)"
    exit 1
}

Write-Info ""
Write-Success "Installation complete!"
