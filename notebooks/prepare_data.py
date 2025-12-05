import pandas as pd
import os

def prepare_spam_dataset():
    """
    Converts the raw, tab-separated spam data into a clean CSV format.
    """
    # Define file paths relative to the project root
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    raw_data_path = os.path.join(base_dir, 'data', 'spam_raw.txt')
    processed_data_path = os.path.join(base_dir, 'data', 'spam.csv')

    print("--- Starting Data Preparation ---")

    if not os.path.exists(raw_data_path):
        print(f"Error: Raw data file not found at {raw_data_path}")
        return

    print(f"Reading raw data from: {raw_data_path}")
    
    # Read the tab-separated file into a pandas DataFrame
    # Use 'latin-1' encoding to handle special characters in the dataset
    df = pd.read_csv(
        raw_data_path, 
        sep='\t', 
        header=None, 
        names=['v1', 'v2'],
        encoding='latin-1'
    )

    print(f"Successfully loaded {len(df)} records.")
    
    # Save the DataFrame to a CSV file, which the training script expects
    df.to_csv(processed_data_path, index=False)
    
    print(f"Successfully created processed data file at: {processed_data_path}")
    print("--- Data Preparation Complete ---")

if __name__ == "__main__":
    prepare_spam_dataset()