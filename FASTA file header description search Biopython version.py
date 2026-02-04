# FASTA file header search version with Biopython
from Bio import SeqIO
import sys

def get_user_descriptions():
    """Collect Multiple Descriptions from the User."""
    descriptions = set() # used to store multiple items in a single variable
    print("Enter descriptions to search for (type 'done' when finished entering descriptions; type 'next' for next file search; type 'exit' to quit the search):")
    while True:
        user_input = input("> ").strip().lower()
        if user_input.lower() == 'done': 
            break
        if user_input.lower() == 'next': 
            print("Go to next file search.\n")
            main()  
        if user_input.lower() == 'exit': 
            print("Exiting search. Goodbye!")
            quit()  
        if user_input: # When user has more than one search terms
            descriptions.add(user_input)
    return descriptions

def parse_fasta(filename):
    """Parse a FASTA file using Biopython's SeqIO."""
    try:
        sequences = SeqIO.to_dict(SeqIO.parse(filename, "fasta"))
        # Convert SeqRecord objects to a dictionary of header and sequence
        sequences = {record.description: str(record.seq) for record in sequences.values()}
        return sequences
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.\n")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def search_fasta(descriptions, sequences): # keys: header descriptions; values: DNA/protein sequences
    """Search and Display Results."""
    found_count = 0 # Initializes a counter to track how many matches are found
    # Iterates through each key (header) and value (sequence) pair in the sequences dictionary
    for header, sequence in sequences.items(): 
        # Checks if every string in the user's descriptions list exists within the current header string
        if all(desc in header.lower() for desc in descriptions):
            print(f"\n--- Match Found ---")
            print(f"Header: >{header}\n")
            print(f"Sequence: {sequence}\n")
            print(f"Length: {len(sequence)}")
            print(f"-------------------")
            found_count += 1
    if found_count == 0:
        print("No sequences found matching the descriptions.")

    print(f"{found_count} matches found\n")
    
def save_results_to_file(filename, descriptions, sequences):
    """Save search results to file."""
    try:
        with open(filename, 'w') as f: # Opens a file specified by filename in write mode ('w'). The file object is assigned to the variable f
            original_stdout = sys.stdout # Redirect the standard output (stdout) to the file f
            sys.stdout = f
            search_fasta(descriptions, sequences) # The output of this function will be written to the file f because sys.stdout has been redirected
            sys.stdout = original_stdout  # Reset stdout
        print(f"\nSuccessfully saved results to {filename}\n")
    except IOError as e:
        print(f"Error saving file: {e}\n")

def save_results_prompt(descriptions, sequences):
    """Asks the user if they want to save search results to a file."""
    user_choice = input("Do you want to save the search results to a file? (yes/no): ").strip().lower()
    if user_choice in ['yes', 'y']:
        filename = input("Enter a filename (e.g., results.fasta or faa): ").strip()
        if not filename.lower().endswith('.fasta'):
            filename += '.fasta'
        if not filename:
            filename = "search_results.fasta" # Default filename if none provided
        save_results_to_file(filename, descriptions, sequences)
    elif user_choice in ['no', 'n']:
        print("Results not saved.\n")
    else:
        print("Invalid input. Results not saved.")
    
def main():
    """Main function for the program's execution."""
    FASTA_FILE_NAME = input("Please enter the name of the FASTA file (e.g., sequences.fasta or faa): ")
    fasta_data = parse_fasta(FASTA_FILE_NAME)

    if fasta_data is None:
        main()
        return
    print(f"\nSuccessfully loaded {len(fasta_data)} sequences.\n")
    
    # creating a search loop
    while True:    
        user_descriptions = get_user_descriptions()
        if user_descriptions:
            search_fasta(user_descriptions, fasta_data)
            save_results_prompt(user_descriptions, fasta_data)
        else:
            print("No descriptions entered.\n")

# Checks if the script is being run directly by the user rather than being imported as a module into another script
if __name__ == "__main__": 
    main()
