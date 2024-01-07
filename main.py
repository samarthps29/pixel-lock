# use binary representations of alphabets a -> 1 -> 00001, z -> 26 -> 011010
from pattern import Pattern
from utils import filter, convert, render, readConfigFile


def encrypt(plainText: str, configFilePath: str) -> Pattern:
    filteredPlainText = filter(plainText)
    convertedPlainText = convert(filteredPlainText)
    config = readConfigFile(configFilePath)
    pattern = Pattern((config["ROWS"], config["COLS"]), (config["CENTERX"], config["CENTERY"]), config["RADIUS"],
                      config["ANGLEINCREMENT"], config["ANGLEDECREMENT"], config["LAYERGAP"])
    pattern.encrypt(convertedPlainText)
    return pattern


def decrypt(imagePath: str, configFilePath: str) -> str:
    config = readConfigFile(configFilePath)
    return render(Pattern.decrypt((config["CENTERX"], config["CENTERY"]), config["RADIUS"],
                                  config["ANGLEINCREMENT"], config["ANGLEDECREMENT"], config["LAYERGAP"], imagePath)).strip()


def main() -> None:
    while True:
        print("Encrypt (e) | Decrypt (d)")
        inp = input("Enter your choice : ").lower().strip()
        if (inp == "q"):
            return
        elif (inp == "e"):
            plainText = input("Enter data to be encrypted: \n")
            configFilePath = input("Enter your config file path: ")
            pattern = encrypt(plainText=plainText,
                              configFilePath=configFilePath)
            pattern.save()
        elif (inp == "d"):
            imagePath = input("Enter the file path: ")
            configFilePath = input("Enter your config file path: ")
            print(decrypt(imagePath=imagePath, configFilePath=configFilePath))
        else:
            print("Invalid choice, try again")


if (__name__ == "__main__"):
    main()
