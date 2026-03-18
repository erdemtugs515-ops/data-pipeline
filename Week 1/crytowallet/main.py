from wallet import CryptoWallet


def display_menu():
    print("Crypto wallet UI")
    print("1: Create Wallet")
    print("2: Deposit")
    print("3: Withdraw")
    print("4: Check Balance")
    print("5: Transaction History")
    print("0: Exit")


def main():
    wallets = {}
    current_wallet = None

    print("Welcome to your crypto Wallet!")

    while True:
        display_menu()

        if current_wallet:
            print(
                f"Current Wallet ID: {current_wallet.get_wallet_id()} | Balance: ${current_wallet.get_balance():.2f}")

        if wallets:
            print(f"Total Wallets Created: {len(wallets)}")

        choice = input("\nEnter your choice (0-5): ").strip()

        if choice == "0":
            print("Thank you for using the Cryptocurrency Wallet!")
            break

        elif choice == "1":
            print("\n--- Create New Wallet ---")
            initial_amount = input(
                "Enter initial balance (press Enter for 0): ").strip()

            if initial_amount == "":
                initial_amount = 0.0
            else:
                try:
                    initial_amount = float(initial_amount)
                except ValueError:
                    print("Error: Invalid amount. Creating wallet with $0.00")
                    initial_amount = 0.0

            try:
                wallet = CryptoWallet(initial_amount)
                wallet_id = wallet.get_wallet_id()
                wallets[wallet_id] = wallet
                current_wallet = wallet
                print(f"Wallet created! ID: {wallet_id}")
                print("This wallet is now your active wallet.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            if not current_wallet:
                print("Error: Please create a wallet first.")
                continue

            amount = input("Enter deposit amount: $")
            current_wallet.deposit(amount)

        elif choice == "3":
            if not current_wallet:
                print("Error: Please create a wallet first.")
                continue

            amount = input("Enter withdrawal amount: $")
            current_wallet.withdraw(amount)

        elif choice == "4":
            if not current_wallet:
                print("Error: Please create a wallet first.")
                continue

            print(f"\nCurrent Balance: ${current_wallet.get_balance():.2f}")

        elif choice == "5":
            if not current_wallet:
                print("Error: Please create a wallet first.")
                continue

            current_wallet.show_transaction_history()

        else:
            print("Error: Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()