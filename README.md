# Implementing-Control-Structures

Employee Shift Scheduler
This project demonstrates the implementation of control structures in both Python and Java to build a weekly employee shift scheduler. It combines GUI development, preference-based scheduling, and logic-driven assignments to generate optimal shift allocations.

💡 Objective
To showcase practical application of control structures such as conditionals, loops, and user input validation by implementing a fully functional employee shift scheduling tool. The GUI-based Python application and complementary Java component allow for employee preference management and constraint-based scheduling logic.

📁 Project Structure
bash

.
├── Main.py                  # Python GUI-based shift scheduler using Tkinter
├── Employeescheduler.java   # Java file for scheduling logic (if needed for comparison/demo)
├── README.md                # Project documentation
🛠 Features
Tkinter-based GUI for interactive employee input

Preference-based shift assignment logic

Control of minimum and maximum employees per shift

Conflict resolution and shift balancing

Weekly view of shift schedule

Restart capability to reconfigure employee preferences

🧩 Control Structures Implemented
Conditional Statements: To validate inputs, assign shifts based on constraints, and resolve conflicts.

Loops: To iterate over days, shifts, and employee lists for assigning and reassigning shifts.

Functions & Object-Oriented Structures: Encapsulate logic for better modularity and reuse.

GUI Controls: Button actions, entry validations, and step-by-step user flow.

🚀 How to Run
🐍 Python Application (Main.py)
Make sure Python 3 is installed.

Install Tkinter (usually pre-installed):

sudo apt-get install python3-tk
Run the Python file:


python3 Main.py
☕ Java File (Employeescheduler.java)
Compile and run using:


javac Employeescheduler.java
java Employeescheduler
Note: This Java file may serve as a console-based or logic-only module depending on your implementation.

📸 Sample GUI Flow (Python)
Input number of employees

For each employee:

Name input

Preferences for each day (shift priority)

Final schedule displayed in a scrollable window


🏁 Future Enhancements
Export schedule to CSV or PDF

Email notifications to employees

AI-based smart preference balancing

📜 License
This project is licensed for educational and demonstrative purposes only.

