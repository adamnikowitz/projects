import docker
import tempfile
import os
import time
import re

def detect_required_packages(code: str) -> list:
    """Detect packages that need to be installed from import statements"""
    import_patterns = [
        r'from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import',
        r'import\s+([a-zA-Z_][a-zA-Z0-9_]*)'
    ]
    
    # Standard library modules that don't need installation
    stdlib_modules = {
        'typing', 'collections', 'itertools', 'functools', 'operator', 'sys', 'os', 
        'math', 'random', 'datetime', 'time', 'json', 'csv', 'sqlite3', 're', 
        'urllib', 'http', 'html', 'xml', 'email', 'base64', 'hashlib', 'hmac',
        'uuid', 'decimal', 'fractions', 'statistics', 'pathlib', 'glob', 'shutil',
        'subprocess', 'threading', 'multiprocessing', 'queue', 'socket', 'ssl',
        'heapq', 'bisect', 'array', 'struct', 'codecs', 'io', 'string', 'textwrap'
    }
    
    # Common packages and their pip names
    package_mappings = {
        'numpy': 'numpy',
        'pandas': 'pandas', 
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'requests': 'requests',
        'beautifulsoup4': 'beautifulsoup4',
        'bs4': 'beautifulsoup4',
        'scipy': 'scipy',
        'sklearn': 'scikit-learn',
        'cv2': 'opencv-python',
        'PIL': 'Pillow',
        'flask': 'flask',
        'django': 'django'
    }
    
    required_packages = set()
    
    for pattern in import_patterns:
        matches = re.findall(pattern, code)
        for match in matches:
            # Get the top-level module name
            module_name = match.split('.')[0]
            
            # Skip if it's a standard library module
            if module_name not in stdlib_modules:
                # Map to pip package name if needed
                pip_name = package_mappings.get(module_name, module_name)
                required_packages.add(pip_name)
    
    return list(required_packages)

def run_code_in_docker(code: str, test_case: str = None) -> str:
    """
    Execute Python code in a secure Docker container with automatic package installation
    
    Args:
        code (str): The Python code to execute
        test_case (str): Optional test case to run
    
    Returns:
        str: The output from code execution or error message
    """
    client = docker.from_env()
    
    try:
        # Detect required packages
        required_packages = detect_required_packages(code)
        
        # Prepare the code to execute
        if test_case and test_case.strip():
            # If test_case looks like a function call, execute it
            if '(' in test_case and ')' in test_case:
                full_code = f"{code}\nresult = {test_case}\nprint(f'Test case: {test_case}')\nprint(f'Result: {{result}}')"
            else:
                # Otherwise, just print the test case
                full_code = f"{code}\nprint('Test case:', {test_case})\nprint('Result:', {test_case})"
        else:
            # Just run the code as-is
            full_code = code
        
        print(f"DEBUG: Executing code in Docker: {full_code[:100]}...")
        if required_packages:
            print(f"DEBUG: Installing packages: {required_packages}")
        
        # Create installation command if packages are needed
        install_cmd = ""
        if required_packages:
            packages_str = " ".join(required_packages)
            install_cmd = f"pip install {packages_str} && "
        
        # Create the full command
        container_name = f"leetcode_executor_{int(time.time())}"
        
        # Run the container with package installation + code execution
        full_command = f'{install_cmd}python3 -c "{full_code.replace(chr(34), chr(92)+chr(34))}"'
        
        output = client.containers.run(
            "python:3.10-slim",
            f"sh -c '{full_command}'",
            name=container_name,
            remove=True,
            network_disabled=False,  # Enable network for pip install
            mem_limit="256m",  # Increased for package installation
            cpu_period=100000,
            cpu_quota=50000,  # Limit to 50% CPU
            timeout=30,  # Increased timeout for package installation
            stdout=True,
            stderr=True
        )
        
        result = output.decode('utf-8').strip()
        print(f"DEBUG: Docker execution result: {result}")
        return result
        
    except docker.errors.ContainerError as e:
        error_output = e.stderr.decode('utf-8') if e.stderr else str(e)
        print(f"DEBUG: Container error: {error_output}")
        return f"Runtime Error: {error_output}"
    
    except docker.errors.ImageNotFound:
        return "Error: Python Docker image not found. Please ensure Docker is running and python:3.10-slim is available."
    
    except Exception as e:
        print(f"DEBUG: Unexpected error in docker execution: {str(e)}")
        return f"Execution Error: {str(e)}"

def test_docker_setup():
    """Test if Docker is properly set up"""
    try:
        client = docker.from_env()
        # Try to run a simple command
        output = client.containers.run(
            "python:3.10-slim",
            "python3 -c 'print(\"Docker setup OK\")'",
            remove=True,
            timeout=5
        )
        return output.decode('utf-8').strip() == "Docker setup OK"
    except Exception as e:
        print(f"Docker setup test failed: {e}")
        return False

if __name__ == "__main__":
    # Test the docker setup
    if test_docker_setup():
        print("✅ Docker setup is working correctly")
        
        # Test code execution with imports
        test_code = """
from typing import List

def process_numbers(nums: List[int]) -> List[int]:
    return [x * 2 for x in nums]

print(process_numbers([1, 2, 3]))
"""
        result = run_code_in_docker(test_code, "")
        print(f"Test result: {result}")
    else:
        print("❌ Docker setup failed")