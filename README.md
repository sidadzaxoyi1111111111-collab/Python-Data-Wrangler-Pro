import pandas as pd

def clean_ai_training_data():
    # Creating a sample dataset (Real-world scenario for AI training)
    data = {
        'text_id': [1, 2, 3, 2, 5],
        'input_text': ['Hello AI', 'Data cleaning', 'Machine learning', 'Data cleaning', 'Python code'],
        'label': ['Greeting', 'Process', 'Field', 'Process', 'Code']
    }
    
    df = pd.DataFrame(data)
    
    # 1. Removing Duplicate Entries (Essential for model training)
    clean_df = df.drop_duplicates()
    
    print("--- QA Data Processing Status ---")
    print(f"Total records processed: {len(df)}")
    print(f"Unique records saved: {len(clean_df)}")
    
    return clean_df

if __name__ == "__main__":
    processed_data = clean_ai_training_data()
    print("\nCleaned Data Sample:")
    print(processed_data)
