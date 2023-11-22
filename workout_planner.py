import streamlit as st
import pandas as pd
from ortools.sat.python import cp_model


@st.cache_data(persist=True)
def read_and_filter(filename, muscle_group):
    df = pd.read_csv(filename)
    filtered = df[df['major_muscle'] == muscle_group]
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


def solve(model, exercise_vars, df):
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        selected_workouts = [exercise for exercise,
                             var in exercise_vars.items() if solver.Value(var) == 1]

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


st.title("Plan your next workout intelligently")
muscle_group = st.selectbox("What muscle group are you working out today?",
                            ("Chest", "Back", "Legs", "Shoulders", "Arms"),
                            index=None,
                            placeholder="Select a muscle group")

with st.spinner("Generating your workout..."):
    df = read_and_filter('exercises_cleaned.csv', muscle_group)
    model, exercise_vars = create_problem(df)
    selected_workouts = solve(model, exercise_vars, df)
if selected_workouts is None:
    st.write("No workout generated")
else:
    st.write(selected_workouts)
