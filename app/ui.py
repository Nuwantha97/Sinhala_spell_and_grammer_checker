import tkinter as tk
from tkinter import messagebox
from app.spell_checker import check_sentence
from app.utils import load_dictionary
from app.grammar_checker import SinhalaGrammarChecker
import pandas as pd

# Load the Sinhala dictionary CSV
sinhala_dictionary = load_dictionary("data/sinhala_dict_with_ipa.csv")

def launch_ui():
    def check_spelling():
        input_text = input_box.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("Input Error", "Please enter some text!")
            return

        try:
            # Perform spell checking
            original_sentence, corrected_sentence, suggestions = check_sentence(input_text, sinhala_dictionary)
            
            # Display spelling suggestions
            suggestion_box.delete("1.0", tk.END)
            for word, suggestion_list in suggestions.items():
                suggestion_box.insert(tk.END, f"Spell check for: {word}\n")
                for i, (suggestion, distance) in enumerate(suggestion_list, 1):
                    suggestion_box.insert(tk.END, f"  {i}. {suggestion}\n")
                suggestion_box.insert(tk.END, "\n")
            
            # Perform grammar check on corrected sentence
            check_grammar(corrected_sentence)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error during spell checking: {str(e)}")

    def check_grammar(sentence):
        try:
            # Initialize grammar checker
            grammar_checker = SinhalaGrammarChecker()
            grammar_checker.load_model("C:/Projects/AI/Sinhala_Spell_and_Grammer_Checker/models/model2")
            
            # Get DataFrame for corrections
            df = pd.read_csv("data/merged_sentences.csv")
            
            # Check grammar
            result = grammar_checker.check_grammar(sentence, df)
            
            # Display results
            result_box.delete("1.0", tk.END)
            
            if result['has_error']:
                result_box.insert(tk.END, result['correction'] if result['correction'] else sentence)
                
                suggestion_box.insert(tk.END, "\nGrammar Check Results:\n")
                suggestion_box.insert(tk.END, f"Status: Grammatical errors found\n")
                if result['problematic_words']:
                    suggestion_box.insert(tk.END, "Corrections needed:\n")
                    for error in result['problematic_words']:
                        suggestion_box.insert(tk.END, 
                            f"• '{error['word']}' → '{error['correction']}'\n")
            else:
                result_box.insert(tk.END, sentence)
                suggestion_box.insert(tk.END, "\n✓ No grammatical errors found\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error during grammar checking: {str(e)}")



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
    tk.Button(root, text="Check", command=check_spelling).pack()

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
