import streamlit as st
import pandas as pd
from ortools.sat.python import cp_model
import re


@st.cache_data(persist=True)
def read_and_filter(filename, muscle_group):
    df = pd.read_csv(filename)
    filtered = df[df['major_muscle'] == muscle_group]
    if filtered.empty:
        filtered = df[df['minor_muscle'] == muscle_group]

    # Can be removed, just ensuring that there is no bias in the selection
    shuffled = filtered.sample(frac=1).reset_index(drop=True)
    return shuffled


def create_problem(df):
    model = cp_model.CpModel()

    exercise_vars = {}
    for index, row in df.iterrows():
        exercise_vars[row['exercise']] = model.NewBoolVar(row['exercise'])

    upper_bound, lower_bound = 7, 5
    model.Add(sum(exercise_vars.values()) >= lower_bound)
    model.Add(sum(exercise_vars.values()) <= upper_bound)

    return model, exercise_vars


def extract_and_add(**kwargs):
    all_muscles = []
    pattern = re.compile(r"'([^']+)'")

    for _, value in kwargs.items():
        matches = pattern.findall(value)
        for match in matches:
            all_muscles.append(match)
    return all_muscles


def get_all_muscles(exercise):
    # TODO: Remove this line, and have the cleaned csv contain these columns instead
    original = pd.read_csv('exrx.csv')

    row = original[original['exercise'] == exercise]
    target_muscles = row['target_muscles'].values[0]
    synergist_muscles = row['synergist_muscles'].values[0]
    stabilizer_muscles = row['stabilizer_muscles'].values[0]
    dynamic_stabilizer_muscles = row['dynamic_stabilizer_muscles'].values[0]
    antagonist_stabilizer_muscles = row['antagonist_stabilizer_muscles'].values[0]

    kwargs = {'target_muscles': target_muscles, 'synergist_muscles': synergist_muscles, 'stabilizer_muscles': stabilizer_muscles,
              'dynamic_stabilizer_muscles': dynamic_stabilizer_muscles, 'antagonist_stabilizer_muscles': antagonist_stabilizer_muscles}
    all_muscles = extract_and_add(**kwargs)
    return all_muscles


def find_lowest_contributing_exercise(selected_workouts):
    contribution_set = set()
    contribution_set_sizes = []
    for exercise in selected_workouts:
        all_muscles = get_all_muscles(exercise)
        for muscle in all_muscles:
            contribution_set.add(muscle)
        contribution_set_sizes.append(len(contribution_set))

    differences = [contribution_set_sizes[i] - contribution_set_sizes[i - 1]
                   for i in range(1, len(contribution_set_sizes))]

    # Move the index by 1 to account for the difference calculation
    min_index = differences.index(min(differences)) + 1
    lowest_contributor = selected_workouts[min_index]
    total_muscles = len(contribution_set)
    return lowest_contributor, total_muscles


def solve(model, exercise_vars, df):
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        selected_workouts = [exercise for exercise,
                             var in exercise_vars.items() if solver.Value(var) == 1]

        lowest_contributor, total_muscles = find_lowest_contributing_exercise(
            selected_workouts)

        if not 21 <= total_muscles <= 30:
            df = df[df['exercise'] != lowest_contributor]

            model, exercise_vars = create_problem(df)

            solve(model, exercise_vars, df)

        st.write(
            f"• Removing {lowest_contributor} from the workout")

        rows = []
        for workout in selected_workouts:
            row = df[df['exercise'] == workout].copy()
            row['target_muscles'] = row['target_muscles'].str.title()
            rows.append(row)

        output = pd.concat(rows)
        output.drop(columns=['utility', 'minor_muscle',
                    'major_muscle'], inplace=True)

        output.reset_index(inplace=True, drop=True)
        output.index += 1
        return output
    else:
        # No solution found
        return None


st.set_page_config(page_title="Workout Planner", page_icon="💪")

st.title("Plan your next workout intelligently")
muscle_group = st.selectbox("What muscle group are you working out today?",
                            ("Neck", "Shoulders", "Upper Arms", "Forearms",
                             "Back", "Chest", "Waist", "Hips", "Thighs", "Calves"),
                            index=None,
                            placeholder="Select a muscle group")

with st.spinner("Generating your workout..."):
    df = read_and_filter('exercises_cleaned.csv', muscle_group)
    model, exercise_vars = create_problem(df)
    selected_workouts = solve(model, exercise_vars, df)
if selected_workouts is None:
    st.write("No workout generated")
else:
    st.write("#")
    st.write("We found a workout for you! 🎉")
    st.write(selected_workouts)
