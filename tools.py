


def parse_command(command):
    if command == "print":
        print("Hello World!")
    elif command == "light_on":
        print("Turning on the light")
    elif command == "light_off":
        print("Turning off the light")
    elif command == "exit":
        print("Exiting program")
        exit()
    else:
        print("Invalid command") 