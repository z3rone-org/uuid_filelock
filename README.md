# UUID File Lock

[![PyPi badge](https://img.shields.io/pypi/v/uuid-filelock)](https://pypi.org/project/uuid-filelock/)

A simple UUID-based file lock implementation for Python. This package provides a lightweight and effective way to coordinate access to shared resources using a lock file mechanism.
This does not require any file locking capabilities of the underlying filesystem or network share.

## How It Works

1. **Lock File Check:** The system checks if the lock file exists.
2. **Lock Creation:** If no lock file exists, it creates one and writes a unique UUID to it.
3. **Verification:** The lock waits briefly and then verifies if the UUID matches the one it wrote.
4. **Retry Logic:** If the UUID mismatches or the lock file already exists, it retries after a delay.
5. **Release Mechanism:** When the lock is released, the lock file is deleted if it contains the same UUID.

This mechanism ensures that only one process can hold the lock at any time, making it ideal for coordinating file or resource access across multiple processes.

*Note: In order for this to work over a network share the `verification_delay` needs to be larger than the time it takes for a client to detect that another has created a file.*

![working principal](https://raw.githubusercontent.com/z3rone-org/uuid_filelock/refs/heads/main/docs/uuid_filelock.png)
## Installation

Install the package via pip:

```bash
pip install uuid-filelock
```

## Usage

You can use the `UUIDFileLock` class to acquire and release locks in your Python code. The class also supports usage within a `with` clause for convenience.

### Example: Using the Lock Explicitly

```python
import time
from uuid_filelock import UUIDFileLock

lock_file_path = "/tmp/mylockfile.lock"
lock = UUIDFileLock(lock_file_path)

print("Acquire lock...")
lock.acquire()
print("Lock acquired!")

# Perform critical section tasks here
# Simulating work
time.sleep(5)

# Release the lock
lock.release()
print("Lock released.")
```

### Example: Using the Lock in a `with` Clause

```python
import time
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
- `prefix` (str, default=""): A custom prefix for the UUID to help debugging. 
- `verification_delay` (float, default=1.0): Time to wait before verifying that the lock was acquired.
- `retry_interval` (float, default=0.1): Time to wait before retrying if the lock cannot be acquired.
- `timeout_interval` (float, default=-1): Timeout for acquiring lock. Set to negative value for no timeout.

## Change Default Values
You can change the default values for `verification_delay` and `retry_interval`
via `UUIDFileLock.verification_delay=<new_value>` and `UUIDFileLock.retry_interval=<new_value>` respectively.

## License

This package is licensed under the MIT License.

