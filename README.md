# LLMStrike — LLM Prompt-Injection & Jailbreak Test Harness

A multi-provider red-teaming harness that fires adversarial attack packs at LLMs,
auto-judges the responses, and generates a pentest-style security report.
Built to measure how real models hold up against OWASP LLM01 (Prompt Injection).

## Headline findings (6 models, ~100 attack executions)

- **Leetspeak obfuscation bypassed 100% of models tested** (8/8 successful injections)
- Base64-encoded instructions: 80% bypass rate
- Direct injection is nearly dead: ~96% of front-door attacks were refused
- Multiple models *attempted* to follow encoded malicious instructions but failed
  the decoding itself — capability, not alignment, was the limiting control
- Verdicts are stochastic: identical attacks produced different outcomes across
  runs, so LLMStrike treats re-runs as trials and reports rates, not single results

![leaderboard](docs/screenshot.png)

## How it works

```
attacks/*.yaml ──&gt; runner ──&gt; target (Gemini / Groq / NVIDIA NIM)
                     │
                     v
                   judge ──&gt; verdict + severity
                     │
                     v
              SQLite (raw responses = evidence)
                     │
                     v
              report.py ──&gt; reports/report.html
```

- **Attack packs**: YAML, each entry declares a `success_marker` canary
- **Judge**: canary matching + refusal-pattern vocabulary, verdicts:
  compromised / partial / refused / unclear / error
- **rejudge.py**: re-scores all stored responses offline when the judge improves —
  verdicts are derived data, responses are evidence
- **run_all.py**: batch sweeps across providers/models

## Usage

```bash
pip install -r requirements.txt
# .env needs GEMINI_API_KEY / GROQ_API_KEY / NVIDIA_API_KEY (all free tiers)

python main.py --pack direct_injection --provider groq --delay 2
python run_all.py            # full multi-model sweep
python main.py --report      # regenerate reports/report.html
python rejudge.py            # re-score after judge improvements
```

## Roadmap

- [ ] Fuzzy canary matching (near-miss decodes like `PANED` currently read as unclear)
- [ ] Guardrail evaluation: run packs through llama-prompt-guard / nemoguard first
- [ ] Indirect injection pack (payloads hidden in documents the model processes)
- [ ] PDF export

## Ethics

All testing targets public demo APIs of models, using the author's own free-tier
keys. No production systems, no real user data. Built for defensive research —
understanding injection techniques is prerequisite to defending against them.