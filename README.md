# UUID File Lock

A simple UUID-based file lock implementation for Python. This package provides a lightweight and effective way to coordinate access to shared resources using a lock file mechanism.

## How It Works

1. **Lock File Check:** The system checks if the lock file exists.
2. **Lock Creation:** If no lock file exists, it creates one and writes a unique UUID to it.
3. **Verification:** The lock waits briefly and then verifies if the UUID matches the one it wrote.
4. **Retry Logic:** If the UUID mismatches or the lock file already exists, it retries after a delay.
5. **Release Mechanism:** When the lock is released, the lock file is deleted if it contains the same UUID.

This mechanism ensures that only one process can hold the lock at any time, making it ideal for coordinating file or resource access across multiple processes.

## Installation

Install the package via pip:

```bash
pip install uuid-filelock
```

## Usage

You can use the `UUIDFileLock` class to acquire and release locks in your Python code. The class also supports usage within a `with` clause for convenience.

### Example: Using the Lock Explicitly

```python
from uuid_filelock import UUIDFileLock

lock_file_path = "/tmp/mylockfile.lock"
lock = UUIDFileLock(lock_file_path)

try:
    print("Trying to acquire lock...")
    lock.acquire()
    print("Lock acquired!")

    # Perform critical section tasks here
    # Simulating work
    time.sleep(5)

finally:
    lock.release()
    print("Lock released.")
```

### Example: Using the Lock in a `with` Clause

```python
from uuid_filelock import UUIDFileLock

lock_file_path = "/tmp/mylockfile.lock"

with UUIDFileLock(lock_file_path) as lock:
    print("Lock acquired!")
    # Perform critical section tasks
    time.sleep(5)  # Simulate work
    print("Work done!")

# The lock is automatically released when the block exits.
print("Lock released.")
```

## Parameters

- `lock_file` (str): The path to the lock file.
- `retry_interval` (float, default=1.0): Time to wait before retrying if the lock cannot be acquired.

## License

This package is licensed under the MIT License.

