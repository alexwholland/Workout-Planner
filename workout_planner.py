import streamlit as st
import pandas as pd
from constraint import Problem


@st.cache_data(persist=True)
def read_and_filter(filename, muscle_group):
    df = pd.read_csv(filename)
    filtered = df[df['major_muscle'] == muscle_group][:20]
    return filtered


def create_problem(df):
    problem = Problem()

    records = df.to_dict('records')

    for exercise in records:
        problem.addVariable(exercise['exercise'], [0, 1])

    problem.addConstraint(lambda *selected_workouts: 5 <= sum(selected_workouts)
                          <= 7, tuple(workout['exercise'] for workout in records))
    return problem


def solve(problem):
    solutions = problem.getSolutions()

    selected_workouts = []
    for solution in solutions:
        selected_workouts = [workout for workout,
                             selected in solution.items() if selected == 1]
        if len(selected_workouts) in [5, 6, 7]:
            break
    return selected_workouts


st.title("Plan your next workout intelligently")
muscle_group = st.selectbox("What muscle group are you working out today?",
                            ("Chest", "Back", "Legs", "Shoulders", "Arms"),
                            index=None,
                            placeholder="Select a muscle group")

with st.spinner("Generating your workout..."):
    df = read_and_filter('exercises_cleaned.csv', muscle_group)
    problem = create_problem(df)

    selected_workouts = solve(problem)
    workouts_df = pd.DataFrame(selected_workouts, columns=["Exercise"])
    workouts_df.index += 1

if workouts_df.empty:
    st.write("No workout generated")
else:
    st.write(workouts_df)
