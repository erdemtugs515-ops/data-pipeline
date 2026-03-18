from counter import Counter

def main():
    print("Program starting.")
    print("Initializing counter...")
    counter = Counter()
    print("Counter initialized.")

    while True:
        print("\nOptions:")
        print("1: Add count")
        print("2: Get count")
        print("3: Zero count")
        print("0: Exit program")

        choice = input("Choice: ")

        if choice == "1":
            counter.addCount()
            print("Count increased")
        elif choice == "2":
            print(f"Current count '{counter.getCount()}'")
        elif choice == "3":
            counter.zeroCount()
            print("Count zeroed")
        elif choice == "0":
            print("Program ending.")
            break
        else:
            print("Unknown Input.")

if __name__ == "__main__":
    main()
