import json
import os
from contextvars import ContextVar
from threading import Lock

# Context var para el idioma
current_lang: ContextVar[str] = ContextVar("current_lang", default="en")


class I18nService:
    _instances = {}
    _lock = Lock()

    def __new__(cls, root_dir: str):
        # Singleton por root_dir
        with cls._lock:
            if root_dir not in cls._instances:
                instance = super().__new__(cls)
                instance._init(root_dir)
                cls._instances[root_dir] = instance
            return cls._instances[root_dir]

    def _init(self, root_dir: str):
        self.root_dir = root_dir
        self._messages = None
        self._load_messages()

    def _load_messages(self):
        path = os.path.join(self.root_dir, "message.json")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"No se encontró el fichero de mensajes: {path}")
        with open(path, "r", encoding="utf-8") as f:
            self._messages = json.load(f)

    def set_language(self, lang: str):
        current_lang.set(lang)

    def get_language(self):
        return current_lang.get()

    def gettext(self, key: str) -> str:
        lang = current_lang.get()
        entry = self._messages.get(key)
        if not entry:
            return f"[Missing key: {key}]"
        # Retornar la traducción o fallback en inglés
        return entry.get(lang) or entry.get("en") or f"[Missing translation: {key}]"
