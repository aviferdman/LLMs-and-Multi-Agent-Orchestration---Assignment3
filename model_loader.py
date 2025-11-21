"""
Fault-tolerant model loader with SSL error handling.

This module provides robust model loading that:
1. Tries to load from local path first
2. Falls back to HuggingFace download if needed
3. Detects SSL errors specifically
4. Provides clear error messages and recovery instructions
5. Respects offline mode and environment variables

Environment Variables:
    HF_HUB_OFFLINE: Set to "1" to force offline mode
    MODEL_LOCAL_PATH: Override default local model path
"""

import os
import sys
from pathlib import Path
from typing import Optional

# Import will be attempted, but we handle failures gracefully
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None


class ModelLoadError(Exception):
    """Custom exception for model loading failures."""
    pass


class SSLCertificateError(ModelLoadError):
    """Raised when SSL certificate verification fails."""
    pass


def get_default_model_path() -> Path:
    """Get the default local model path."""
    # Try environment variable first
    env_path = os.environ.get('MODEL_LOCAL_PATH')
    if env_path:
        return Path(env_path).expanduser()
    
    # Try multiple possible locations
    possible_paths = [
        Path.home() / 'models' / 'all-MiniLM-L6-v2',  # ~/models/
        Path(__file__).parent / 'models' / 'all-MiniLM-L6-v2',  # ./models/
        Path('/tmp/models/all-MiniLM-L6-v2'),  # Temporary location
    ]
    
    # Return first existing path, or default to ~/models/
    for path in possible_paths:
        if path.exists():
            return path
    
    return Path.home() / 'models' / 'all-MiniLM-L6-v2'


def is_offline_mode() -> bool:
    """Check if offline mode is enabled."""
    return os.environ.get('HF_HUB_OFFLINE', '0') == '1'


def is_ssl_error(exception: Exception) -> bool:
    """
    Detect if an exception is SSL-related.
    
    Args:
        exception: The exception to check
        
    Returns:
        True if the exception is SSL-related
    """
    error_str = str(exception).lower()
    ssl_indicators = [
        'ssl',
        'certificate',
        'cert',
        'self-signed',
        'ssl_certificate_verify_failed',
        'sslcertverificationerror',
        'certificate verify failed',
    ]
    return any(indicator in error_str for indicator in ssl_indicators)


def print_ssl_error_help():
    """Print helpful message about SSL errors."""
    print("\n" + "="*80)
    print("⚠️  SSL CERTIFICATE ERROR DETECTED")
    print("="*80)
    print("\nYour network (corporate/school) is intercepting HTTPS connections,")
    print("which prevents downloading the embedding model from HuggingFace.")
    print("\n" + "-"*80)
    print("SOLUTIONS:")
    print("-"*80)
    print("\n1. Run the setup script to download the model:")
    print("   python3 setup.py")
    print("\n2. Or manually download with Git LFS:")
    print("   git lfs install")
    print("   mkdir -p ~/models")
    print("   cd ~/models")
    print("   git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2")
    print("\n3. Or switch to a home network (not corporate/school)")
    print("\n4. Or set offline mode:")
    print("   export HF_HUB_OFFLINE=1")
    print("\n" + "-"*80)
    print("After downloading, the project will work offline automatically.")
    print("="*80 + "\n")


def print_model_not_found_help(local_path: Path):
    """Print helpful message when model is not found."""
    print("\n" + "="*80)
    print("❌ MODEL NOT FOUND")
    print("="*80)
    print(f"\nLooked for model at: {local_path}")
    print("\nThe embedding model is required but not available.")
    print("\n" + "-"*80)
    print("TO FIX:")
    print("-"*80)
    print("\nRun the automated setup script:")
    print("   python3 setup.py")
    print("\nThis will:")
    print("   ✓ Check your network connectivity")
    print("   ✓ Download the model (930MB)")
    print("   ✓ Handle SSL issues automatically")
    print("   ✓ Set up offline mode")
    print("\n" + "-"*80)
    print("Alternatively, see README.md for manual installation.")
    print("="*80 + "\n")


def load_model_from_local(model_path: Path, verbose: bool = True) -> Optional[SentenceTransformer]:
    """
    Load model from local path.
    
    Args:
        model_path: Path to the local model directory
        verbose: Whether to print status messages
        
    Returns:
        Loaded model or None if failed
    """
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        raise ModelLoadError(
            "sentence-transformers package not installed. "
            "Run: pip install -r requirements.txt"
        )
    
    if not model_path.exists():
        if verbose:
            print(f"ℹ️  Local model not found at: {model_path}")
        return None
    
    try:
        if verbose:
            print(f"📦 Loading model from local path: {model_path}")
        model = SentenceTransformer(str(model_path))
        if verbose:
            print("✅ Model loaded successfully from local directory!")
        return model
    except Exception as e:
        if verbose:
            print(f"⚠️  Failed to load from local path: {e}")
        return None


def load_model_from_hub(model_name: str = 'all-MiniLM-L6-v2', verbose: bool = True) -> Optional[SentenceTransformer]:
    """
    Load model from HuggingFace Hub.
    
    Args:
        model_name: Name of the model on HuggingFace Hub
        verbose: Whether to print status messages
        
    Returns:
        Loaded model or None if failed
        
    Raises:
        SSLCertificateError: If SSL certificate verification fails
        ModelLoadError: For other loading errors
    """
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        raise ModelLoadError(
            "sentence-transformers package not installed. "
            "Run: pip install -r requirements.txt"
        )
    
    if is_offline_mode():
        if verbose:
            print("ℹ️  Offline mode enabled (HF_HUB_OFFLINE=1), skipping download")
        return None
    
    try:
        if verbose:
            print(f"🌐 Attempting to download model '{model_name}' from HuggingFace...")
            print("   (This may take a few minutes on first run)")
        model = SentenceTransformer(model_name)
        if verbose:
            print("✅ Model downloaded and loaded successfully!")
        return model
    except Exception as e:
        if is_ssl_error(e):
            if verbose:
                print("❌ SSL certificate error detected")
            raise SSLCertificateError(
                "Failed to download model due to SSL certificate verification error"
            ) from e
        else:
            if verbose:
                print(f"❌ Failed to download model: {e}")
            raise ModelLoadError(f"Failed to download model: {e}") from e


def load_model(
    model_name: str = 'all-MiniLM-L6-v2',
    local_path: Optional[Path] = None,
    verbose: bool = True,
    fail_on_error: bool = True
) -> Optional[SentenceTransformer]:
    """
    Load embedding model with fault-tolerant handling.
    
    This function implements a robust model loading strategy:
    1. Try local path first (if provided or auto-detected)
    2. Fall back to HuggingFace download if needed
    3. Handle SSL errors gracefully with helpful messages
    4. Respect offline mode and environment variables
    
    Args:
        model_name: Name of the model on HuggingFace Hub
        local_path: Optional local path to model (auto-detected if None)
        verbose: Whether to print status messages
        fail_on_error: Whether to exit on failure (vs returning None)
        
    Returns:
        Loaded SentenceTransformer model, or None if failed and fail_on_error=False
        
    Raises:
        SystemExit: If model loading fails and fail_on_error=True
        
    Example:
        >>> model = load_model()  # Auto-detect path, download if needed
        >>> model = load_model(local_path=Path('./my_model'))  # Use specific path
        >>> model = load_model(verbose=False)  # Silent mode
    """
    if verbose:
        print("\n" + "="*80)
        print("🤖 LOADING EMBEDDING MODEL")
        print("="*80 + "\n")
    
    # Determine local path
    if local_path is None:
        local_path = get_default_model_path()
    
    model = None
    ssl_error_occurred = False
    
    # Strategy 1: Try local path first
    if verbose:
        print("📍 Step 1: Checking for local model...")
    model = load_model_from_local(local_path, verbose=verbose)
    
    # Strategy 2: Try HuggingFace download if local failed
    if model is None and not is_offline_mode():
        if verbose:
            print("\n📍 Step 2: Local model not found, attempting download...")
        try:
            model = load_model_from_hub(model_name, verbose=verbose)
        except SSLCertificateError:
            ssl_error_occurred = True
            if verbose:
                print_ssl_error_help()
        except ModelLoadError as e:
            if verbose:
                print(f"\n❌ Failed to download model: {e}")
    
    # If both strategies failed, provide guidance
    if model is None:
        if ssl_error_occurred:
            if verbose:
                print("\n💡 The model download failed due to SSL errors.")
                print("   Please run: python3 setup.py")
        else:
            if verbose:
                print_model_not_found_help(local_path)
        
        if fail_on_error:
            if verbose:
                print("\n❌ Cannot proceed without model. Exiting...")
            sys.exit(1)
        else:
            return None
    
    if verbose:
        print("\n" + "="*80)
        print("✅ MODEL READY")
        print("="*80 + "\n")
    
    return model


# Global model instance (cached after first load)
_global_model = None


def get_model(
    model_name: str = 'all-MiniLM-L6-v2',
    local_path: Optional[Path] = None,
    verbose: bool = False,
    force_reload: bool = False
) -> SentenceTransformer:
    """
    Get model instance with caching.
    
    This function maintains a global model instance to avoid reloading
    on every call. Use force_reload=True to refresh the model.
    
    Args:
        model_name: Name of the model
        local_path: Optional local path
        verbose: Print status messages
        force_reload: Force reload even if cached
        
    Returns:
        Loaded model instance
    """
    global _global_model
    
    if _global_model is None or force_reload:
        _global_model = load_model(
            model_name=model_name,
            local_path=local_path,
            verbose=verbose,
            fail_on_error=True
        )
    
    return _global_model


def check_model_available() -> bool:
    """
    Check if model is available without loading it.
    
    Returns:
        True if model can be loaded, False otherwise
    """
    local_path = get_default_model_path()
    
    # Check local path
    if local_path.exists():
        required_files = ['config.json', 'pytorch_model.bin', 'tokenizer.json']
        has_all_files = all((local_path / f).exists() for f in required_files)
        if has_all_files:
            return True
    
    # Check if offline mode
    if is_offline_mode():
        return False
    
    # Could potentially download (but we don't actually try here)
    return False


if __name__ == "__main__":
    """Test the model loader."""
    print("Testing model loader...\n")
    
    # Test 1: Check if model is available
    print("Test 1: Checking model availability...")
    available = check_model_available()
    print(f"   Model available: {available}\n")
    
    # Test 2: Try to load model
    print("Test 2: Attempting to load model...")
    try:
        model = load_model(verbose=True, fail_on_error=False)
        if model:
            print("\n✅ Model loaded successfully!")
            print(f"   Model type: {type(model)}")
            
            # Test encoding
            test_text = "Hello world"
            embedding = model.encode(test_text)
            print(f"   Test encoding shape: {embedding.shape}")
        else:
            print("\n⚠️  Model could not be loaded")
    except Exception as e:
        print(f"\n❌ Error: {e}")

