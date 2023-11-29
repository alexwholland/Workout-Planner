import csv

muscles = {
    'Upper Arms': 3.5,
    'Shoulders': 3.0,
    'Hips': 2.5,
    'Calves': 2.8,
    'Back': 3.2,
    'Thighs': 3.0,
    'Waist': 2.0,
    'Chest': 3.8,
    'Forearms': 2.2,
    'Neck': 1.5
}

muscle_data = []

for muscle, size in muscles.items():
    lower_bound = round(max(1, size - 0.5), 1)
    upper_bound = round(min(4, size + 0.5), 1)
    muscle_data.append({'Muscle': muscle, 'Lower Bound': lower_bound, 'Upper Bound': upper_bound})

csv_file_path = 'muscle_bounds.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['Muscle', 'Lower Bound', 'Upper Bound']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(muscle_data)

print(f"CSV file '{csv_file_path}' has been created.")
