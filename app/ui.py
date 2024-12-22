import tkinter as tk
from tkinter import messagebox
from app.spell_checker import check_sentence
from app.utils import load_dictionary

# Load the Sinhala dictionary CSV
sinhala_dictionary = load_dictionary("data/sinhala_dict_with_ipa.csv")

def launch_ui():
    def check_spelling():
        input_text = input_box.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("Input Error", "Please enter some text!")
            return

        # Perform spell checking
        original_sentence, corrected_sentence, suggestions = check_sentence(input_text, sinhala_dictionary)

        # Display the corrected sentence
        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, corrected_sentence)

        # Display suggestions
        suggestion_box.delete("1.0", tk.END)
        for word, suggestion_list in suggestions.items():
            suggestion_box.insert(tk.END, f"Word: {word}\n")
            for i, (suggestion, distance) in enumerate(suggestion_list, 1):
                suggestion_box.insert(tk.END, f"  {i}. {suggestion} (Distance: {distance})\n")
            suggestion_box.insert(tk.END, "\n")

    # Create the main window
    root = tk.Tk()
    root.title("Sinhala Spell and Grammar Checker")

    # Disable window resizing
    root.resizable(False, False)

    # Input Text Box
    tk.Label(root, text="Enter Text:").pack()
    input_box = tk.Text(root, height=10, width=50)
    input_box.pack()

    # Check Button
    tk.Button(root, text="Check Spelling", command=check_spelling).pack()

    # Corrected Text Box
    tk.Label(root, text="Corrected Sentence:").pack()
    result_box = tk.Text(root, height=5, width=50)
    result_box.pack()

    # Suggestions Text Box
    tk.Label(root, text="Suggestions:").pack()
    suggestion_box = tk.Text(root, height=10, width=50)
    suggestion_box.pack()

    # Run the application
    root.mainloop()
