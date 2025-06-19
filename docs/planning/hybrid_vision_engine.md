# Hybrid Vision Engine Plan

This document outlines a phased approach to implement a hybrid Vision Engine that combines a transparent Weighted Shortest Job First (WSJF) heuristic with a reinforcement-learning (RL) refinement layer.

## Research Background
The approach follows the strategy described in the research paper on Epic Prioritization. Key points include:

1. Establish a **WSJF heuristic baseline** that provides a clear, defensible ranking of epics.
2. Introduce an **RL agent as a refinement layer**, initially running in shadow mode to compare its suggestions against the heuristic output.
3. Adopt a **phased rollout** where the RL agent gains authority only after demonstrating consistent improvements over the baseline.

Reference: lines 233–260 of `docs/research/Epic Prioritization_ RL vs Heuristics_.md`.

## Proposed Tasks

:::task-stub{title="Document hybrid Vision Engine design"}
- Summarize WSJF scoring inputs and RL refinement logic.
- Detail the shadow-mode deployment strategy.
:::

:::task-stub{title="Extend WSJF scoring utilities"}
- Provide CLI hooks for ranking epics using WSJF.
- Add unit tests covering typical scoring scenarios.
:::

:::task-stub{title="Implement RL training pipeline"}
- Collect data from WSJF runs and observability metrics.
- Train a lightweight RL agent (e.g., SITP) offline.
:::

:::task-stub{title="Run RL agent in shadow mode"}
- Integrate the trained agent with the Vision Engine.
- Log suggested rankings without altering live decisions.
:::

:::task-stub{title="Gradually enable RL authority"}
- Configure a rollout percentage that controls how much the RL agent can adjust rankings.
- Monitor performance metrics to decide when to increase authority.
:::
