#!/bin/bash
# Tarot CLI Uninstallation Script for Linux/Mac

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="$HOME/.local/bin"
BINARY_NAME="tarot"
BINARY_PATH="$INSTALL_DIR/$BINARY_NAME"

echo -e "${BLUE}Tarot CLI Uninstaller${NC}"
echo "====================="

# Check if binary exists
if [ ! -f "$BINARY_PATH" ]; then
    echo -e "${YELLOW}Tarot CLI is not installed at $BINARY_PATH${NC}"
    echo "Nothing to uninstall."
    exit 0
fi

# Remove the binary
echo -e "${YELLOW}Removing $BINARY_PATH...${NC}"
rm -f "$BINARY_PATH"

if [ ! -f "$BINARY_PATH" ]; then
    echo -e "${GREEN}✓ Tarot CLI successfully uninstalled${NC}"
else
    echo -e "${RED}✗ Failed to remove $BINARY_PATH${NC}"
    exit 1
fi

# Note about PATH
echo
echo -e "${BLUE}Note:${NC} If you manually added $INSTALL_DIR to your PATH,"
echo "you may want to remove it from your shell profile (~/.bashrc or ~/.zshrc)"
echo "if you don't have other binaries installed there."