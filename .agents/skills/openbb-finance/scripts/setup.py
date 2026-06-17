"""
OpenBB Setup Script
Automatically installs OpenBB and its dependencies.
"""
import subprocess
import sys

def install_package(package):
    """Install a Python package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package}: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and 9 <= version.minor <= 12:
        print("✓ Python version is compatible (3.9 - 3.12)")
        return True
    else:
        print("✗ Python version is not compatible. Requires Python 3.9 - 3.12")
        return False

def check_pip():
    """Check if pip is available."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✓ pip is available")
        return True
    except subprocess.CalledProcessError:
        print("✗ pip is not available")
        return False

def main():
    """Main setup function."""
    print("=" * 60)
    print("OpenBB Setup Script")
    print("=" * 60)
    print()
    
    # Check Python version
    if not check_python_version():
        print("\nPlease install Python 3.9 - 3.12")
        sys.exit(1)
    
    print()
    
    # Check pip
    if not check_pip():
        print("\nPlease install pip")
        sys.exit(1)
    
    print()
    
    # Packages to install
    packages = [
        ("openbb", "Main OpenBB platform"),
        ("pandas", "Data manipulation"),
        ("pandas-ta", "Technical analysis indicators"),
        ("matplotlib", "Visualization (optional)"),
    ]
    
    print("Installing packages:")
    print("-" * 60)
    
    success_count = 0
    for package, description in packages:
        print(f"\nInstalling {package} ({description})...")
        if install_package(package):
            success_count += 1
    
    print()
    print("=" * 60)
    print(f"Setup Complete: {success_count}/{len(packages)} packages installed")
    print("=" * 60)
    
    if success_count == len(packages):
        print("\n✓ All packages installed successfully!")
        print("\nYou can now use OpenBB:")
        print("  from openbb import obb")
        print("  output = obb.equity.price.historical('AAPL')")
        print("  df = output.to_dataframe()")
    else:
        print("\n⚠ Some packages failed to install. Please check errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()