import os
from datetime import datetime
from pathlib import Path

def SavePlot(fig):
    """Saves a Matplotlib figure to the user's downloads directory, ignoring the displayed x and y limits."""
    # Set the x and y limits to None to include the entire plot in the saved file
    ax = fig.axes[0]
    ax.set_xlim(0, None)
    
    # Get the user's downloads folder
    downloads_folder = str(Path.home() / "Downloads")

    # Create the CSV file path with current date
    now = datetime.now().strftime("%d-%m-%Y_%H-%M")
    file_path = os.path.join(downloads_folder, f"rotato_graph_{now}.png")

    fig.savefig(file_path)
