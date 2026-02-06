import tkinter as tk
from tkinter import messagebox, ttk
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
            original_sentence, corrected_sentence = check_sentence(input_text, sinhala_dictionary)
    
            # Perform grammar check on corrected sentence
            check_grammar(corrected_sentence)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error during spell checking: {str(e)}")

    def check_grammar(sentence):
        try:
            # Initialize grammar checker
            grammar_checker = SinhalaGrammarChecker()
            grammar_checker.load_model("models/model2")
            
            # Get DataFrame for corrections
            df = pd.read_csv("data/merged_sentences.csv")
            
            # Check grammar
            result = grammar_checker.check_grammar(sentence, df)
            
            # Display results
            result_box.delete("1.0", tk.END)
            
            if result['has_error']:
                result_box.insert(tk.END, result['correction'] if result['correction'] else sentence)
                
                result_box.insert(tk.END, "\n\nGrammar Check Results:\n")
                result_box.insert(tk.END, f"\nStatus: Grammatical errors found\n")
                if result['problematic_words']:
                    result_box.insert(tk.END, "Corrections needed:\n")
                    for error in result['problematic_words']:
                        result_box.insert(tk.END, 
                            f"• '{error['word']}' → '{error['correction']}'\n")
            else:
                result_box.insert(tk.END, sentence)
                result_box.insert(tk.END, "\n\nGrammar Check Results:\n")
                result_box.insert(tk.END, "\nStatus: ✓ No grammatical errors found\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error during grammar checking: {str(e)}")

    def clear_all():
        input_box.delete("1.0", tk.END)
        result_box.delete("1.0", tk.END)

    # Create the main window
    root = tk.Tk()
    root.title("Sinhala Spell and Grammar Checker")
    root.configure(bg='#f0f0f0')
    
    # Add padding around the main window
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Title section
    title_frame = ttk.Frame(main_frame)
    title_frame.pack(fill=tk.X, pady=(0, 15))
    
    title_label = ttk.Label(
        title_frame,
        text="Sinhala Spell and Grammar Checker",
        font=('Helvetica', 16, 'bold')
    )
    title_label.pack()

    # Input section
    input_frame = ttk.LabelFrame(main_frame, text="Enter Text", padding="5")
    input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    
    input_box = tk.Text(
        input_frame,
        height=15,
        width=100,
        font=('TkDefaultFont', 11),
        wrap=tk.WORD,
        relief="solid",
        borderwidth=1
    )
    input_box.pack(padx=5, pady=5)

    # Button styling
    style = ttk.Style()
    style.configure(
        'Check.TButton',
        font=('Helvetica', 11),
        padding=10
    )
    
    # Button section
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=(0, 10))
    
    check_button = ttk.Button(
        button_frame,
        text="Check Spelling and Grammar",
        command=check_spelling,
        style='Check.TButton'
    )
    check_button.pack(side=tk.LEFT, padx=5)

    clear_button = ttk.Button(
        button_frame,
        text="Clear All",
        command=clear_all,
        style='Check.TButton'
    )
    clear_button.pack(side=tk.LEFT, padx=5)

    # Result section
    result_frame = ttk.LabelFrame(main_frame, text="Corrected Sentence", padding="5")
    result_frame.pack(fill=tk.BOTH, expand=True)
    
    result_box = tk.Text(
        result_frame,
        height=15,
        width=100,
        font=('TkDefaultFont', 11),
        wrap=tk.WORD,
        relief="solid",
        borderwidth=1
    )
    result_box.pack(padx=5, pady=5)

    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')

    # Run the application
    root.mainloop()
