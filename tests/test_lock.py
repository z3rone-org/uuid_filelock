import pytest
import uuid
import os
from uuid_filelock import UUIDFileLock


@pytest.fixture
def lock_file(tmpdir):
    # Create a temporary lock file
    return tmpdir.join("test_lock_file")


@pytest.fixture
def mock_uuid():
    # Return a mocked UUID
    return str(uuid.uuid4())


def test_acquire_lock(lock_file, mock_uuid):
    lock = UUIDFileLock(str(lock_file))
    lock.my_uuid = mock_uuid  # Use the mocked UUID

    # Acquire the lock
    lock.acquire()

    # Check if the lock file was created with the correct UUID
    with open(str(lock_file), 'r') as f:
        lock_content = f.read().strip()

    assert lock_content == mock_uuid


def test_release_lock(lock_file, mock_uuid):
    # Simulate the lock file existing with the correct UUID
    lock = UUIDFileLock(str(lock_file))
    lock.my_uuid = mock_uuid  # Use the mocked UUID

    # Create the file to simulate the lock being held
    with open(str(lock_file), 'w') as f:
        f.write(mock_uuid)

    # Release the lock
    lock.release()

    # Check if the lock file is removed
    assert not os.path.exists(str(lock_file))


def test_release_lock_when_locked_by_another(lock_file, mock_uuid):
    # Simulate a lock file with a different UUID
    other_uuid = str(uuid.uuid4())
    lock = UUIDFileLock(str(lock_file))
    lock.my_uuid = mock_uuid  # Use the mocked UUID

    # Create the file with a different UUID
    with open(str(lock_file), 'w') as f:
        f.write(other_uuid)

    # Release the lock (should not remove the lock file as the UUID is different)
    lock.release()

    # Ensure that the lock file still exists
    with open(str(lock_file), 'r') as f:
        lock_content = f.read().strip()

    assert lock_content == other_uuid


def test_context_manager(lock_file, mock_uuid):
    lock = UUIDFileLock(str(lock_file))
    lock.my_uuid = mock_uuid  # Use the mocked UUID

    # Use the context manager to acquire and release the lock
    with lock:
        # Check that the lock file was created with the correct UUID
        with open(str(lock_file), 'r') as f:
            lock_content = f.read().strip()

        assert lock_content == mock_uuid

    # Ensure that the lock file is removed after exiting the context
    assert not os.path.exists(str(lock_file))
