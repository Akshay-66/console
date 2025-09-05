from flask import Flask, request, render_template, session
import os

app = Flask(__name__)
app.secret_key = "vecnas-logic-trap"

# --- Define your questions dynamically ---
questions = {
    "Q1": lambda x: x[::-1],                   # reverse string
    "Q2": lambda x: str(int(x) * 8),           # multiply number by 8
    "Q3": lambda x: f"Length: {len(x)} chars"  # length of input
    # ➕ Add more like "Q4": func
}


@app.route("/", methods=["GET", "POST"])
def home():
    # Initialize session storage
    if "histories" not in session:
        session["histories"] = {q: [] for q in questions}
    if "active_question" not in session:
        session["active_question"] = None

    histories = session["histories"]
    active_question = session["active_question"]

    if request.method == "POST":
        user_input = request.form["user_input"].strip()
        output = ""

        # Reset clears everything
        if user_input.lower() == "reset":
            session.clear()
            session["histories"] = {q: [] for q in questions}
            session["active_question"] = None
            histories = session["histories"]
            active_question = None
            output = "Terminal reset."

        # Switching active question
        elif user_input.startswith("switch "):
            qname = user_input.split(" ", 1)[1]
            if qname in questions:
                active_question = qname
                session["active_question"] = qname
                output = f"Switched to {qname}."
                histories[qname].append((user_input, output))
            else:
                output = f"Unknown question: {qname}"

        # Normal input → process only if active question set
        else:
            if active_question:
                try:
                    output = questions[active_question](user_input)
                except Exception as e:
                    output = f"Error: {str(e)}"
                histories[active_question].append((user_input, output))
            else:
                output = "Please choose a question first."
                # keep it in a temporary view but not stored in histories

        # Save back
        session["histories"] = histories

    # Choose which history to render
    display_history = []
    if active_question:
        display_history = histories[active_question]
    else:
        # Always show "Please choose a question first." when none active
        display_history = [("System", "Please choose a question first.")]

    return render_template(
        "index.html",
        history=display_history,
        active_question=active_question,
        questions=list(questions.keys())
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)