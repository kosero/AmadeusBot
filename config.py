import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


# BOT
BOT_TOKEN: str = config["bot"]["token"]
VERSION: str = config["bot"]["version"]

# Ai
GEMINI_TOKEN: str = config["ai"]["gemini_token"]
MAX_HISTORY: int = config["ai"]["max_history"]

# Lum
LUM_GUILD: int = config["lum"]["guild_id"]
LUM_WAIT_ROLE: int = config["lum"]["wait_role_id"]
BIG_BROTHER_WATCHING: int = config["lum"]["register_watch_role_id"]
LUM_REGISTER_ALLOWED_ROL_OR_MEMBER = config["lum"]["register_allowed_rol_or_member"]
LUM_USER_LOG_CH: int = config["lum"]["lum_user_log_ch"]
ZINCIRLI_CH: int = config["lum"]["zincirli_ch"]

# GOS
GOS_GUILD: int = config["gos"]["guild_id"]
GOS_WAIT_ROLE: int = config["gos"]["wait_role_id"]
