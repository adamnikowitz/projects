#!/usr/bin/env python3
"""
LeetCode Tutor with CORRECT workflow:
1. Generate problem ONLY (no Docker, no execution) - appears immediately
2. User writes code
3. Submit code → THEN Docker execution + feedback
4. "Too Hard" button records difficulty and generates easier problem
"""

import gradio as gr
from crew import LeetCodeTutorCrew
import traceback

# Initialize the crew
print("Initializing crew at startup...")
crew = LeetCodeTutorCrew()
print("Crew initialized successfully")

def generate_problem_only():
    """Generate ONLY a coding problem - no execution, no Docker"""
    try:
        print("Generating problem only...")
        
        # Use OpenAI directly for problem generation
        from openai import OpenAI
        import random
        client = OpenAI()
        
        # Add variety by randomly selecting problem types and topics
        problem_types = [
            "array manipulation",
            "hash map operations", 
            "two-pointer technique",
            "string processing",
            "basic recursion",
            "tree traversal",
            "linked list operations",
            "stack/queue usage",
            "sliding window",
            "greedy algorithms",
            "basic sorting",
            "binary search"
        ]
        
        difficulty_levels = ["easy-medium", "medium", "medium-hard"]
        
        contexts = [
            "a real-world scenario like organizing data",
            "a game or puzzle context", 
            "a business problem scenario",
            "a mathematical sequence problem",
            "a data processing challenge",
            "an optimization problem"
        ]
        
        # Random selections for variety
        selected_type = random.choice(problem_types)
        selected_difficulty = random.choice(difficulty_levels)
        selected_context = random.choice(contexts)
        
        prompt = f"""You are a coding problem generator. Generate a {selected_difficulty} Python coding problem 
focused on {selected_type} that should take 10-15 minutes to solve.

Frame the problem in {selected_context} to make it more interesting and varied.

Requirements:
1. A clear problem statement with detailed description
2. Example input and output showing expected behavior
3. At least 2-3 test cases in the format: "function_name(arguments)" 
4. Expected time and space complexity analysis
5. Any constraints or edge cases to consider

The problem should be:
- Solvable in 10-15 minutes by an intermediate programmer
- Focus specifically on {selected_type} (avoid string/subarray if this wasn't selected)
- Have a clear, straightforward solution approach
- Be interesting and varied (not just another string/array manipulation)

IMPORTANT: Make this problem feel different from typical string/subarray questions. Be creative with the problem domain and context.

Format your response as a complete, self-contained problem description."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        result = response.choices[0].message.content
        print(f"Generated {selected_type} problem: {len(str(result))} chars")
        
        # Log the problem generation with type info
        crew.memory.log_problem(f"[{selected_type}] {str(result)}")
        
        return str(result)
        
    except Exception as e:
        print(f"Error generating problem: {e}")
        return "No problem generated yet. Click 'Generate New Problem' to create one."

def mark_problem_too_hard():
    """Mark current problem as too hard and generate a new one"""
    try:
        print("User marked problem as too hard...")
        
        # Record the difficulty feedback
        crew.memory.log_feedback("Problem marked as too hard - user requested easier problem")
        if "weaknesses" not in crew.memory.data:
            crew.memory.data["weaknesses"] = []
        crew.memory.data["weaknesses"].append("problem_difficulty")
        crew.memory._save()
        
        print("Logged 'too hard' feedback and generating new problem...")
        
        # Generate a new, potentially easier problem with variety
        from openai import OpenAI
        import random
        client = OpenAI()
        
        # Focus on easier topics when marked too hard
        easier_topics = [
            "basic array operations",
            "simple hash map usage",
            "basic string manipulation", 
            "two-pointer technique",
            "simple iteration patterns",
            "basic list operations",
            "counting and frequency problems",
            "simple mathematical calculations"
        ]
        
        contexts = [
            "a simple counting problem",
            "a basic data organization task",
            "a straightforward searching problem", 
            "a simple validation task",
            "a basic mathematical problem"
        ]
        
        selected_topic = random.choice(easier_topics)
        selected_context = random.choice(contexts)
        
        print(f"DEBUG: Selected easier topic: {selected_topic}")
        print(f"DEBUG: Selected context: {selected_context}")
        
        prompt = f"""You are a coding problem generator. The user just marked the previous problem as "too hard". 
Generate an EASIER Python coding problem focused on {selected_topic} that should take 10-15 minutes to solve.

Frame this as {selected_context} to make it interesting but accessible.

Focus on:
- {selected_topic}
- Very straightforward logic
- Minimal edge cases
- Clear, simple examples
- Avoid complex recursion, dynamic programming, or advanced algorithms

Create a problem that includes:
1. A clear, simple problem statement
2. Example input and output
3. 2-3 test cases in the format: "function_name(arguments)"
4. Should be solvable in 10-15 minutes for a beginner-intermediate programmer

IMPORTANT: Make this noticeably easier than typical interview questions. Focus on fundamentals.

Format your response as a complete problem description."""

        print("DEBUG: Making OpenAI API call...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        result = response.choices[0].message.content
        print(f"DEBUG: OpenAI response received: {len(str(result))} chars")
        
        # Log the new problem with easier marking
        crew.memory.log_problem(f"[EASIER - {selected_topic}] {str(result)}")
        
        print(f"Generated easier {selected_topic} problem: {len(str(result))} chars")
        return str(result)
        
    except Exception as e:
        error_msg = str(e)
        print(f"ERROR in mark_problem_too_hard: {error_msg}")
        import traceback
        traceback.print_exc()
        return f"Error generating easier problem: {error_msg}. Please try 'Generate New Problem'."

def execute_and_review_code(user_code: str):
    """Execute user code in Docker AND provide feedback - ONLY when user submits"""
    try:
        if not user_code or not user_code.strip():
            return "No code provided for execution.", "No code provided for review."
        
        print("NOW executing code in Docker and generating feedback...")
        
        # Use the full crew workflow for execution and feedback
        crew_instance = crew.crew()
        result = crew_instance.kickoff(inputs={"user_code": user_code})
        
        # Extract execution and feedback from tasks 2 and 3
        execution_result = ""
        feedback_result = ""
        
        if hasattr(result, 'tasks_output') and result.tasks_output:
            if len(result.tasks_output) > 1 and hasattr(result.tasks_output[1], 'raw'):
                execution_result = str(result.tasks_output[1].raw)
            if len(result.tasks_output) > 2 and hasattr(result.tasks_output[2], 'raw'):
                feedback_result = str(result.tasks_output[2].raw)
        
        if not execution_result:
            execution_result = "Code execution completed"
        if not feedback_result:
            feedback_result = "Code review completed"
            
        return execution_result, feedback_result
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error in execution/review: {error_msg}")
        return f"Execution error: {error_msg}", f"Review error: {error_msg}"

# Generate initial problem (ONLY problem, no execution)
print("Generating initial problem...")
initial_problem = generate_problem_only()

# Create the Gradio interface
with gr.Blocks(title="🚀 LeetCode Tutor AI", theme=gr.themes.Soft()) as demo:
    gr.HTML("<h1 style='text-align: center; margin-bottom: 1rem'>🚀 LeetCode Tutor AI</h1>")
    gr.Markdown("""
    **Correct Workflow:**
    1. 📋 **Read the problem** (generated below)
    2. ✍️ **Write your solution** in the code box  
    3. 🚀 **Submit** → ONLY THEN does Docker execution + feedback happen
    4. 😰 **Too Hard?** → Click button to get easier problem and record feedback
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            # Problem display (pre-populated, no execution)
            problem_display = gr.Textbox(
                label="📘 Coding Problem (10-15 min target)",
                lines=15,
                value=initial_problem,
                interactive=False,
                info="Your coding challenge - should take 10-15 minutes to solve!"
            )
            
            with gr.Row():
                new_problem_btn = gr.Button("🔄 Generate New Problem", variant="secondary")
                too_hard_btn = gr.Button("😰 Too Hard - Give Easier", variant="secondary")
            
        with gr.Column(scale=1):
            # Code input
            code_input = gr.Textbox(
                label="✍️ Your Solution",
                lines=15,
                placeholder="""def your_solution():
    # Write your code here
    pass
""",
                info="Write your solution - Docker runs ONLY when you submit"
            )
            
            with gr.Row():
                submit_btn = gr.Button("🚀 Submit & Execute", variant="primary", size="lg")
                clear_btn = gr.Button("🗑️ Clear", variant="secondary")
    
    with gr.Row():
        with gr.Column(scale=1):
            execution_output = gr.Textbox(
                label="⚙️ Execution Results",
                lines=8,
                interactive=False,
                info="Docker execution results (only after submit)"
            )
            
        with gr.Column(scale=1):
            feedback_output = gr.Textbox(
                label="🧠 Code Review",
                lines=8,
                interactive=False,
                info="AI feedback (only after submit)"
            )
    
    # Event handlers
    submit_btn.click(
        fn=execute_and_review_code,
        inputs=[code_input],
        outputs=[execution_output, feedback_output]
    )
    
    new_problem_btn.click(
        fn=generate_problem_only,  # ONLY generates problem
        outputs=[problem_display]
    )
    
    too_hard_btn.click(
        fn=mark_problem_too_hard,  # Records feedback and generates easier problem
        outputs=[problem_display]
    )
    
    clear_btn.click(
        lambda: "",
        outputs=[code_input]
    )

if __name__ == "__main__":
    print("🌐 Launching LeetCode Tutor with CORRECT workflow!")
    print("📋 Problem visible immediately, Docker ONLY runs on submit!")
    demo.launch(server_port=7860, share=False)