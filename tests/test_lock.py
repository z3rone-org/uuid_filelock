from datetime import datetime
import os
from uuid_filelock import UUIDFileLock, LockTimeoutException


def test_two_locks(tmpdir):
    lockfile = os.path.join(tmpdir, '.lock')
    lock1 = UUIDFileLock(lockfile, prefix='lock1-')
    lock2 = UUIDFileLock(lockfile, prefix='lock2-')

    assert not lock1.check_lock()
    assert not lock2.check_lock()

    # Acquire the lock
    lock1.acquire()

    with open(lock1.lock_file) as f:
        assert f.readline().startswith('lock1-')

    assert lock1.check_lock()
    assert not lock2.check_lock()

    lock1.release()
    lock2.acquire()

    assert not lock1.check_lock()
    assert lock2.check_lock()

    lock2.release()

    assert not lock1.check_lock()
    assert not lock2.check_lock()


def test_timeout(tmpdir):
    lockfile = os.path.join(tmpdir, '.lock')
    lock1 = UUIDFileLock(lockfile)
    lock2 = UUIDFileLock(lockfile, timeout_interval=3)

    lock1.acquire()
    assert lock1.check_lock()

    try:
        lock2.acquire()
        assert False
    except LockTimeoutException:
        assert not lock2.check_lock()

    lock1.release()
    assert not lock1.check_lock()
    assert not lock2.check_lock()


def test_default_params(tmpdir):
    lockfile = os.path.join(tmpdir, '.lock')
    UUIDFileLock.default_verification_delay = 5
    start_time = datetime.now()
    with UUIDFileLock(str(lockfile)):
        end_time = datetime.now()
    time_diff = (end_time - start_time).total_seconds()
    assert time_diff > 5
    assert time_diff < 6

    UUIDFileLock.default_verification_delay = 2
    start_time = datetime.now()
    with UUIDFileLock(str(lockfile)):
        end_time = datetime.now()
    time_diff = (end_time - start_time).total_seconds()
    assert time_diff > 2
    assert time_diff < 3


def test_context_manager(tmpdir):
    lockfile = os.path.join(tmpdir, '.lock')
    lock = UUIDFileLock(str(lockfile))

    # Use the context manager to acquire and release the lock
    with lock:
        # Check that the lock file was created with the correct UUID
        with open(str(lockfile), 'r') as f:
            lock_content = f.read().strip()

        assert lock_content == lock.lock_id

    # Ensure that the lock file is removed after exiting the context
    assert not os.path.exists(str(lockfile))
