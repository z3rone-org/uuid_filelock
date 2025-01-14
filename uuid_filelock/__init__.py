import os
import time
import uuid
from datetime import datetime


class UUIDFileLock:
    default_verification_delay: float = 0.1
    default_retry_interval: float = 0.1
    def __init__(self,
                 lock_file: str,
                 prefix='',
                 verification_delay: float = None,
                 retry_interval: float = None,
                 timeout_interval: float = -1):
        """
        Initialize the UUIDFileLock.

        Args:
            lock_file (str): Path to the lock file.
            verification_delay (float): Time to wait before verifying lock (in seconds).
            retry_interval (float): Time to wait before retrying (in seconds).
        """
        self.lock_file = str(lock_file)
        self.lock_id = f'{prefix}{uuid.uuid4()}'
        self.timeout_interval = timeout_interval

        if verification_delay is None:
            self.verification_delay = UUIDFileLock.default_verification_delay
        else:
            self.verification_delay = verification_delay

        if retry_interval is None:
            self.retry_interval = UUIDFileLock.default_retry_interval
        else:
            self.retry_interval = retry_interval

    def acquire(self):
        """
        Acquire the lock by following the UUID-based file lock mechanism.
        """
        start_time = datetime.now()

        while True:
            if not os.path.exists(self.lock_file):
                # Attempt to create the lock file with the UUID
                with open(self.lock_file, 'w') as f:
                    f.write(self.lock_id)

                # Wait a moment and verify the lock
                time.sleep(self.verification_delay)
                try:
                    with open(self.lock_file, 'r') as f:
                        lock_content = f.read().strip()
                except FileNotFoundError:
                    # Deleted by lock holder
                    lock_content = None

                if lock_content == self.lock_id:
                    # Successfully acquired the lock
                    return

            if self.timeout_interval >= 0.0:
                if (datetime.now() - start_time).total_seconds() > self.timeout_interval:
                    raise LockTimeoutException()

            # If the lock file exists or the content mismatches, retry
            time.sleep(self.retry_interval)

    def check_lock(self):
        try:
            with open(self.lock_file, 'r') as f:
                lock_content = f.read().strip()
        except FileNotFoundError:
            # No lock file present
            return False

        if lock_content == self.lock_id:
            # Successfully acquired the lock
            return True

        # Otherwise not locked
        return False

    def release(self):
        """
        Release the lock if it is held by this instance.
        """
        if os.path.exists(self.lock_file):
            with open(self.lock_file, 'r') as f:
                lock_content = f.read().strip()

            if lock_content == self.lock_id:
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

class LockTimeoutException(Exception):
    def __init__(self, message="acquiring lock timed out"):
        super().__init__(message)