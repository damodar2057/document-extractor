import os

class Settings:
    def __init__(self):
        self.app_name = os.getenv('APP_NAME', 'Document Extractor')
        self.app_prefix = os.getenv('API_PREFIX', '/api/v1')


        # Open AI Settings
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.openai_model = os.getenv("OPENAI_MODEL", 'gpt-4o-mini')


settings = Settings()