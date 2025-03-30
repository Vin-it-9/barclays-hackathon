
from src.model import PasswordStrengthModel


def main():
    print("Initializing password strength model...")
    model = PasswordStrengthModel()

    print("Preparing training data from RockYou dataset...")
    passwords, labels = model.prepare_training_data_from_rockyou()

    if passwords and labels:
        print(f"Training model with {len(passwords)} passwords...")
        model.train(passwords, labels)
        model.save_model()
        print("Model training complete and saved.")
    else:
        print("Failed to prepare training data.")


if __name__ == "__main__":
    main()