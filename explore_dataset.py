
from src.data_processing import PasswordDataProcessor
import pandas as pd
import matplotlib.pyplot as plt


def main():

    processor = PasswordDataProcessor()

    print("Loading RockYou dataset...")
    df = processor.load_rockyou_dataset()

    if df is not None:

        print(f"\nDataset loaded successfully with {len(df)} passwords.")
        print(f"\nPassword length statistics:")
        print(df['length'].describe())

        print("\nMost common password lengths:")
        print(df['length'].value_counts().sort_index().head(20))

        print("\nTop 10 most common passwords:")
        top_passwords = df['password'].value_counts().head(10)
        for pwd, count in top_passwords.items():
            print(f"  '{pwd}': {count} occurrences")

        plt.figure(figsize=(10, 6))
        df['length'].plot(kind='hist', bins=30, title='Password Length Distribution')
        plt.xlabel('Password Length')
        plt.ylabel('Frequency')
        plt.savefig('password_length_distribution.png')
        print("\nSaved password length distribution to 'password_length_distribution.png'")


if __name__ == "__main__":
    main()