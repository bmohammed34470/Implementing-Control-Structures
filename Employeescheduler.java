import java.util.*;

public class EmployeeScheduler {

    static final String[] DAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
    static final String[] SHIFTS = {"morning", "afternoon", "evening"};
    static final int MIN_PER_SHIFT = 2;
    static final int MAX_PER_SHIFT = 3;

    static class Employee {
        String name;
        Map<String, List<String>> preferences = new HashMap<>(); // day -> priority list of shifts
        Map<String, String> assignments = new HashMap<>();       // day -> assigned shift

        public Employee(String name) {
            this.name = name;
        }

        public boolean canWork() {
            return assignments.size() < 5;
        }

        public boolean isWorkingOn(String day) {
            return assignments.containsKey(day);
        }

        public void assignShift(String day, String shift) {
            assignments.put(day, shift);
        }

        public void removeShift(String day) {
            assignments.remove(day);
        }

        public String toString() {
            return name;
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        List<Employee> employees = new ArrayList<>();

        System.out.print("Enter number of employees: ");
        int n = Integer.parseInt(scanner.nextLine().trim());

        for (int i = 0; i < n; i++) {
            System.out.printf("Enter name for employee %d: ", i+1);
            String name = scanner.nextLine().trim();
            Employee emp = new Employee(name);

            System.out.println("Enter shift preferences for each day as comma separated list (e.g., morning,afternoon,evening):");
            for (String day : DAYS) {
                while (true) {
                    System.out.printf("  %s: ", day);
                    String line = scanner.nextLine().toLowerCase().trim();
                    String[] prefs = line.split("\\s*,\\s*");
                    if (validatePreferences(prefs)) {
                        emp.preferences.put(day, Arrays.asList(prefs));
                        break;
                    } else {
                        System.out.println("Invalid preferences. Must include shifts from [morning, afternoon, evening] with no duplicates.");
                    }
                }
            }
            employees.add(emp);
        }

        Map<String, Map<String, List<Employee>>> schedule = buildSchedule(employees);
        schedule = fillMinimumStaff(schedule, employees);
        schedule = resolveConflicts(schedule, employees);

        printSchedule(schedule);

        scanner.close();
    }

    // Validate preferences: only morning, afternoon, evening, no duplicates, length 3
    static boolean validatePreferences(String[] prefs) {
        if (prefs.length != SHIFTS.length) return false;
        Set<String> set = new HashSet<>();
        for (String p : prefs) {
            if (!Arrays.asList(SHIFTS).contains(p)) return false;
            if (set.contains(p)) return false;
            set.add(p);
        }
        return true;
    }

    static Map<String, Map<String, List<Employee>>> buildSchedule(List<Employee> employees) {
        Map<String, Map<String, List<Employee>>> schedule = new HashMap<>();
        for (String day : DAYS) {
            Map<String, List<Employee>> shiftsMap = new HashMap<>();
            for (String shift : SHIFTS) {
                shiftsMap.put(shift, new ArrayList<>());
            }
            schedule.put(day, shiftsMap);
        }

        for (Employee emp : employees) {
            for (String day : DAYS) {
                for (String prefShift : emp.preferences.get(day)) {
                    if (emp.canWork() && !emp.isWorkingOn(day)) {
                        List<Employee> assigned = schedule.get(day).get(prefShift);
                        if (assigned.size() < MAX_PER_SHIFT) {
                            assigned.add(emp);
                            emp.assignShift(day, prefShift);
                            break;
                        }
                    }
                }
            }
        }
        return schedule;
    }

    static Map<String, Map<String, List<Employee>>> fillMinimumStaff(Map<String, Map<String, List<Employee>>> schedule, List<Employee> employees) {
        Random rand = new Random();

        for (String day : DAYS) {
            for (String shift : SHIFTS) {
                List<Employee> assigned = schedule.get(day).get(shift);
                if (assigned.size() < MIN_PER_SHIFT) {
                    int needed = MIN_PER_SHIFT - assigned.size();
                    List<Employee> candidates = new ArrayList<>();
                    for (Employee e : employees) {
                        if (e.canWork() && !e.isWorkingOn(day)) {
                            candidates.add(e);
                        }
                    }
                    Collections.shuffle(candidates, rand);
                    int added = 0;
                    for (Employee c : candidates) {
                        if (assigned.size() >= MAX_PER_SHIFT) break;
                        if (added >= needed) break;
                        assigned.add(c);
                        c.assignShift(day, shift);
                        added++;
                    }
                    if (assigned.size() < MIN_PER_SHIFT) {
                        System.out.printf("Warning: Could not assign minimum staff to %s shift on %s.\n", shift, day);
                    }
                }
            }
        }
        return schedule;
    }

    static Map<String, Map<String, List<Employee>>> resolveConflicts(Map<String, Map<String, List<Employee>>> schedule, List<Employee> employees) {
        for (Employee emp : employees) {
            // Create a copy of days to avoid concurrent modification
            List<String> assignedDays = new ArrayList<>(emp.assignments.keySet());
            for (String day : assignedDays) {
                String assignedShift = emp.assignments.get(day);
                List<String> preferredOrder = emp.preferences.get(day);
                if (!assignedShift.equals(preferredOrder.get(0))) {
                    // Try better shifts same day
                    boolean moved = false;
                    for (String preferredShift : preferredOrder) {
                        if (preferredShift.equals(assignedShift)) break;
                        List<Employee> shiftList = schedule.get(day).get(preferredShift);
                        if (shiftList.size() < MAX_PER_SHIFT) {
                            schedule.get(day).get(assignedShift).remove(emp);
                            emp.removeShift(day);
                            shiftList.add(emp);
                            emp.assignShift(day, preferredShift);
                            moved = true;
                            break;
                        }
                    }
                    if (!moved) {
                        // Try next day, top preference shift
                        int dayIndex = Arrays.asList(DAYS).indexOf(day);
                        if (dayIndex + 1 < DAYS.length) {
                            String nextDay = DAYS[dayIndex + 1];
                            List<Employee> nextDayShiftList = schedule.get(nextDay).get(preferredOrder.get(0));
                            if (emp.canWork() && !emp.isWorkingOn(nextDay) && nextDayShiftList.size() < MAX_PER_SHIFT) {
                                schedule.get(day).get(assignedShift).remove(emp);
                                emp.removeShift(day);
                                nextDayShiftList.add(emp);
                                emp.assignShift(nextDay, preferredOrder.get(0));
                            }
                        }
                    }
                }
            }
        }
        return schedule;
    }

    static void printSchedule(Map<String, Map<String, List<Employee>>> schedule) {
        System.out.println("\nFinal Weekly Schedule:");
        for (String day : DAYS) {
            System.out.println(day + ":");
            for (String shift : SHIFTS) {
                List<Employee> emps = schedule.get(day).get(shift);
                if (emps.isEmpty()) {
                    System.out.println("  " + capitalize(shift) + ": No employees assigned");
                } else {
                    System.out.print("  " + capitalize(shift) + ": ");
                    System.out.println(String.join(", ", emps.stream().map(e -> e.name).toList()));
                }
            }
            System.out.println();
        }
    }

    static String capitalize(String s) {
        if (s == null || s.isEmpty()) return s;
        return s.substring(0, 1).toUpperCase() + s.substring(1);
    }
}