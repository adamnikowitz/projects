#!/usr/bin/env python3
"""
Simple test script to verify the crew works
"""

from crew import LeetCodeTutorCrew
import traceback

def main():
    print("🧪 Testing Fixed CrewAI Implementation")
    print("=" * 50)
    
    try:
        # Create crew
        crew_instance = LeetCodeTutorCrew()
        assembled_crew = crew_instance.crew()
        
        print("✅ Crew assembled successfully")
        print(f"Agents: {len(assembled_crew.agents)}")
        print(f"Tasks: {len(assembled_crew.tasks)}")
        
        # Test with simple code
        test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
        
        print(f"\n🚀 Testing with Fibonacci function...")
        print("Starting execution...")
        
        result = assembled_crew.kickoff(inputs={"user_code": test_code})
        
        print("✅ Execution completed!")
        print(f"Result type: {type(result)}")
        
        # Print available attributes
        attrs = [attr for attr in dir(result) if not attr.startswith('_')]
        print(f"Available attributes: {attrs}")
        
        # Try to extract outputs
        if hasattr(result, 'tasks_output'):
            print(f"\n📋 Task Outputs ({len(result.tasks_output)} tasks):")
            for i, task_output in enumerate(result.tasks_output):
                print(f"\n--- Task {i+1} ---")
                content = ""
                if hasattr(task_output, 'raw'):
                    content = str(task_output.raw)
                elif hasattr(task_output, 'result'):
                    content = str(task_output.result)
                else:
                    content = str(task_output)
                
                print(content[:300] + "..." if len(content) > 300 else content)
        
        print("\n🎉 Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All tests passed! The crew should work in the Gradio app now.")
    else:
        print("\n❌ Tests failed. Check the errors above.")