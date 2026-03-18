class SmartDevice:
    def __init__(self, device_name):
        self.device_name = device_name
        self.status = "off"

    def operate(self):
        pass


class SmartLight(SmartDevice):
    def __init__(self, device_name, brightness=50):
        super().__init__(device_name)
        self.brightness = brightness

    def operate(self):
        if self.status == "off":
            self.status = "on"
            print(f"{self.device_name} is now ON with brightness {self.brightness}%")
        else:
            self.status = "off"
            print(f"{self.device_name} is now OFF")


class SmartThermostat(SmartDevice):
    def __init__(self, device_name, temperature=22):
        super().__init__(device_name)
        self.temperature = temperature

    def operate(self):
        if self.status == "off":
            self.status = "on"
            print(
                f"{self.device_name} is now ON - Temperature set to {self.temperature}°C")
        else:
            self.status = "off"
            print(f"{self.device_name} is now OFF")


class SmartLock(SmartDevice):
    def __init__(self, device_name):
        super().__init__(device_name)
        self.locked = True

    def operate(self):
        if self.locked:
            self.locked = False
            self.status = "unlocked"
            print(f"{self.device_name} is now UNLOCKED")
        else:
            self.locked = True
            self.status = "locked"
            print(f"{self.device_name} is now LOCKED")


def operate_devices(devices):
    if not devices:
        print("No devices available")
        return

    for device in devices:
        device.operate()


def main():
    devices = []

    while True:
        print("\n Smart Home System")
        print("1 - Add Smart Device")
        print("2 - Operate Devices")
        print("0 - Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 0:
                print("Exiting Smart Home System")
                break

            elif choice == 1:
                print("\nDevice Types:")
                print("1: Smart Light")
                print("2: Smart Thermostat")
                print("3: Smart Lock")

                try:
                    device_type = int(input("Select device type: "))
                    device_name = input("Enter device name: ")

                    if device_type == 1:
                        brightness = int(input("Enter brightness (1-100): "))
                        devices.append(SmartLight(device_name, brightness))
                        print(
                            f"Smart Light '{device_name}' added successfully")

                    elif device_type == 2:
                        temperature = int(input("Enter temperature: "))
                        devices.append(SmartThermostat(
                            device_name, temperature))
                        print(
                            f"Smart Thermostat '{device_name}' added successfully")

                    elif device_type == 3:
                        devices.append(SmartLock(device_name))
                        print(f"Smart Lock '{device_name}' added successfully")

                    else:
                        print("Invalid device type")

                except ValueError:
                    print("Invalid input. Please enter a number")

            elif choice == 2:
                print("\nOperating all devices:")
                operate_devices(devices)

            else:
                print("Invalid choice. Please enter a valid choice.")

        except ValueError:
            print("Invalid input. Please enter a number")


if __name__ == "__main__":
    main()