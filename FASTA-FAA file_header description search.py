# A program for user to input multiple descriptions to search a fasta file, and with an option to save the search result as fasta files without using Biopython
import sys

# Collect Multiple Descriptions from the User
def get_user_descriptions():
    descriptions = set() # used to store multiple items in a single variable
    print("Enter descriptions to search for (type 'done' when finished entering descriptions; type 'next' for next file search; type 'exit' to quit the search):")
    while True:
        user_input = input("> ").strip()
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

# Parse the FASTA file to store the headers and sequences efficiently
def parse_fasta(filename):
    sequences = {}
    header = None
    try: # Starts a "try-except" block to handle potential errors
        with open(filename, 'r') as f: # Opens the specified filename in read-only mode, and assigns the file objects to the variable f
            for line in f: # Iterates through each line of the file
                line = line.rstrip() # Removes trailing whitespace, including (\n), from the end of each line
                if line.startswith('>'): 
                    if header is not None: # If a previous header and sequence were being tracked
                        sequences[header] = sequence # If so, saves the previous sequence into the sequences dictionary with the header as key
                    header = line[1:] # Then, updates the header variable to the new header. Remove the '>'
                    sequence = "" # Resets the sequence variable to an empty string, ready to accumulate the lines for a new sequence
                else:
                    sequence += line # If the line doesn't start with >, it appends this line to the current sequence string as being part of the sequence data
            if header is not None: # Add the last sequence
                sequences[header] = sequence  
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.\n")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
    
    return sequences

# Search and Display Results
def search_fasta(descriptions, sequences): # keys: header descriptions; values: DNA/protein sequences
    found_count = 0 # Initializes a counter to track how many matches are found
    for header, sequence in sequences.items(): # Iterates through each key (header) and value (sequence) pair in the sequences dictionary
        # Checks if every string in the user's descriptions list exists within the current header string
        if all(desc in header for desc in descriptions):  
            print(f"\n--- Match Found ---")
            print(f"Header: >{header}\n")
            print(f"Sequence: {sequence}\n")
            print(f"Length: {len(sequence)}")
            print(f"-------------------")
            found_count += 1
    if found_count == 0:
        print("No sequences found matching the descriptions.")

    print(f"{found_count} matches found\n") # Summarize the amount of matches were found

# Save search results to file
def save_results_to_file(filename, descriptions, sequences):
    try:
        with open(filename, 'w') as f: # Opens a file specified by filename in write mode ('w'). The file object is assigned to the variable f
            original_stdout = sys.stdout # Redirect the standard output (stdout) to the file f
            sys.stdout = f
            search_fasta(descriptions, sequences) # The output of this function will be written to the file f because sys.stdout has been redirected
            sys.stdout = original_stdout  # Reset stdout
        print(f"\nSuccessfully saved results to {filename}\n")
    except IOError as e:
        print(f"Error saving file: {e}\n")

# Asks the user if they want to save search results to a file
def save_results_prompt(descriptions, sequences):
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
    
# Main function for the program's execution
def main():
    FASTA_FILE_NAME = input("Please enter the name of the FASTA file (e.g., sequences.fasta or faa): ")
    fasta_data = parse_fasta(FASTA_FILE_NAME)

    if fasta_data is None: # If the file cannot be read, ask for the file again until it is loaded successfully
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
