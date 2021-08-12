import os

JUEJIN_USERNAME = os.getenv("JUEJIN_USERNAME")
JUEJIN_PASSWORD = os.getenv("JUEJIN_PASSWORD")
JUEJIN_NICKNAME = os.getenv("JUEJIN_NICKNAME")

MAIL_ADDRESS = os.getenv("MAIL_ADDRESS")
MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
MAIL_TO = os.getenv("MAIL_TO")
MAIL_USER = os.getenv("MAIL_USER")

SWITCH = os.getenv("SWITCH", "on")
PUBLISH_SWITCH = os.getenv("PUBLISH_SWITCH", "off")
