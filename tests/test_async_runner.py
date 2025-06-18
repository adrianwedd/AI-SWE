import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import asyncio
import unittest

from core.async_runner import AsyncRunner


class TestAsyncRunner(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.runner = AsyncRunner()

    async def test_run_echo(self):
        result = await self.runner.run(["echo", "hello"])
        self.assertEqual(result["stdout"].strip(), "hello")
        self.assertEqual(result["stderr"], "")
        self.assertEqual(result["exit_code"], 0)

    async def test_run_failure(self):
        result = await self.runner.run(["sh", "-c", "exit 1"])
        self.assertNotEqual(result["exit_code"], 0)

    async def test_concurrent_runs(self):
        cmd = ["python3", "-c", "import time; time.sleep(0.5)"]
        start = asyncio.get_event_loop().time()
        await asyncio.gather(self.runner.run(cmd), self.runner.run(cmd))
        duration = asyncio.get_event_loop().time() - start
        self.assertLess(duration, 1.0)


if __name__ == "__main__":
    unittest.main()
