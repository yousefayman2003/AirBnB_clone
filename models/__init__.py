"""Initialize the models Package"""

from models.engine.file_storage import FileStorage

# Create an instance of FileStorage
storage = FileStorage()

# Reload the storage to load any existing data
storage.reload()
