__author__ = "Cees van de Griend <cees@griend.eu>"
__status__ = "development"
__version__ = "0.1"
__date__ = "31 december 2022"

config = {}

config["CHECK_NAME"] = "Google"
config["CHECK_URL"] = "https://www.google.com/"

config["ACTIVEMQ_HOSTNAME"] = "dev01.kade3.home"
config["ACTIVEMQ_PORT"] = 61613
config["ACTIVEMQ_USERNAME"] = "admin"
config["ACTIVEMQ_PASSWORD"] = "admin"
config["ACTIVEMQ_QUEUE"] = "/topic/checks"


if __name__ == "__main__":
    print(f"Hostname: {config['ACTIVEMQ_HOSTNAME']}:{config['ACTIVEMQ_PORT']}")
    print(f"Username: {config['ACTIVEMQ_USERNAME']}")
    print(f"Queue:    {config['ACTIVEMQ_QUEUE']}")
    print(f"{config['CHECK_NAME']} - {config['CHECK_URL']}")
