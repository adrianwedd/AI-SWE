import asyncio
import shlex
from typing import Sequence, Union, Dict

class AsyncRunner:
    """Run shell commands asynchronously."""

    async def run(self, command: Union[str, Sequence[str]]) -> Dict[str, Union[str, int]]:
        """Execute ``command`` asynchronously and capture output.

        Parameters
        ----------
        command:
            The command to execute. Can be a string or sequence of arguments.

        Returns
        -------
        dict
            Dictionary with ``stdout``, ``stderr`` and ``exit_code``.
        """
        if isinstance(command, str):
            args = shlex.split(command)
        else:
            args = list(command)

        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()

        return {
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "exit_code": proc.returncode,
        }
