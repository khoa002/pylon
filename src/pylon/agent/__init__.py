"""Agent layer: tools and the model loop. Milestone 3, weeks 9 to 12.

⚠️ Write the loop directly against the model API. No orchestration framework
before Milestone 3 ships. See CLAUDE.md.

The model gets exactly two jobs: turn English into a structured query, and turn
the structured answer back into English with citations. It never decides what is
required. See ADR-001.
"""
