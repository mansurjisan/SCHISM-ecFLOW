import datetime

def convert_to_seconds(time_str, start_time):
    time = datetime.datetime.strptime(time_str, "%m.%d.%Y %H:%M:%S")
    delta = time - start_time
    return int(delta.total_seconds())

input_file = 'tpxo9.out'
output_file = '../../workdir/elev.th'

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    # Skip header lines until find the first data line
    for line in infile:
        line = line.strip()
        if line and not line.startswith("Model:") and not line.startswith("Constituents") and not line.startswith("Lat") and not line.startswith("s1") and not line.startswith("-"):
            first_line = line
            print(f"First data line: {first_line}") 
            break

    # Process the first data line
    fields = first_line.split()
    print(f"Fields: {fields}")  

    if len(fields) >= 6:
        start_time_str = f"{fields[2]} {fields[3]}"
        start_time = datetime.datetime.strptime(start_time_str, "%m.%d.%Y %H:%M:%S")
        z_value = fields[4]
        
        # Write the first line
        outfile.write(f"0 {z_value}\n")
        
        # Process the rest of the lines
        for line in infile:
            fields = line.split()
            if len(fields) < 6:  
                continue
            time_str = f"{fields[2]} {fields[3]}"
            z_value = fields[4]
            seconds = convert_to_seconds(time_str, start_time)
            outfile.write(f"{seconds} {z_value}\n")

        print(f"Conversion complete. Output written to {output_file}")
    else:
        print("Error: First data line does not contain enough fields.")
        print("Please check the input file format.")
