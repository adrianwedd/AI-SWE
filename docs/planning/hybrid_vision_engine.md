# Hybrid Vision Engine Plan

This document outlines a phased approach to implement a hybrid Vision Engine that combines a transparent Weighted Shortest Job First (WSJF) heuristic with a reinforcement-learning (RL) refinement layer.

## Research Background
The approach follows the strategy described in the research paper on Epic Prioritization. Key points include:

1. Establish a **WSJF heuristic baseline** that provides a clear, defensible ranking of epics.
2. Introduce an **RL agent as a refinement layer**, initially running in shadow mode to compare its suggestions against the heuristic output.
3. Adopt a **phased rollout** where the RL agent gains authority only after demonstrating consistent improvements over the baseline.

Reference: lines 233–260 of `docs/research/Epic Prioritization_ RL vs Heuristics_.md`.

## Design Overview

The hybrid Vision Engine has two layers:

1. **WSJF baseline** – each epic is scored using the classic formula
   `(User/Business Value + Time Criticality + RR\&OE) / Job Size`.
   This provides a transparent ranking that can be justified to
   stakeholders.
2. **RL refinement** – a lightweight agent (initially SITP-based)
   learns to slightly adjust the WSJF order. Its action space is a
   re‑ranking of the top candidates rather than unrestricted backlog
   manipulation. The reward function measures improvement over the
   heuristic baseline to keep behaviour grounded and explainable.

## Rollout Strategy

1. **Heuristic only** – deploy WSJF scoring and record the resulting
   decisions along with observability metrics.
2. **Shadow-mode RL** – train the agent offline using the collected
   data, then run it in parallel while logging its suggested rankings
   without affecting live prioritization.
3. **Gradual authority** – once the agent shows consistent improvements,
   allow it to modify a small portion of the WSJF output. Increase this
   percentage only when metrics continue to trend positively.

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
