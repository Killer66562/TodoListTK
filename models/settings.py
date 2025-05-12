import json
import pathlib


class Settings:
    def __init__(self):
        self.font_size: int = 10
        self.dark_mode: bool = False
        self.notify: bool = True

    @staticmethod
    def from_json(fp: str):
        try:
            path = pathlib.Path(fp)
            with open(path, mode="r", encoding="utf-8") as file:
                data = json.load(file)

            font_size = min(max(int(data.get('font_size')), 10), 14)
            dark_mode = bool(data.get('dark_mode'))
            notify = bool(data.get('notify'))

            settings = Settings()
            settings.font_size = font_size
            settings.dark_mode = dark_mode
            settings.notify = notify

            return settings
        except:
            return Settings()
        
    def _to_dict(self) -> dict:
        return {
            'font_size': self.font_size, 
            'dark_mode': self.dark_mode, 
            'notify': self.notify
        }
    
    def load(self, fp: str):
        try:
            path = pathlib.Path(fp)
            with open(path, mode="r", encoding="utf-8") as file:
                data = json.load(file)

            font_size = min(max(int(data.get('font_size')), 10), 14)
            dark_mode = bool(data.get('dark_mode'))
            notify = bool(data.get('notify'))

            self.font_size = font_size
            self.dark_mode = dark_mode
            self.notify = notify

            self.save(fp)
        except:
            self.save(fp)
        
    def save(self, fp: str):
        path = pathlib.Path(fp)
        with open(path, mode="w", encoding="utf-8") as file:
            json.dump(self._to_dict(), file, indent=4)
        