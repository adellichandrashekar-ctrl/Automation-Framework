import os
import json
from dotenv import load_dotenv

load_dotenv()  # loads the environment variables from .env


class Config:
    """
    Loads settings for environments.json
    """
    def __init__(self, env=None):
        self.env = env or "dev"

        config_file = os.path.join(os.path.dirname(__file__), "environments.json")

        with open(config_file, "r") as f:
            all_envs = json.load(f)

        self._settings = all_envs.get(self.env, all_envs["dev"])

    @property
    def base_url(self):
        return self._settings.get("base_url")
    
    @property
    def ui_url(self):
        return self._settings.get("ui_url")
    
    @property
    def timeout(self):
        return self._settings.get("timeout", 10)
    
    @property
    def auth_username(self):
        return self._settings.get("auth_username")
    
    @property
    def auth_password(self):
        return self._settings.get("auth_password")
    
    def get(self, key, default=None):
        """Get any setting by key name"""
        env_val = os.environ.get(key) or os.environ.get(key.upper())
        if env_val:
            return env_val

        return self._settings.get(key, default)
    
    def __repr__(self):
        return f"Config(env='{self.env}', base_url='{self.base_url}')"


