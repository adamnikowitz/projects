#!/usr/bin/env python3
"""
Test Gradio interface without any crew execution
This will help us identify if the issue is with Gradio setup or crew integration
"""

import gradio as gr

def mock_tutor_session(user_code: str):
    """Mock function that returns test data without calling crew"""
    print(f"Mock function called with: {user_code[:30]}...")
    
    # Return test data to verify Gradio is working
    problem = """
### Test Problem: Two Sum

Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

**Example:**
- Input: nums = [2,7,11,15], target = 9
- Output: [0,1]
- Explanation: nums[0] + nums[1] = 2 + 7 = 9

**Test Cases:**
- two_sum([2,7,11,15], 9) should return [0,1]
- two_sum([3,2,4], 6) should return [1,2]

**Time Complexity:** O(n)
**Space Complexity:** O(n)
"""
    
    execution_result = """
=== CODE EXECUTION RESULT ===
Test case: two_sum([2,7,11,15], 9)
Result: [0, 1] ✅

Test case: two_sum([3,2,4], 6)  
Result: [1, 2] ✅

All test cases passed!
=============================
"""
    
    feedback = """
### Code Review for Two Sum Implementation

**Correctness Analysis:**
✅ Your solution correctly implements the two sum algorithm
✅ All test cases pass successfully

**Code Quality Assessment:**
- Clean and readable code structure
- Good variable naming conventions
- Proper use of Python data structures

**Algorithm Efficiency:**
- Time Complexity: O(n) - excellent!
- Space Complexity: O(n) - optimal for this approach
- Uses hash map for efficient lookups

**Suggestions for Improvement:**
1. Consider adding input validation for edge cases
2. Add type hints for better code documentation
3. Consider handling duplicate values explicitly

**Next Steps for Learning:**
- Practice with Three Sum problem
- Explore sliding window technique
- Study hash table collision handling
"""
    
    return problem, execution_result, feedback

# Test using Blocks (same structure as main app)
with gr.Blocks(title="🧪 Test Gradio - No Crew", theme=gr.themes.Soft()) as demo:
    gr.HTML("<h1 style='text-align: center; margin-bottom: 1rem'>🧪 Test Gradio Interface</h1>")
    gr.Markdown("""
    **This is a test version that bypasses the crew entirely.**
    
    If this works, the issue is with crew integration.
    If this doesn't work, the issue is with Gradio setup.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            code_input = gr.Textbox(
                label="✍️ Test Input",
                lines=10,
                placeholder="Type anything here to test...",
                value="def test(): pass"  # Pre-filled for easy testing
            )
            submit_btn = gr.Button("Test Submit", variant="primary")
            clear_btn = gr.Button("Clear", variant="secondary")
            
        with gr.Column(scale=1):
            problem_output = gr.Textbox(
                label="📘 Test Problem Output",
                lines=10,
                interactive=False
            )
            execution_output = gr.Textbox(
                label="⚙️ Test Execution Output",
                lines=8,
                interactive=False
            )
            feedback_output = gr.Textbox(
                label="🧠 Test Feedback Output",
                lines=10,
                interactive=False
            )
    
    # Set up event handlers
    submit_btn.click(
        fn=mock_tutor_session,
        inputs=[code_input],
        outputs=[problem_output, execution_output, feedback_output]
    )
    
    clear_btn.click(
        lambda: ("", "", "", ""),
        outputs=[code_input, problem_output, execution_output, feedback_output]
    )

if __name__ == "__main__":
    print("🧪 Launching TEST Gradio interface (no crew execution)")
    print("This will test if Gradio display mechanism works...")
    demo.launch(server_port=7862, share=False)  # Different port