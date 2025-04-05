from src.data_processing import PasswordDataProcessor
import pandas as pd
import matplotlib.pyplot as plt

def main():
    processor = PasswordDataProcessor()

    print("Loading RockYou dataset...")
    df = processor.load_rockyou_dataset()

    if df is not None:
        print(f"\nDataset loaded successfully with {len(df)} passwords.")

        sample_size = 1000000
        if len(df) > sample_size:
            df_sample = df.sample(n=sample_size, random_state=42)
        else:
            df_sample = df

        print(f"\nRandomly selected {len(df_sample)} passwords for analysis.")

        print(f"\nPassword length statistics (random sample):")
        print(df_sample['length'].describe())

        print("\nMost common password lengths (random sample):")
        print(df_sample['length'].value_counts().sort_index().head(20))

        print("\nTop 10 most common passwords (random sample):")
        top_passwords = df_sample['password'].value_counts().head(10)
        for pwd, count in top_passwords.items():
            print(f"  '{pwd}': {count} occurrences")

        plt.figure(figsize=(10, 6))
        df_sample['length'].plot(kind='hist', bins=30, title='Password Length Distribution (Random Sample of 1M)')
        plt.xlabel('Password Length')
        plt.ylabel('Frequency')
        plt.tight_layout()  # Ensures the chart is neatly filled with data
        plt.savefig('password_length_distribution.png')
        print("\nSaved password length distribution to 'password_length_distribution.png'")

if __name__ == "__main__":
    main()
