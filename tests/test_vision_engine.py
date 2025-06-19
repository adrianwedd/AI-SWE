import unittest
from core.task import Task
from vision.vision_engine import VisionEngine, RLAgent


class TestVisionEngine(unittest.TestCase):
    def _task(self, id, ubv, tc, rr, size):
        t = Task(
            id=id,
            description="",
            component="vision",
            dependencies=[],
            priority=1,
            status="pending",
        )
        t.user_business_value = ubv
        t.time_criticality = tc
        t.risk_reduction = rr
        t.job_size = size
        return t

    def test_wsjf_sorting(self):
        t1 = self._task(1, 10, 2, 1, 5)  # score 2.6
        t2 = self._task(2, 5, 1, 1, 2)   # score 3.5
        t3 = self._task(3, 8, 0, 0, 4)   # score 2.0
        ve = VisionEngine()
        ordered = ve.prioritize([t1, t2, t3])
        self.assertEqual([t.id for t in ordered], [2, 1, 3])

    def test_rl_shadow_mode_records_history(self):
        agent = RLAgent()
        ve = VisionEngine(rl_agent=agent, shadow_mode=True)
        t1 = self._task(1, 1, 1, 1, 1)
        t2 = self._task(2, 1, 1, 1, 2)
        ve.prioritize([t1, t2])
        self.assertEqual(len(agent.history), 1)
        self.assertEqual(agent.history[0]["baseline"], [1, 2])
