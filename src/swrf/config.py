import os

config = {}

config["CHECK_NAME"] = os.environ.get("CHECK_NAME", "Google")
config["CHECK_URL"] = os.environ.get("CHECK_URL", "https://www.google.com/")

config["ACTIVEMQ_HOSTNAME"] = os.environ.get("ACTIVEMQ_HOSTNAME", "dev01.kade3.home")
config["ACTIVEMQ_PORT"] = int(os.environ.get("ACTIVEMQ_PORT", "61613"))
config["ACTIVEMQ_USERNAME"] = os.environ.get("ACTIVEMQ_USERNAME", "admin")
config["ACTIVEMQ_PASSWORD"] = os.environ.get("ACTIVEMQ_PASSWORD", "admin")
config["ACTIVEMQ_TOPIC"] = os.environ.get("ACTIVEMQ_TOPIC", "/topic/check")


if __name__ == "__main__":
    print(f"Hostname:     {config['ACTIVEMQ_HOSTNAME']}:{config['ACTIVEMQ_PORT']}")
    print(f"Username:     {config['ACTIVEMQ_USERNAME']}")
    print(f"Check:        {config['ACTIVEMQ_TOPIC']}")
    print(f"{config['CHECK_NAME']} - {config['CHECK_URL']}")
