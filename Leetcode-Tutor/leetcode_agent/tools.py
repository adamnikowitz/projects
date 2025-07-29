from crewai.tools import tool
from sandbox_runner import run_code_in_docker
import re

@tool("docker_code_executor")
def docker_code_executor(code: str, test_case: str = "") -> str:
    """
    Executes Python code in a secure Docker container and returns the output or error message.
    
    This tool runs Python code safely in an isolated Docker environment with resource limits.
    It can execute code with or without test cases and provides detailed output.
    
    Args:
        code (str): The Python code to execute. Should be valid Python syntax.
        test_case (str): Optional test case to run against the code. Can be a function call or expression.
    
    Returns:
        str: The output from the code execution, including results, errors, or execution details.
    
    Examples:
        - docker_code_executor("def add(a,b): return a+b", "add(2,3)")
        - docker_code_executor("print('Hello World')", "")
        - docker_code_executor("x = [1,2,3]; print(sum(x))", "")
    """
    print(f"DEBUG: docker_code_executor called with:")
    print(f"  Code (first 100 chars): {code[:100]}...")
    print(f"  Test case: {test_case}")
    
    try:
        # Validate inputs
        if not code or not code.strip():
            return "Error: No code provided for execution."
        
        # Clean up the code
        code = code.strip()
        
        # Validate Python syntax (basic check)
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            return f"Syntax Error: {str(e)}"
        
        # Execute the code
        result = run_code_in_docker(code, test_case)
        
        # Format the result nicely
        if result:
            formatted_result = f"""
=== CODE EXECUTION RESULT ===
{result}
=============================
"""
            return formatted_result.strip()
        else:
            return "Code executed successfully but produced no output."
            
    except Exception as e:
        error_msg = f"Tool execution error: {str(e)}"
        print(f"ERROR in docker_code_executor: {error_msg}")
        return error_msg

@tool("extract_test_cases")
def extract_test_cases(problem_description: str) -> str:
    """
    Extract test cases from a problem description.
    
    Args:
        problem_description (str): The problem description containing test cases
        
    Returns:
        str: Formatted list of extracted test cases
    """
    try:
        test_cases = []
        
        # Look for various test case patterns
        patterns = [
            r'test_case_\d+\s*[=:]\s*["\']([^"\']+)["\']',  # test_case_1 = "function(args)"
            r'Test case \d+:\s*([^\n]+)',  # Test case 1: function(args)
            r'Example \d+:\s*Input[:\s]+([^\n]+)',  # Example 1: Input: function(args)
            r'(\w+\([^)]+\))\s*(?:->|=>|=)\s*([^\n]+)',  # function(args) -> result
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, problem_description, re.IGNORECASE | re.MULTILINE)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        test_cases.append(match[0])
                    else:
                        test_cases.append(match)
                break
        
        if test_cases:
            return "Extracted test cases:\n" + "\n".join(f"- {tc}" for tc in test_cases[:5])  # Limit to 5 test cases
        else:
            return "No test cases found in the problem description."
            
    except Exception as e:
        return f"Error extracting test cases: {str(e)}"

# Test the tools if run directly
if __name__ == "__main__":
    # Test docker_code_executor
    test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    
    print("Testing docker_code_executor...")
    result = docker_code_executor(test_code, "fibonacci(5)")
    print("Result:", result)
    
    # Test extract_test_cases
    sample_problem = """
    Calculate the nth Fibonacci number.
    
    Test case 1: fibonacci(0) = 0
    Test case 2: fibonacci(1) = 1  
    Test case 3: fibonacci(5) = 5
    """
    
    print("\nTesting extract_test_cases...")
    test_cases = extract_test_cases(sample_problem)
    print("Test cases:", test_cases)