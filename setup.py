#!/usr/bin/env python3
"""
Automated setup script for Multi-Agent Translation Semantic Drift Experiment.

This script:
1. Checks for required dependencies
2. Attempts to download the embedding model
3. Handles SSL certificate errors automatically
4. Falls back to Git LFS clone if needed
5. Validates the installation
6. Provides clear user guidance

Run this before first use:
    python3 setup.py

Or with options:
    python3 setup.py --force      # Force re-download
    python3 setup.py --check-only # Just check status
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Tuple, Optional

# ANSI color codes for pretty output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print a header."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*80}{Colors.END}\n")

def print_step(num: int, text: str):
    """Print a step."""
    print(f"{Colors.BOLD}{Colors.CYAN}[Step {num}]{Colors.END} {text}")

def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def check_python_version() -> bool:
    """Check if Python version is adequate."""
    if sys.version_info < (3, 8):
        print_error(f"Python 3.8+ required, you have {sys.version}")
        return False
    print_success(f"Python version: {sys.version.split()[0]}")
    return True


def check_pip_packages() -> Tuple[bool, list]:
    """Check if required packages are installed."""
    required = [
        'sentence-transformers',
        'torch',
        'numpy',
        'scipy',
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print_warning(f"Missing packages: {', '.join(missing)}")
        return False, missing
    else:
        print_success("All required packages installed")
        return True, []


def install_requirements() -> bool:
    """Install requirements from requirements.txt."""
    req_file = Path(__file__).parent / 'requirements.txt'
    
    if not req_file.exists():
        print_error("requirements.txt not found")
        return False
    
    print_info("Installing requirements...")
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', str(req_file)],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print_success("Requirements installed successfully")
            return True
        else:
            print_error(f"pip install failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print_error("Installation timed out (>5 minutes)")
        return False
    except Exception as e:
        print_error(f"Installation failed: {e}")
        return False


def check_git_lfs() -> bool:
    """Check if Git LFS is installed."""
    try:
        result = subprocess.run(
            ['git', 'lfs', 'version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print_success(f"Git LFS installed: {result.stdout.strip()}")
            return True
        else:
            print_warning("Git LFS not installed")
            return False
    except FileNotFoundError:
        print_warning("Git not found")
        return False
    except Exception as e:
        print_warning(f"Could not check Git LFS: {e}")
        return False


def install_git_lfs() -> bool:
    """Try to install/initialize Git LFS."""
    print_info("Attempting to initialize Git LFS...")
    try:
        result = subprocess.run(
            ['git', 'lfs', 'install'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print_success("Git LFS initialized")
            return True
        else:
            print_warning("Git LFS initialization failed (may already be initialized)")
            return True  # Not fatal
    except Exception as e:
        print_warning(f"Git LFS setup failed: {e}")
        return False


def get_model_path() -> Path:
    """Get the model installation path."""
    # Check environment variable
    env_path = os.environ.get('MODEL_LOCAL_PATH')
    if env_path:
        return Path(env_path).expanduser()
    
    # Default to ~/models/all-MiniLM-L6-v2
    return Path.home() / 'models' / 'all-MiniLM-L6-v2'


def check_model_exists(model_path: Path) -> bool:
    """Check if model already exists and is valid."""
    if not model_path.exists():
        return False
    
    # Check for essential files
    required_files = [
        'config.json',
        'pytorch_model.bin',
        'tokenizer.json',
        'modules.json'
    ]
    
    missing = [f for f in required_files if not (model_path / f).exists()]
    
    if missing:
        print_warning(f"Model directory exists but missing files: {', '.join(missing)}")
        return False
    
    print_success(f"Model found at: {model_path}")
    return True


def download_model_via_git(model_path: Path) -> bool:
    """Download model using Git LFS (bypasses SSL API issues)."""
    print_info(f"Downloading model to: {model_path}")
    print_info("This may take several minutes (930MB download)...")
    
    # Create parent directory
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Clone repository
    repo_url = 'https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2'
    
    try:
        result = subprocess.run(
            ['git', 'clone', repo_url, str(model_path)],
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes max
        )
        
        if result.returncode == 0:
            print_success("Model downloaded successfully via Git!")
            return True
        else:
            print_error(f"Git clone failed: {result.stderr}")
            
            # Check if it's an SSL error
            if 'ssl' in result.stderr.lower() or 'certificate' in result.stderr.lower():
                print_error("SSL certificate error detected during git clone")
                print_info("Your network may be blocking Git HTTPS as well")
                return False
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Download timed out (>10 minutes)")
        return False
    except FileNotFoundError:
        print_error("Git not found. Please install Git first.")
        return False
    except Exception as e:
        print_error(f"Download failed: {e}")
        return False


def download_model_via_python(model_path: Path) -> Tuple[bool, bool]:
    """
    Try to download model via Python API.
    
    Returns:
        (success: bool, ssl_error: bool)
    """
    print_info("Attempting to download model via HuggingFace API...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # Try to download and save
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Save to our local path
        model.save(str(model_path))
        
        print_success("Model downloaded via Python API!")
        return True, False
        
    except ImportError:
        print_error("sentence-transformers not installed")
        return False, False
        
    except Exception as e:
        error_str = str(e).lower()
        is_ssl = any(kw in error_str for kw in ['ssl', 'certificate', 'cert'])
        
        if is_ssl:
            print_warning("SSL certificate error detected")
            return False, True
        else:
            print_error(f"Download failed: {e}")
            return False, False


def validate_model(model_path: Path) -> bool:
    """Validate that the model works."""
    print_info("Validating model...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        model = SentenceTransformer(str(model_path))
        
        # Test encoding
        test_text = "Hello world"
        embedding = model.encode(test_text)
        
        if embedding is not None and len(embedding) == 384:
            print_success(f"Model validated! Embedding dimension: {len(embedding)}")
            return True
        else:
            print_error(f"Model validation failed: unexpected embedding shape")
            return False
            
    except Exception as e:
        print_error(f"Model validation failed: {e}")
        return False


def create_env_file(model_path: Path):
    """Create .env file with model path."""
    env_file = Path(__file__).parent / '.env'
    
    content = f"""# Auto-generated by setup.py
# Model configuration
MODEL_LOCAL_PATH={model_path}
HF_HUB_OFFLINE=1

# To use online mode, set:
# HF_HUB_OFFLINE=0
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(content)
        print_success(f"Created .env file: {env_file}")
    except Exception as e:
        print_warning(f"Could not create .env file: {e}")


def print_next_steps():
    """Print next steps for the user."""
    print_header("🎉 SETUP COMPLETE!")
    
    print(f"{Colors.BOLD}Next steps:{Colors.END}\n")
    print("1. Test the model loader:")
    print(f"   {Colors.CYAN}python3 model_loader.py{Colors.END}\n")
    print("2. Run a quick test:")
    print(f"   {Colors.CYAN}python3 scripts/calculate_distance.py \"hello world\" \"hi earth\"{Colors.END}\n")
    print("3. Try the interactive analyzer:")
    print(f"   {Colors.CYAN}python3 run_interactive.py{Colors.END}\n")
    print("4. Explore the experiment results:")
    print(f"   {Colors.CYAN}python3 simple_demo.py{Colors.END}\n")
    print(f"{Colors.GREEN}The project is now ready to use!{Colors.END}")


def print_troubleshooting():
    """Print troubleshooting guide."""
    print_header("❓ TROUBLESHOOTING")
    
    print("If setup failed, try these solutions:\n")
    print(f"{Colors.BOLD}1. SSL Certificate Issues:{Colors.END}")
    print("   - Switch to home WiFi (not corporate/school network)")
    print("   - Or manually download:")
    print(f"     {Colors.CYAN}git lfs install{Colors.END}")
    print(f"     {Colors.CYAN}mkdir -p ~/models{Colors.END}")
    print(f"     {Colors.CYAN}cd ~/models{Colors.END}")
    print(f"     {Colors.CYAN}git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2{Colors.END}\n")
    
    print(f"{Colors.BOLD}2. Missing Dependencies:{Colors.END}")
    print(f"   {Colors.CYAN}pip3 install -r requirements.txt{Colors.END}\n")
    
    print(f"{Colors.BOLD}3. Git LFS Not Installed:{Colors.END}")
    print("   - macOS: brew install git-lfs")
    print("   - Ubuntu: sudo apt-get install git-lfs")
    print("   - Windows: Download from https://git-lfs.github.com/\n")
    
    print("For more help, see README.md or HOW_TO_RUN.md")


def main():
    """Main setup routine."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup Multi-Agent Translation Project')
    parser.add_argument('--force', action='store_true', help='Force re-download even if model exists')
    parser.add_argument('--check-only', action='store_true', help='Only check status, do not install')
    parser.add_argument('--skip-validation', action='store_true', help='Skip model validation')
    args = parser.parse_args()
    
    print_header("🚀 MULTI-AGENT TRANSLATION PROJECT SETUP")
    
    # Step 1: Check Python version
    print_step(1, "Checking Python version...")
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Check/install dependencies
    print_step(2, "Checking Python packages...")
    packages_ok, missing = check_pip_packages()
    
    if not packages_ok:
        if args.check_only:
            print_error("Dependencies missing (use --no-check-only to install)")
            sys.exit(1)
        
        print_info("Installing missing packages...")
        if not install_requirements():
            print_error("Failed to install dependencies")
            print_troubleshooting()
            sys.exit(1)
    
    # Step 3: Check Git LFS
    print_step(3, "Checking Git LFS...")
    git_lfs_ok = check_git_lfs()
    
    if not git_lfs_ok:
        if not args.check_only:
            install_git_lfs()
        else:
            print_warning("Git LFS not available (may cause issues)")
    
    # Step 4: Check/download model
    print_step(4, "Checking embedding model...")
    model_path = get_model_path()
    print_info(f"Model path: {model_path}")
    
    model_exists = check_model_exists(model_path)
    
    if model_exists and not args.force:
        print_success("Model already installed!")
        
        if not args.skip_validation:
            print_step(5, "Validating model...")
            if not validate_model(model_path):
                print_error("Model validation failed")
                print_info("Try re-running with --force to re-download")
                sys.exit(1)
        
        create_env_file(model_path)
        print_next_steps()
        return
    
    if args.check_only:
        print_error("Model not found (use --no-check-only to download)")
        sys.exit(1)
    
    if args.force and model_exists:
        print_warning("Removing existing model (--force)")
        shutil.rmtree(model_path, ignore_errors=True)
    
    # Try Python API first (faster if works)
    print_step(5, "Downloading model...")
    success, ssl_error = download_model_via_python(model_path)
    
    # If SSL error, try Git clone
    if not success and ssl_error:
        print_info("Falling back to Git LFS clone (bypasses SSL API issues)...")
        success = download_model_via_git(model_path)
    
    if not success:
        print_error("Model download failed")
        print_troubleshooting()
        sys.exit(1)
    
    # Step 6: Validate
    if not args.skip_validation:
        print_step(6, "Validating model...")
        if not validate_model(model_path):
            print_error("Model validation failed")
            sys.exit(1)
    
    # Step 7: Create config
    print_step(7, "Creating configuration...")
    create_env_file(model_path)
    
    # Success!
    print_next_steps()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Setup interrupted by user{Colors.END}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

