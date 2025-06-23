import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SHIFTS = ["morning", "afternoon", "evening"]
MIN_PER_SHIFT = 2
MAX_PER_SHIFT = 3  # max employees per shift

class Employee:
    def __init__(self, name):
        self.name = name
        self.preferences = {}  # day -> list of priority shifts
        self.assignments = {}  # day -> assigned shift

    def can_work(self):
        return len(self.assignments) < 5

    def is_working_on(self, day):
        return day in self.assignments

    def assign_shift(self, day, shift):
        self.assignments[day] = shift

    def remove_shift(self, day):
        if day in self.assignments:
            del self.assignments[day]

    def __str__(self):
        return self.name

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Shift Scheduler")
        self.employees = []

        self.current_employee_index = 0
        self.employee_frames = []

        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_start_screen()

    def create_start_screen(self):
        # Ask number of employees
        self.clear_frame(self.main_frame)

        label = ttk.Label(self.main_frame, text="Enter number of employees:")
        label.pack(pady=5)

        self.num_employees_var = tk.IntVar()
        entry = ttk.Entry(self.main_frame, textvariable=self.num_employees_var)
        entry.pack(pady=5)

        btn = ttk.Button(self.main_frame, text="Submit", command=self.create_employee_forms)
        btn.pack(pady=10)

    def create_employee_forms(self):
        n = self.num_employees_var.get()
        if n <= 0:
            messagebox.showerror("Invalid Input", "Please enter a positive integer for number of employees.")
            return
        self.num_employees = n
        self.employees = []
        self.current_employee_index = 0

        self.clear_frame(self.main_frame)
        self.show_employee_form()

    def show_employee_form(self):
        self.clear_frame(self.main_frame)
        idx = self.current_employee_index

        label = ttk.Label(self.main_frame, text=f"Enter details for employee {idx + 1} of {self.num_employees}")
        label.pack(pady=5)

        name_label = ttk.Label(self.main_frame, text="Employee Name:")
        name_label.pack()
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(self.main_frame, textvariable=self.name_var)
        name_entry.pack(pady=5)

        self.pref_vars = {}
        ttk.Label(self.main_frame, text="Enter shift preferences (comma separated in priority order) for each day:").pack(pady=5)

        for day in DAYS:
            frame = ttk.Frame(self.main_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=day+":", width=10).pack(side=tk.LEFT)
            var = tk.StringVar()
            entry = ttk.Entry(frame, textvariable=var, width=30)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Set existing preferences if employee exists, else default
            if idx < len(self.employees):
                var.set(", ".join(self.employees[idx].preferences.get(day, SHIFTS)))
            else:
                var.set("morning, afternoon, evening")

            self.pref_vars[day] = var

        # Set existing employee name if exists
        if idx < len(self.employees):
            self.name_var.set(self.employees[idx].name)
        else:
            self.name_var.set("")

        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        if idx > 0:
            prev_btn = ttk.Button(btn_frame, text="Previous", command=self.prev_employee)
            prev_btn.pack(side=tk.LEFT, padx=5)
        next_btn = ttk.Button(btn_frame, text="Next", command=self.next_employee)
        next_btn.pack(side=tk.LEFT, padx=5)

    def clear_form_fields(self):
        self.name_var.set("")
        for day in DAYS:
            self.pref_vars[day].set("morning, afternoon, evening")

    def prev_employee(self):
        if self.current_employee_index > 0:
            if not self.save_current_employee():
                return
            self.current_employee_index -= 1
            self.load_employee()
            self.show_employee_form()

    def next_employee(self):
        if not self.save_current_employee():
            return
        if self.current_employee_index < self.num_employees - 1:
            self.current_employee_index += 1
            if self.current_employee_index < len(self.employees):
                self.load_employee()
            else:
                self.clear_form_fields()
            self.show_employee_form()
        else:
            # Last employee saved, run scheduling
            self.run_scheduler()

    def save_current_employee(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Invalid Input", "Employee name cannot be empty.")
            return False
        # Validate preferences
        preferences = {}
        for day, var in self.pref_vars.items():
            prefs_raw = var.get().strip().lower()
            prefs = [p.strip() for p in prefs_raw.split(",")]
            if not all(p in SHIFTS for p in prefs) or len(set(prefs)) != len(prefs):
                messagebox.showerror(
                    "Invalid Input",
                    f"Invalid preferences for {day}. Use shifts from {SHIFTS} separated by commas, no repeats."
                )
                return False
            preferences[day] = prefs
        # Save employee
        emp = Employee(name)
        emp.preferences = preferences

        if len(self.employees) <= self.current_employee_index:
            self.employees.append(emp)
        else:
            self.employees[self.current_employee_index] = emp
        return True

    def load_employee(self):
        emp = self.employees[self.current_employee_index]
        self.name_var.set(emp.name)
        for day in DAYS:
            self.pref_vars[day].set(", ".join(emp.preferences.get(day, SHIFTS)))

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    # Scheduling functions (same as before, but inside class, using self.employees)
    def assign_employee(self, schedule, emp, day, shift):
        if emp.can_work() and not emp.is_working_on(day) and len(schedule[day][shift]) < MAX_PER_SHIFT:
            schedule[day][shift].append(emp)
            emp.assign_shift(day, shift)
            return True
        return False

    def build_schedule(self):
        schedule = {day: {shift: [] for shift in SHIFTS} for day in DAYS}
        for emp in self.employees:
            for day in DAYS:
                for shift_pref in emp.preferences[day]:
                    if self.assign_employee(schedule, emp, day, shift_pref):
                        break
        return schedule

    def fill_minimum_staff(self, schedule):
        for day in DAYS:
            for shift in SHIFTS:
                assigned = schedule[day][shift]
                if len(assigned) < MIN_PER_SHIFT:
                    needed = MIN_PER_SHIFT - len(assigned)
                    candidates = [e for e in self.employees if e.can_work() and not e.is_working_on(day)]
                    random.shuffle(candidates)
                    added = 0
                    for c in candidates:
                        if len(schedule[day][shift]) >= MAX_PER_SHIFT:
                            break
                        if added >= needed:
                            break
                        schedule[day][shift].append(c)
                        c.assign_shift(day, shift)
                        added += 1
                    if len(schedule[day][shift]) < MIN_PER_SHIFT:
                        print(f"Warning: Could not assign minimum staff to {shift} on {day}.")
        return schedule

    def resolve_conflicts(self, schedule):
        for emp in self.employees:
            for day in list(emp.assignments.keys()):
                assigned_shift = emp.assignments[day]
                preferred_order = emp.preferences[day]

                if assigned_shift != preferred_order[0]:
                    for preferred_shift in preferred_order:
                        if preferred_shift == assigned_shift:
                            break
                        if len(schedule[day][preferred_shift]) < MAX_PER_SHIFT:
                            schedule[day][assigned_shift].remove(emp)
                            emp.remove_shift(day)
                            schedule[day][preferred_shift].append(emp)
                            emp.assign_shift(day, preferred_shift)
                            break
                    else:
                        day_index = DAYS.index(day)
                        if day_index + 1 < len(DAYS):
                            next_day = DAYS[day_index + 1]
                            if emp.can_work() and not emp.is_working_on(next_day):
                                if len(schedule[next_day][preferred_order[0]]) < MAX_PER_SHIFT:
                                    schedule[day][assigned_shift].remove(emp)
                                    emp.remove_shift(day)
                                    schedule[next_day][preferred_order[0]].append(emp)
                                    emp.assign_shift(next_day, preferred_order[0])
        return schedule

    def run_scheduler(self):
        # Clear previous assignments first
        for emp in self.employees:
            emp.assignments = {}

        schedule = self.build_schedule()
        schedule = self.fill_minimum_staff(schedule)
        schedule = self.resolve_conflicts(schedule)
        self.display_schedule(schedule)

    def display_schedule(self, schedule):
        self.clear_frame(self.main_frame)

        label = ttk.Label(self.main_frame, text="Final Weekly Schedule", font=("Arial", 14, "bold"))
        label.pack(pady=5)

        text_area = scrolledtext.ScrolledText(self.main_frame, width=60, height=25, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)

        output_lines = []
        for day in DAYS:
            output_lines.append(f"{day}:")
            for shift in SHIFTS:
                emps = schedule[day][shift]
                if emps:
                    names = ", ".join(e.name for e in emps)
                else:
                    names = "No employees assigned"
                output_lines.append(f"  {shift.capitalize()}: {names}")
            output_lines.append("")  # blank line

        text_area.insert(tk.END, "\n".join(output_lines))
        text_area.config(state=tk.DISABLED)

        # Add a restart button
        btn_restart = ttk.Button(self.main_frame, text="Restart", command=self.create_start_screen)
        btn_restart.pack(pady=10)

def main():
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()