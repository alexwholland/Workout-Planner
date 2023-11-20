from constraint import Problem, AllDifferentConstraint

# Sample data representing workouts with their major and target muscle groups
workouts_data = [
    {'name': 'Workout1', 'major_muscle': 'Chest', 'target_muscle': 'Triceps'},
    {'name': 'Workout2', 'major_muscle': 'Back', 'target_muscle': 'Biceps'},
    {'name': 'Workout3', 'major_muscle': 'Legs', 'target_muscle': 'Quads'},
    # Add more workout data as needed
]

# Create a problem instance
problem = Problem()

# Add variables for each workout
for workout in workouts_data:
    problem.addVariable(workout['name'], [0, 1])  # 0 for not selected, 1 for selected

# Specify workouts that should not be selected
for workout in workouts_data:
    if workout['name'] == 'Workout1':  # Adjust this condition as needed
        problem.addConstraint(lambda var: var != 1, (workout['name'],))

# Add a constraint to ensure at least one workout is selected
problem.addConstraint(lambda *selected_workouts: 2 <= sum(selected_workouts) <= 3, tuple(workout['name'] for workout in workouts_data))

# Find solutions
solutions = problem.getSolutions()

# Print selected workouts from a solution
for solution in solutions:
    selected_workouts = [workout for workout, selected in solution.items() if selected == 1]
    print("Selected Workouts:", selected_workouts)
