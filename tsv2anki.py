import genanki
import tkinter as tk
from tkinter import filedialog, messagebox
import logging

tsv_file_path = None  # Global variable to store the selected .tsv file path

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

# Function to select the TSV file
def select_tsv_file():
    global tsv_file_path
    tsv_file_path = filedialog.askopenfilename(filetypes=[("TSV Files", "*.tsv")])

    if tsv_file_path:
        tsv_file_label.config(text=f"Selected TSV File: {tsv_file_path}")
    else:
        tsv_file_label.config(text="No TSV file selected")

# Function to convert TSV to Anki flashcards
def convert_to_anki():
    if not tsv_file_path:
        messagebox.showerror("Error", "Please select a TSV file first.")
        return

    # Get the deck ID and deck name from the user
    try:
        deck_id = int(deck_id_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Deck ID must be an integer.")
        return

    deck_name = deck_name_entry.get()
    if not deck_name:
        messagebox.showerror("Error", "Please enter a Deck Name.")
        return

    # Automatically generate the output file name based on the deck name
    output_path = filedialog.asksaveasfilename(defaultextension=".apkg", filetypes=[("Anki Package Files", "*.apkg")], initialfile=f"{deck_name}.apkg")

    if not output_path:
        return  # User canceled output file selection

    # Define your Anki deck
    deck = genanki.Deck(deck_id, deck_name)

    # Read the selected .tsv file and convert it into flashcards
    with open(tsv_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            fields = line.strip().split('\t')
            if len(fields) == 2:
                front = fields[0]
                back = fields[1]

                # Create an Anki note
                note = genanki.Note(
                    model=genanki.Model(
                        deck_id + 1,  # Using deck_id + 1 as the model ID
                        'Simple Model',
                        fields=[
                            {'name': 'Front'},
                            {'name': 'Back'},
                        ],
                        templates=[
                            {
                                'name': 'Card 1',
                                'qfmt': '{{Front}}',
                                'afmt': '{{Front}}<br>{{Back}}',
                            },
                        ],
                    ),
                    fields=[front, back]
                )

                # Add the note to the deck
                deck.add_note(note)

    # Create an Anki package
    package = genanki.Package(deck)

    # Export the package to the specified output path
    try:
        package.write_to_file(output_path)
        messagebox.showinfo("Conversion Complete", "Anki deck has been created successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create a GUI window
root = tk.Tk()
root.title("TSV to Anki Converter")

# Deck ID label and entry
deck_id_label = tk.Label(root, text="Enter Deck ID:")
deck_id_label.pack()
deck_id_entry = tk.Entry(root)
deck_id_entry.pack()

# Deck name label and entry
deck_name_label = tk.Label(root, text="Enter Deck Name:")
deck_name_label.pack()
deck_name_entry = tk.Entry(root)
deck_name_entry.pack()

# Select TSV button
select_tsv_button = tk.Button(root, text="Select TSV", command=select_tsv_file)
select_tsv_button.pack()

# Convert button
convert_button = tk.Button(root, text="Convert to Anki", command=convert_to_anki)
convert_button.pack()

# Label to display the selected TSV file
tsv_file_label = tk.Label(root, text="")
tsv_file_label.pack()

# Run the GUI application
root.mainloop()
