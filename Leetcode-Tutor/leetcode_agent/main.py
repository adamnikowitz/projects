import gradio as gr
from crew import LeetCodeTutorCrew

# Initialize the crew
crew = LeetCodeTutorCrew()

# Define the function that runs the crew using Gradio
def tutor_session(user_code: str):
    result = crew.crew().kickoff(inputs={"user_code": user_code})
    
    # DEBUG: Print result keys if needed
    print("Crew Output:", result)

    return result.get("generate_problem_task", "No problem generated."), \
           result.get("evaluate_code_task", "No execution result."), \
           result.get("give_feedback_task", "No feedback available.")

# Gradio interface setup
demo = gr.Interface(
    fn=tutor_session,
    inputs=gr.Textbox(
        label="✍️ Your Python Code",
        lines=20,
        placeholder="def fib(n): ..."
    ),
    outputs=[
        gr.Textbox(label="📘 Problem"),
        gr.Textbox(label="⚙️ Execution Result"),
        gr.Textbox(label="🧠 Feedback")
    ],
    title="LeetCode Tutor AI",
    description="An AI tutor that generates coding problems, runs your code, and adapts to your weaknesses.",
    allow_flagging="never"
)

# Run either CLI or GUI
if __name__ == "__main__":
    import sys

    if "--cli" in sys.argv:
        print("📘 Running in CLI mode...\n")
        user_code = input("Paste your Python code:\n")
        result = crew.crew().kickoff(inputs={"user_code": user_code})

        print("\n📘 Problem:\n", result.get("generate_problem_task"))
        print("\n⚙️ Execution Result:\n", result.get("evaluate_code_task"))
        print("\n🧠 Feedback:\n", result.get("give_feedback_task"))
    else:
        print("🌐 Launching Gradio UI at http://localhost:7860")
        demo.launch()
