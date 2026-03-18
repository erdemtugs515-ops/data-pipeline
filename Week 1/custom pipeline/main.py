from hierarchy import hierarchy, TemperatureSensor, HumiditySensor, MotionSensor

CSV_FILE = "iot_data.csv"

devices = [] 


def add_device():
    print("\n  1: Temperature  2: Humidity  3: Motion")
    choice = input("Choose type:").strip()

    if choice == "1":
        device_class = TemperatureSensor
    elif choice == "2":
        device_class = HumiditySensor
    elif choice == "3":
        device_class = MotionSensor
    else:
        print(" Invalid choice.")
        return

    device_id = input("Device ID: ").strip()
    location = input("Location: ").strip()
    data_input = input("Data (temp=22,unit=C): ").strip()

    # Simple data parsing
    data = {}
    if data_input:
        pairs = data_input.split(",")
        for pair in pairs:
            if "=" in pair:
                key, value = pair.split("=", 1)
                data[key.strip()] = value.strip()

    device = device_class(device_id=device_id, location=location, data=data)
    devices.append(device)
    print(f" Added device: {device_class.__name__}")


def serialize():
    """saving devices to csv file"""
    if not devices:
        print(" No devices to save.")
        return
    try:
        with open(CSV_FILE, "w", encoding="utf-8") as f:
            f.write("device_type,device_id,location,data\n")
            for device in devices:
                row = device.to_row()
                line = row[0] + "," + row[1] + "," + \
                    row[2] + "," + row[3] + "\n"
                f.write(line)
        print(f" Saved {len(devices)} devices to file.")
    except Exception as e:
        print(f" Save failed: {e}")


def deserialize():
    """loading devices from csv"""
    try:
        devices.clear()
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i in range(1, len(lines)): 
                line = lines[i].strip()
                if line:
                    parts = line.split(",")
                    if len(parts) >= 4:
                        devices.append(hierarchy.from_row(parts))
        print(f" Loaded {len(devices)} devices:")
        for device in devices:
            print(f"{device}")
    except FileNotFoundError:
        print(" File not found. Please save devices first.")
    except Exception as e:
        print(f" Load failed: {e}")


def main():
    while True:
        print("""

  IoT Data Pipeline        

  1: Add IoT Device          
  2: Serialize Data          
  3: Deserialize Data        
  0: Exit                    """)

        choice = input("Choice:").strip()

        if choice == "0":
            print("Exiting...")
            break
        elif choice == "1":
            add_device()
        elif choice == "2":
            serialize()
        elif choice == "3":
            deserialize()
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()