import tkinter as tk
from tkinter import ttk


def get_window(table_rows):
    # Create a new Tkinter window
    window = tk.Tk()

    # Create a frame for the Treeview and scrollbars
    frame = ttk.Frame(window)
    frame.pack(fill='both', expand=True)

    # Create a treeview widget
    tree = ttk.Treeview(frame, columns=(
    'Poem Name', 'Type', 'Author', 'Year', 'Lime', 'Metaphor Available', 'Count', 'Source', 'Target', 'Meaning'),
                        show='headings')

    # Set column widths (modify these values as needed)
    for column in tree['columns']:
        tree.column(column, width=100)
        tree.heading(column, text=column)  # Set the headings

    # Create vertical and horizontal scrollbars
    v_scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
    h_scrollbar = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)

    # Configure the treeview to use the scrollbars
    tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Insert the data into the treeview
    for row in table_rows:
        tree.insert('', 'end', values=row)

    # Pack the treeview and scrollbars to the frame
    tree.grid(column=0, row=0, sticky='nsew')
    v_scrollbar.grid(column=1, row=0, sticky='ns')
    h_scrollbar.grid(column=0, row=1, sticky='ew')

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    return window
