{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "minicoin-dev-environment";
  
  buildInputs = with pkgs; [
    # Python 3.11 with full development support
    python311Full
    python311Packages.pip
    python311Packages.setuptools
    python311Packages.wheel
    
    # Python packages for the project
    python311Packages.pydantic
    python311Packages.pytest
    python311Packages.rich
    
    # Development tools
    python311Packages.black
    python311Packages.flake8
    python311Packages.mypy
    
    # Utilities
    git
    curl
    which
  ];

  shellHook = ''
    echo "=================================================="
    echo "  MiniCoin Development Environment"
    echo "=================================================="
    echo "Python version: $(python --version)"
    echo "Pip version: $(pip --version)"
    echo ""
    echo "Available commands:"
    echo "  - Run server:     python -m minicoin.server"
    echo "  - Run client:     python -m clients.simulator"
    echo "  - Run tests:      pytest tests/ -v"
    echo "  - Install deps:   pip install -r requirements.txt"
    echo "=================================================="
    echo ""
    
    # Set up Python path
    export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$PWD"
    
    # Create logs directory if it doesn't exist
    mkdir -p logs
    mkdir -p deliverables/code
    mkdir -p deliverables/logs
    
    # Optional: Create virtual environment if needed
    # python -m venv .venv
    # source .venv/bin/activate
  '';

  # Environment variables
  PYTHONPATH = ".";
  PYTHONUNBUFFERED = "1";
}
