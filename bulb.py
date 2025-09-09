print("💡 Bulb Control Program")
print("Type 'on' to turn ON, 'off' to turn OFF, 'exit' to quit")

bulb_state = "OFF"

while True:
    print(f"\nCurrent Bulb State: {bulb_state}")
    command = input("Enter command (on/off/exit): ").lower()

    if command == "on":
        if bulb_state == "ON":
            print("The bulb is already ON.")
        else:
            bulb_state = "ON"
            print("The bulb is now ON.")
    elif command == "off":
        if bulb_state == "OFF":
            print("The bulb is already OFF.")
        else:
            bulb_state = "OFF"
            print("The bulb is now OFF.")
    elif command == "exit":
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid command. Please type 'on', 'off', or 'exit'.")