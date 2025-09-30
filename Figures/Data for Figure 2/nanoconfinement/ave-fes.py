import numpy as np

# Input file paths
files = ["../Configuration-1-fes.dat", "../Configuration-2-fes.dat", "../Configuration-3-fes.dat"]
output_file = "../Nanoconfinement-fes-avg.dat"

# Read file contents
lines_list = []
headers = []

for file in files:
    with open(file, "r") as f:
        lines = f.readlines()
    # Separate comment lines (starting with '#') from data lines
    header = [line for line in lines if line.startswith("#")]
    headers.append(header)
    lines_list.append(lines)

# Check if headers are consistent across all files
consistent_header = True
for i in range(1, len(headers)):
    if headers[i] != headers[0]:
        consistent_header = False
        break

if not consistent_header:
    print("⚠️ Warning: File headers are inconsistent, which may indicate different formats!")

# Write averaged data to output file
with open(output_file, "w") as fout:
    # Write unified header (use header from the first file)
    for line in headers[0]:
        fout.write(line)

    # Process each line of data
    num_files = len(files)
    for line_idx in range(len(lines_list[0])):
        data_values = []

        # Check if this line is a comment or invalid
        skip = False
        for i in range(num_files):
            line = lines_list[i][line_idx]
            if line.startswith("#"):  # Skip comment lines
                skip = True
                break
            parts = line.strip().split()
            if len(parts) < 5:  # Require at least 5 columns
                skip = True
                break
            try:
                free = float(parts[2])  # Extract free energy value (3rd column)
                data_values.append(free)
            except ValueError:  # Handle non-numeric values
                skip = True
                break

        if skip:
            continue  # Skip this line if marked

        # Extract collective variable coordinates and derivatives from the first file
        first_line_parts = lines_list[0][line_idx].strip().split()
        s_co = first_line_parts[0]      # CV1 value (e.g., distance)
        s_ch = first_line_parts[1]      # CV2 value
        der_s_co = first_line_parts[3]  # Derivative w.r.t. CV1
        der_s_ch = first_line_parts[4]  # Derivative w.r.t. CV2

        # Calculate average free energy across all configurations
        avg_free = sum(data_values) / num_files

        # Write averaged line: s_co s_ch avg_free der_s_co der_s_ch
        fout.write(f"{s_co} {s_ch} {avg_free:.9f} {der_s_co} {der_s_ch}\n")

print(f"✅ Averaged FES file has been generated: {output_file}")