import os
import re
import csv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import subprocess

parent_dir = '~/parent_dir'

    # Traverse immediate subdirectories

start_date = datetime(2024, 1, 1)
curr_date = start_date
date_string_format = "%b %-d %Y"
for i in range(12):
    year_month = curr_date.strftime("%Y%m")
    print(f"Running for {year_month}")
    end_date = curr_date + relativedelta(months=1)
    command = [
        'git', 
        "shortlog", 
        f"--since='{curr_date.strftime(date_string_format)}'", 
        f"--until='{end_date.strftime(date_string_format)}'", 
        "--summary", 
        "--numbered", 
        "--email", 
        "--all"
    ]
    dir_counter = 0
    for entry in os.scandir(parent_dir):
        if entry.is_dir():
            subdir_path = entry.path
            print(f'Processing {subdir_path}...')

            # Example: run a command inside each subdirectory
            # Let's say the command is: `cat data.txt`
           
            try:
                result = subprocess.run(
                    command,
                    cwd=subdir_path,
                    capture_output=True,
                    text=True,
                    check=True
                )
                output_csv = f'{year_month}-output.csv'
                with open(output_csv, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    if dir_counter == 0:
                        writer.writerow(['directory', 'count', 'name', 'email'])  # header
                    for line in result.stdout.strip().splitlines():
                        line = line.strip()
                        match = re.match(r'(\d+)\s+(.*)\s+<([^>]+)>', line)
                        if match:
                            id_part = match.group(1)
                            name_part = match.group(2)
                            email_part = match.group(3)
                            writer.writerow([entry.name, id_part, name_part, email_part])
                        else:
                            print(f'No match found for line: {line}')
                dir_counter += 1
            except subprocess.CalledProcessError as e:
                print(f'Command failed in {subdir_path}: {e}')
                raise e
                    
    curr_date = end_date