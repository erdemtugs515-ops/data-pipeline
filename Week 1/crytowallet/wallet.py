import random


class CryptoWallet:
    def __init__(self, initial_balance=0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self._balance = float(initial_balance)
        self._wallet_id = f"WALLET{random.randint(10000, 99999)}"
        self._transaction_history = []

        if initial_balance > 0:
            self._add_transaction("Initial Deposit", initial_balance)

    def get_wallet_id(self):
        return self._wallet_id

    def get_balance(self):
        return self._balance

    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                print("Error: Deposit amount must be positive")
                return False

            self._balance += amount
            self._add_transaction("Deposit", amount)
            print(
                f"Successfully deposited ${amount:.2f}. New balance: ${self._balance:.2f}")
            return True
        except (ValueError, TypeError):
            print("Error: Please enter a valid number")
            return False

    def withdraw(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                print("Error: Withdrawal amount must be positive")
                return False

            if amount > self._balance:
                print(
                    f"Error: Insufficient funds. Current balance: ${self._balance:.2f}")
                return False

            self._balance -= amount
            self._add_transaction("Withdrawal", -amount)
            print(
                f"Successfully withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")
            return True
        except (ValueError, TypeError):
            print("Error: Please enter a valid number")
            return False

    def _add_transaction(self, transaction_type, amount):
        transaction = {
            'type': transaction_type,
            'amount': amount,
            'balance': self._balance
        }
        self._transaction_history.append(transaction)

    def show_transaction_history(self):
        if not self._transaction_history:
            print("No transactions found.")
            return

        print(f"\nTransaction History for Wallet {self._wallet_id}")
        print("-" * 50)
        for transaction in self._transaction_history:
            print(
                f"{transaction['type']} | ${transaction['amount']:+.2f} | Balance: ${transaction['balance']:.2f}")
        print("-" * 50)