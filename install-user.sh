#!/bin/bash
# Tarot CLI User Installation Script
# Downloads and installs the latest release from GitHub

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO="USERNAME/tarot-cli"  # Replace with actual GitHub repo
BINARY_NAME="tarot"

echo -e "${BLUE}Tarot CLI Installer${NC}"
echo "==================="

# Detect platform
OS=$(uname -s)
ARCH=$(uname -m)

case "$OS" in
    Linux*)
        PLATFORM="linux"
        INSTALL_DIR="/usr/local/bin"
        NEED_SUDO=true
        ;;
    Darwin*)
        PLATFORM="macos"
        INSTALL_DIR="/usr/local/bin"
        NEED_SUDO=true
        ;;
    CYGWIN*|MINGW*|MSYS*)
        PLATFORM="windows"
        INSTALL_DIR="$HOME/.local/bin"
        NEED_SUDO=false
        BINARY_NAME="tarot.exe"
        ;;
    *)
        echo -e "${RED}Error: Unsupported platform: $OS${NC}"
        exit 1
        ;;
esac

echo -e "${YELLOW}Detected platform: $PLATFORM${NC}"

# Get latest release URL
echo "Fetching latest release information..."
DOWNLOAD_URL="https://github.com/$REPO/releases/latest/download/tarot-$PLATFORM"

if [ "$PLATFORM" = "windows" ]; then
    DOWNLOAD_URL="${DOWNLOAD_URL}.exe"
fi

echo -e "${YELLOW}Download URL: $DOWNLOAD_URL${NC}"

# Create install directory for user installations
if [ "$NEED_SUDO" = false ] && [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Creating install directory: $INSTALL_DIR${NC}"
    mkdir -p "$INSTALL_DIR"
fi

# Download the binary
echo "Downloading tarot CLI..."
TEMP_FILE=$(mktemp)

if command -v curl >/dev/null 2>&1; then
    curl -L -o "$TEMP_FILE" "$DOWNLOAD_URL"
elif command -v wget >/dev/null 2>&1; then
    wget -O "$TEMP_FILE" "$DOWNLOAD_URL"
else
    echo -e "${RED}Error: Neither curl nor wget found. Please install one of them.${NC}"
    exit 1
fi

# Check if download was successful
if [ ! -s "$TEMP_FILE" ]; then
    echo -e "${RED}Error: Download failed or file is empty${NC}"
    echo "Please check that the release exists at: $DOWNLOAD_URL"
    rm -f "$TEMP_FILE"
    exit 1
fi

# Install the binary
echo "Installing tarot CLI..."
if [ "$NEED_SUDO" = true ]; then
    echo -e "${YELLOW}Installing to $INSTALL_DIR (requires sudo)${NC}"
    sudo cp "$TEMP_FILE" "$INSTALL_DIR/$BINARY_NAME"
    sudo chmod +x "$INSTALL_DIR/$BINARY_NAME"
else
    cp "$TEMP_FILE" "$INSTALL_DIR/$BINARY_NAME"
    chmod +x "$INSTALL_DIR/$BINARY_NAME"
fi

# Clean up
rm -f "$TEMP_FILE"

echo -e "${GREEN}✓ Tarot CLI installed to $INSTALL_DIR/$BINARY_NAME${NC}"

# Check PATH for non-sudo installs
if [ "$NEED_SUDO" = false ]; then
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        echo -e "${YELLOW}⚠ Warning: $INSTALL_DIR is not in your PATH${NC}"
        echo
        echo "To add it to your PATH, add this line to your shell profile:"
        echo "  export PATH=\"\$PATH:$INSTALL_DIR\""
        echo
        case "$SHELL" in
            */bash)
                echo "Run: echo 'export PATH=\"\$PATH:$INSTALL_DIR\"' >> ~/.bashrc"
                ;;
            */zsh)
                echo "Run: echo 'export PATH=\"\$PATH:$INSTALL_DIR\"' >> ~/.zshrc"
                ;;
            */fish)
                echo "Run: fish_add_path $INSTALL_DIR"
                ;;
            *)
                echo "Add to your shell's configuration file"
                ;;
        esac
        echo
        echo "Then restart your terminal or source your profile"
    else
        echo -e "${GREEN}✓ $INSTALL_DIR is already in your PATH${NC}"
    fi
fi

# Test installation
echo
echo "Testing installation..."
if "$INSTALL_DIR/$BINARY_NAME" --help > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Installation successful!${NC}"
    echo
    echo "Try it out:"
    echo "  $BINARY_NAME -s \"draw one\" -p \"What should I focus on today?\""
    echo "  $BINARY_NAME -s \"past present future\" -p \"Career guidance\""
else
    echo -e "${RED}✗ Installation test failed${NC}"
    echo "The binary may not be compatible with your system."
    exit 1
fi

echo
echo -e "${GREEN}Installation complete!${NC}"