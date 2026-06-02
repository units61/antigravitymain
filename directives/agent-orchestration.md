# Directive: Pipeline Orchestration & Session Rules

## 1. Objective
This directive governs the orchestrator engine (`pipeline_runner.py`). It specifies how the multi-agent design pipeline is initiated, how sessions are generated and saved, how errors are caught, how fallbacks are loaded, and how the Critic Agent revision loop is executed.

---

## 2. Session Lifecycle & Storage
1. **Session Initialization**:
   - Each run gets a unique `session_id` (a UUID or a timestamp-hash combo).
   - A dedicated temporary directory is created at `.tmp/pipeline/{session_id}/`.
2. **Intermediate Logging**:
   - Every completed agent step must write its final JSON output to:
     `.tmp/pipeline/{session_id}/step_{step_number}_{agent_name}.json`
3. **Session Master Log**:
   - A final aggregated document is created at:
     `.tmp/pipeline/{session_id}/experience_blueprint.json`
   - This file compiles all individual agent steps, metadata, warnings, and Critic score cards.

---

## 3. Critic Revision Logic
If the **Critic Agent** evaluates the completed plan with an `overall_score < 80`:
1. Increments `revision_loop_count`. If `revision_loop_count >= 3`, halt revision, fallback to the latest blueprint, and issue a warning log.
2. If `revision_loop_count < 3`:
   - Re-execute the **Art Director** (`art_director.py`), passing the Critic's `failures` and `revised_parameters.art_direction` as feedback prompts.
   - Re-execute the **UX Architect** (`ux_architect.py`), passing the Critic's `failures` and `revised_parameters.ux_architecture` as feedback prompts.
   - Re-run all downstream agents (Motion Director, Component Mapper) to update properties based on the revised layout/visuals.
   - Re-run the **Critic Agent** to evaluate the new blueprint.

---

## 4. Fault Tolerance & Fail-Safes
If an API call to OpenRouter fails (due to rate limits, network timeouts, or malformed JSON responses):
1. **Retry twice** with exponential backoff (1s, 2s).
2. If it still fails, load a pre-configured, deterministic template based on the **Design DNA** of the prompt:
   - *Calm Template*: Soft gray theme, Satoshi font, generous airy layouts.
   - *Luxury Template*: Matte black and gold theme, Playfair Display font, asymmetric low-density layouts.
   - *Cyberpunk/Rebel Template*: Heavy neon-bordered layout, Space Grotesk font, high-density grids.
   - *Default Fallback*: Corporate blue theme, Inter font, standard medium-density grid sections.
3. Add a warning entry to `metadata.applied_warnings` documenting the fallback execution.
