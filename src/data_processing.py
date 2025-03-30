
import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PasswordDataProcessor:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.datasets = {}

    def load_rockyou_dataset(self, filename='rockyou.txt', encoding='latin-1'):

        filepath = os.path.join(self.data_dir, filename)

        if not os.path.exists(filepath):
            logger.error(f"Dataset file not found: {filepath}")
            logger.info("Please download the RockYou dataset and place it in the data directory.")
            return None

        try:
            logger.info(f"Loading password dataset: {filepath}")
            with open(filepath, 'r', encoding=encoding, errors='ignore') as file:
                passwords = [line.strip() for line in file if line.strip()]

            df = pd.DataFrame(passwords, columns=['password'])

            df['length'] = df['password'].apply(len)

            self.datasets['rockyou'] = df
            logger.info(f"Loaded {len(df)} passwords from RockYou dataset.")
            return df

        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return None

    def get_common_passwords(self, top_n=1000):

        if 'rockyou' not in self.datasets:
            logger.warning("RockYou dataset not loaded. Call load_rockyou_dataset first.")
            return []

        return self.datasets['rockyou']['password'].value_counts().head(top_n).index.tolist()


if __name__ == "__main__":
    processor = PasswordDataProcessor()
