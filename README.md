# Workout Planner

## Overview

This Workout Planner is a Constraint Satisfaction Problem (CSP) that generates a personalized workout schedule based on the user's selected muscle groups. The application can be accessed through the following URL: [Workout Planner](https://get-jacked.streamlit.app/). Alternatively, you can run the code locally by installing the required dependencies listed in `requirements.txt` and executing the command:

```bash
streamlit run workout_planner.py
```

## Features

- **Muscle Group Selection:** Users can choose specific muscle groups for their workout from options such as Neck, Shoulders, Upper Arms, Forearms, Back, Chest, Waist, Hips, Thighs, and Calves.

- **Intelligent Workout Generation:** The code employs a CSP approach to intelligently generate a workout schedule based on the selected muscle groups.

- **Heuristic Function:** A heuristic function is incorporated to maximize the number of unique muscles being trained in the generated exercise set, ensuring a well-rounded workout.

- **Dynamic Exercise Filtering:** The system filters exercises from a pre-existing dataset ('exercises_cleaned.csv') based on the chosen muscle groups, ensuring a tailored workout plan.

- **Optimal Workout Selection:** The application aims to balance the workout routine by selecting exercises that collectively target a diverse range of muscles.

## How to Use

1. Visit [Workout Planner](https://get-jacked.streamlit.app/) to use the application directly.

2. Run the code locally:

   - Install dependencies: `pip install -r requirements.txt`
   - Execute the code: `streamlit run workout_planner.py`

3. On the web application or the locally-run instance, select the desired muscle groups and click the "Generate Workout" button.

4. The system will intelligently generate a workout plan, considering the heuristic function for maximizing unique muscle training. Results include exercise names, target muscles, and mechanics.

## Technical Details

### Code Structure

- **Data Loading:** The code reads exercise data from 'exercises_cleaned.csv' and muscle bounds from 'muscle_bounds.csv'.

- **Heuristic Function:** The heuristic function maximizes the number of unique muscles being trained, enhancing the overall effectiveness of the workout plan.

- **Constraint Satisfaction Problem (CSP):** The application formulates a CSP using the ortools library to generate a balanced workout plan.

- **Permutations and Selection:** The code explores permutations of selected exercises to find the most common lowest contributing exercise, considering the heuristic function.

- **Streamlit Integration:** The application is built using the Streamlit framework for a user-friendly interface.

## Troubleshooting

- If no workout is generated, it may be due to limitations in exercise availability for the selected muscle groups.

- The system may remove certain exercises to maintain balance. Removed exercises will be displayed in the output.

## Acknowledgments

This Workout Planner is designed to assist users in creating balanced and effective workout routines. Feel free to provide feedback or report issues for continuous improvement.

**Let's get jacked together! 💪**
