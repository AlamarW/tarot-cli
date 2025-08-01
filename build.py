#!/usr/bin/env python3
"""
Build script for creating tarot CLI executable using PyInstaller.
"""

import os
import subprocess
import sys
from pathlib import Path


def build_executable():
    """Build the tarot executable using PyInstaller."""

    # Ensure we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)

    # Clean previous builds
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"

    if dist_dir.exists():
        import shutil

        shutil.rmtree(dist_dir)
        print("Cleaned dist/ directory")

    if build_dir.exists():
        import shutil

        shutil.rmtree(build_dir)
        print("Cleaned build/ directory")

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create single executable
        "--name",
        "tarot",  # Name the executable 'tarot'
        "--clean",  # Clean PyInstaller cache
        "--noconfirm",  # Overwrite without asking
        "src/main.py",  # Entry point
    ]

    print("Building executable with PyInstaller...")
    print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(f"Executable created at: {dist_dir / 'tarot'}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False


def test_executable():
    """Test the built executable."""
    # On Windows, PyInstaller creates .exe files
    if sys.platform == "win32":
        executable = Path("dist/tarot.exe")
    else:
        executable = Path("dist/tarot")

    if not executable.exists():
        print("Executable not found!")
        return False

    print("\nTesting executable...")

    # Test help
    try:
        result = subprocess.run(
            [str(executable), "--help"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print("[OK] Help command works")
        else:
            print("[FAIL] Help command failed")
            return False
    except subprocess.TimeoutExpired:
        print("[FAIL] Help command timed out")
        return False

    # Test quick draw
    try:
        result = subprocess.run(
            [str(executable), "-s", "draw one", "-p", "test"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0 and "of" in result.stdout:
            print("[OK] Draw command works")
            print("[OK] Executable is functional")
            return True
        else:
            print("[FAIL] Draw command failed")
            print(f"stdout: {result.stdout}")
            print(f"stderr: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("[FAIL] Draw command timed out")
        return False


if __name__ == "__main__":
    print("Building tarot CLI executable...")

    if build_executable():
        if test_executable():
            print("\nBuild and test successful!")
            print("Executable ready at: dist/tarot")
        else:
            print("\nBuild succeeded but tests failed")
            sys.exit(1)
    else:
        print("\nBuild failed")
        sys.exit(1)

