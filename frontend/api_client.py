import httpx
import asyncio
from typing import Any, Optional
from PySide6.QtCore import QObject, Signal, QThread, QRunnable, Slot


class APIWorker(QRunnable):
    """Worker to run async API calls in a thread pool"""
    
    class Signals(QObject):
        finished = Signal(dict)
        error = Signal(str)
    
    def __init__(self, sentence: str, base_url: str = "http://localhost:8000"):
        super().__init__()
        self.sentence = sentence
        self.base_url = base_url
        self.signals = APIWorker.Signals()
    
    @Slot()
    def run(self):
        """Execute the API call"""
        try:
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def do_request():
                async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as client:
                    response = await client.post(
                        "/api/v1/check_spelling",
                        json={"sentence": self.sentence}
                    )
                    response.raise_for_status()
                    return response.json()
            
            result = loop.run_until_complete(do_request())
            print(result)
            loop.close()
            self.signals.finished.emit(result)
        except httpx.ConnectError:
            self.signals.error.emit("Could not connect to the backend server. Make sure it's running on http://localhost:8000")
        except httpx.HTTPStatusError as e:
            self.signals.error.emit(f"Server returned status: {e.response.status_code}")
        except Exception as e:
            self.signals.error.emit(str(e))
