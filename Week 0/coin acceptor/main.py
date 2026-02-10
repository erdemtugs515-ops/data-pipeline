from coin_acceptor import CoinAcceptor

def displayOptions() -> None:
    print("1: Insert coin")
    print("2: Show coins")
    print("3: Return coins")
    print("0: Exit")

def main() -> None:
    print("Program starting.")
    ca = CoinAcceptor()


    while True:
        displayOptions()
        try:
            option = int(input("Your choice: "))
        except ValueError:
            print("Invalid input, please input an Integer... \n")
            continue
        if(option == 1):
            ca.insertCoin()
        elif(option == 2):
            val = ca.getAmount()
            print(f"Currently '{val}' coins counted.")
        elif(option == 3):
            val = ca.returnCoins()
            print(f"Coin acceptor returned '{val}' coins.")

        elif(option == 0):
            break

        else:
            print("Unknown input, please try again.")
        
    print("\nProgram ending.") #\n creates a new line
    return None

if __name__ == "__main__":
    main()