#  %%
import aiofiles
import asyncio
from pathlib import Path
from datetime import datetime

async def read_logs(logFilePath:Path, keyword:str) -> int:
    """
    Returns the number of occurrences of `keyword` in a logfile

    Args:
        logFilePath (Path): Path to logfile
        keyword (str): Keyword to get the number of occurrences of.

    Returns:
        int: number of occurrences
    """
    async with aiofiles.open(logFilePath, mode="r") as logFile:
        content = await logFile.read()
        
        await asyncio.sleep(0.3) # Artificial delay
        
        return content.count(keyword)
            
# Stores locks for files (Key: fileName, Value: asyncio.Lock())
file_locks = {}
async def log_message(logFilePath:Path, message:str):
    """
    Asynchronously logs a message to a logfile

    Args:
        logFilePath (Path): Path to logfile to log messages to
        message (str): Message to log to the logfile
    """
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    if logFilePath not in file_locks:
        file_locks[logFilePath] = asyncio.Lock()
        
    async with file_locks[logFilePath]:
        print(f"Lock acquired: {message}")
        
        async with aiofiles.open(logFilePath, mode="a") as logFile:
            await logFile.write(log_entry)
            await asyncio.sleep(0.3) # Artificial delay
            
        print(f"Lock released: {message}")

async def main():
    import random
    LOG_FOLDER = Path(__file__).parent / "logs"
    LOG_FOLDER.mkdir(parents=True, exist_ok=True)
    
    # tasks = []
    
    # tasks.append(asyncio.create_task(log_message(LOG_FOLDER / "logTest.txt", "First log entry")))
    # print("Continued executions...")
    
    # await asyncio.sleep(2) # Artificial delay
    
    # tasks.append(asyncio.create_task(log_message(LOG_FOLDER / "logTest1.txt", "2ND log entry")))
    # print("Continued executions...")
    
    log_messages = [
        "INFO: Operation completed successfully.",
        "DEBUG: Variable value at step 5 is 42.",
        "WARNING: Disk space is running low.",
        "ERROR: Failed to connect to the database.",
        "INFO: User login successful.",
        "ERROR: Timeout occurred during data retrieval.",
    ]
    
    log_files = [f"log{i}.txt" for i in range(1, 6)]
    
    tasks = []
    
    # Writing logs concurrently
    print("Writing logs to files...")
    for _ in range(100):
        for logFile in log_files:
            logMessageIndex = random.randint(0, len(log_files) - 1)
            tasks.append(asyncio.create_task(log_message(LOG_FOLDER / logFile, log_messages[logMessageIndex])))
            
    print("================================= TASKS CREATED =================================")
    
    await asyncio.gather(*tasks)
    
    # Reading logs concurrently
    KEYWORD = "ERROR"
    
    print("\nReading logs and counting occurrences...")
    counts = await asyncio.gather(*(read_logs(LOG_FOLDER / file, KEYWORD) for file in log_files))
    total_logs = sum(counts)
    print(f"Total '{KEYWORD}' occurrences across all logs: {total_logs}")
    
if __name__ == "__main__":
    asyncio.run(main())