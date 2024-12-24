#!/usr/bin/env python3
"""
setup.py - Automated setup script for MCP Manager development environment
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import shutil
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mcp-manager-setup')

class SetupError(Exception):
    """Custom exception for setup errors"""
    pass

class MCPManagerSetup:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.src_path = base_path / "src" / "mcp_manager"
        self.tests_path = base_path / "tests"

    def create_directory_structure(self) -> None:
        """Create the project directory structure"""
        logger.info("Creating directory structure...")
        
        directories = [
            self.src_path,
            self.src_path / "core",
            self.src_path / "models",
            self.src_path / "services",
            self.src_path / "utils",
            self.tests_path
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            init_file = directory / "__init__.py"
            if not init_file.exists():
                init_file.touch()

        logger.info("Directory structure created successfully")

    def create_git_ignore(self) -> None:
        """Create .gitignore file"""
        logger.info("Creating .gitignore...")
        
        gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
        
        with open(self.base_path / ".gitignore", "w") as f:
            f.write(gitignore_content.strip())
        
        logger.info(".gitignore created successfully")

    def create_python_version(self) -> None:
        """Create .python-version file"""
        logger.info("Creating .python-version...")
        
        with open(self.base_path / ".python-version", "w") as f:
            f.write("3.10")
        
        logger.info(".python-version created successfully")

    def create_pyproject_toml(self) -> None:
        """Create pyproject.toml"""
        logger.info("Creating pyproject.toml...")
        
        content = """
[project]
name = "mcp-manager"
version = "0.1.0"
description = "A Model Context Protocol (MCP) server for managing other MCP servers"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
    "pydantic>=2.0.0",
    "click>=8.1.7",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pyright>=1.1.389",
    "pytest>=8.3.3",
    "ruff>=0.8.0"
]

[project.scripts]
mcp-manager = "mcp_manager:main"
"""
        
        with open(self.base_path / "pyproject.toml", "w") as f:
            f.write(content.strip())
        
        logger.info("pyproject.toml created successfully")

    def create_readme(self) -> None:
        """Create README.md"""
        logger.info("Creating README.md...")
        
        content = """
# MCP Manager

## Overview
MCP Manager is a specialized Model Context Protocol (MCP) server designed to simplify the installation, configuration, and management of other MCP servers.

## Installation
```bash
# Using uv (recommended)
uv pip install mcp-manager

# Using pip
pip install mcp-manager
```

## Development Setup
```bash
# Clone the repository
git clone https://github.com/your-username/mcp-manager.git

# Run setup script
python setup.py

# Install dependencies
uv pip install -e ".[dev]"
```

## Features
- Simple installation of MCP servers
- Automated configuration management
- Server status monitoring
- Error recovery and diagnostics

## License
This project is licensed under the MIT License - see the LICENSE file for details.
"""
        
        with open(self.base_path / "README.md", "w") as f:
            f.write(content.strip())
        
        logger.info("README.md created successfully")

    def init_git(self) -> None:
        """Initialize git repository"""
        logger.info("Initializing git repository...")
        
        try:
            subprocess.run(["git", "init"], cwd=self.base_path, check=True)
            logger.info("Git repository initialized successfully")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to initialize git repository: {e}")
            logger.warning("Please initialize git repository manually")

    def setup_uv(self) -> None:
        """Setup uv package manager"""
        logger.info("Setting up uv...")
        
        try:
            # Check if uv is installed
            subprocess.run(["uv", "--version"], check=True, capture_output=True)
            logger.info("uv is already installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.info("Installing uv...")
            try:
                if platform.system() == "Windows":
                    # Add Windows uv installation
                    logger.warning("Windows uv installation not implemented")
                else:
                    subprocess.run(
                        ["curl", "-LsSf", "https://astral.sh/uv/install.sh"],
                        stdout=subprocess.PIPE,
                        check=True
                    )
                logger.info("uv installed successfully")
            except subprocess.CalledProcessError as e:
                raise SetupError(f"Failed to install uv: {e}")

    def install_dependencies(self) -> None:
        """Install project dependencies"""
        logger.info("Installing dependencies...")
        
        try:
            subprocess.run(
                ["uv", "pip", "install", "-e", ".[dev]"],
                cwd=self.base_path,
                check=True
            )
            logger.info("Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            raise SetupError(f"Failed to install dependencies: {e}")

    def run(self) -> None:
        """Run the complete setup process"""
        try:
            self.create_directory_structure()
            self.create_git_ignore()
            self.create_python_version()
            self.create_pyproject_toml()
            self.create_readme()
            self.init_git()
            self.setup_uv()
            self.install_dependencies()
            logger.info("Setup completed successfully!")
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            raise

def main():
    """Main entry point"""
    try:
        base_path = Path.cwd()
        setup = MCPManagerSetup(base_path)
        setup.run()
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
