#!/bin/bash
# Tarot CLI Installation Script for Linux/Mac

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

echo -e "${BLUE}Tarot CLI Installer${NC}"
echo "==================="

# Create install directory if it doesn't exist
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Creating install directory: $INSTALL_DIR${NC}"
    mkdir -p "$INSTALL_DIR"
fi

# Check if we're installing from local build or downloading
if [ -f "dist/tarot" ]; then
    echo -e "${GREEN}Installing from local build...${NC}"
    cp "dist/tarot" "$INSTALL_DIR/$BINARY_NAME"
else
    echo -e "${RED}Error: No tarot executable found in dist/tarot${NC}"
    echo "Please run 'uv run python build.py' first to build the executable."
    exit 1
fi

# Make executable
chmod +x "$INSTALL_DIR/$BINARY_NAME"

echo -e "${GREEN}✓ Tarot CLI installed to $INSTALL_DIR/$BINARY_NAME${NC}"

# Check if install directory is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo -e "${YELLOW}⚠ Warning: $INSTALL_DIR is not in your PATH${NC}"
    echo
    echo "To add it to your PATH, add this line to your shell profile:"
    echo "  export PATH=\"\$PATH:$INSTALL_DIR\""
    echo
    echo "For bash: echo 'export PATH=\"\$PATH:$INSTALL_DIR\"' >> ~/.bashrc"
    echo "For zsh:  echo 'export PATH=\"\$PATH:$INSTALL_DIR\"' >> ~/.zshrc"
    echo
    echo "Then restart your terminal or run: source ~/.bashrc (or ~/.zshrc)"
else
    echo -e "${GREEN}✓ $INSTALL_DIR is already in your PATH${NC}"
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
    exit 1
fi