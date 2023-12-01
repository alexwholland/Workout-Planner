import csv

muscles = {
    'Upper Arms': 20,
    'Shoulders': 29,
    'Hips': 18,
    'Calves': 13,
    'Back': 28,
    'Thighs': 34,
    'Waist': 35,
    'Chest': 20,
    'Forearms': 10,
    'Neck': 19
}

muscle_data = []

for muscle, size in muscles.items():
    lower_bound = round( size -3, 1)
    upper_bound = round( size +3, 1)
    muscle_data.append({'Muscle': muscle, 'Lower Bound': lower_bound, 'Upper Bound': upper_bound})

csv_file_path = 'muscle_bounds.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['Muscle', 'Lower Bound', 'Upper Bound']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(muscle_data)

print(f"CSV file '{csv_file_path}' has been created.")
