import csv
import os
from datetime import datetime
from pathlib import Path

import translate as trans

def save_csv(x, y, language):
    # Get the user's downloads folder
    downloads_folder = str(Path.home() / "Downloads")

    # Create the CSV file path with current date
    now = datetime.now().strftime("%d-%m-%Y_%H-%M")
    file_path = os.path.join(downloads_folder, f"rotato_data_{now}.csv")

    # Write the data to the CSV file
    with open(file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([str(trans.trans('time', language) + ' (' + trans.trans('seconds_short', language) + ')'), trans.trans('brightness', language) + '(%)'])
        
        for i in range(len(x)):
            writer.writerow([x[i], y[i]])
