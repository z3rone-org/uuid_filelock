import os
import time
import uuid
from typing import Optional

class UUIDFileLock:
    def __init__(self, lock_file: str, retry_interval: float = 1.0):
        """
        Initialize the UUIDFileLock.

        Args:
            lock_file (str): Path to the lock file.
            retry_interval (float): Time to wait before retrying (in seconds).
        """
        self.lock_file = str(lock_file)
        self.retry_interval = retry_interval
        self.my_uuid = str(uuid.uuid4())

    def acquire(self):
        """
        Acquire the lock by following the UUID-based file lock mechanism.
        """
        while True:
            if not os.path.exists(self.lock_file):
                # Attempt to create the lock file with the UUID
                with open(self.lock_file, 'w') as f:
                    f.write(self.my_uuid)

                # Wait a moment and verify the lock
                time.sleep(self.retry_interval)
                try:
                    with open(self.lock_file, 'r') as f:
                        lock_content = f.read().strip()
                except FileNotFoundError:
                    # Deleted by lock holder
                    lock_content = None

                if lock_content == self.my_uuid:
                    # Successfully acquired the lock
                    return

            # If the lock file exists or the content mismatches, retry
            time.sleep(self.retry_interval)

    def release(self):
        """
        Release the lock if it is held by this instance.
        """
        if os.path.exists(self.lock_file):
            with open(self.lock_file, 'r') as f:
                lock_content = f.read().strip()

            if lock_content == self.my_uuid:
                os.remove(self.lock_file)

    def __enter__(self):
        """
        Context management entry point.
        """
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Context management exit point.
        """
        self.release()

