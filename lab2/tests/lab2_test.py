import pytest

from lab2.lab2 import *

@pytest.mark.asyncio
async def test_log_message():
    import shutil
    
    LOG_FOLDER = Path(__file__).parent / "logs"
    
    if LOG_FOLDER.exists():
        shutil.rmtree(LOG_FOLDER)
        
    LOG_FOLDER.mkdir(parents=True, exist_ok=True)
    
    await log_message(LOG_FOLDER / "logTest.txt", "First log entry")
    
    assert (LOG_FOLDER / "logTest.txt").exists(), "ERR: logTest.txt does not exist!"

@pytest.mark.asyncio
async def test_read_logs():
    TEST_LOG_FILE = Path(__file__).parent / "sample_data/logTest.txt"
    
    assert TEST_LOG_FILE.exists(), "ERR: Test log file does not exist"
    
    numOccurrences = await read_logs(TEST_LOG_FILE, "ERROR")
    
    assert numOccurrences == 2, "ERR: Incorrect number of occurrences returned!"