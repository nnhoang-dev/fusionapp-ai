class FusionAppConfig:
    def __init__(self, app_name="fusion", host="127.0.0.1", port=8000):
        self.app_name = app_name
        self.host = host
        self.port = port

    def __str__(self):
        return f"FusionAppConfig(app_name={self.app_name}, host={self.host}, port={self.port})"

    def to_dict(self):
        return {"app_name": self.app_name, "host": self.host, "port": self.port}
