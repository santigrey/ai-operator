# True Anomaly — Company Research

**Researched:** 2026-03-12
**Source:** trueanomaly.space, web research, job postings
**HQ:** Centennial, CO (Denver metro)
**Other Offices:** Long Beach CA, Colorado Springs CO, Washington DC
**Founded:** August 2022
**Headcount:** ~200+ (43 open engineering roles as of March 2026)

---

## Mission

True Anomaly is the only defense technology company focused exclusively on space defense. They design and build spacecraft, software, and payloads for space superiority. Founded by former U.S. Space Force operators, the company exists to enable a secure, stable, and sustainable space environment for the US and its allies.

## Products

### Jackal — Autonomous Orbital Vehicle (AOV)
- Tactical fighter-interceptor spacecraft for contested space environments
- Multirole space superiority platform with modular architecture
- High-thrust, high-delta-v propulsion
- Multiple mission hardpoints for sensors and effectors
- Designed for high-rate manufacturability at scalable price point
- Three variants: LEO, GEO, and cislunar space operations
- Uses Redwire cameras for real-time tracking and sensor processing

### Mosaic — Autonomy Software Platform
- Full-stack ground-up software platform for space operations
- Transforms commander intent into autonomous spacecraft action
- Capabilities: test/training, mission planning, flight software, on-orbit ops, constellation management, space domain awareness, multi-domain battle management
- Cloud-based (GovCloud compliant) AND installable on classified/air-gapped systems
- Containerized microservices architecture — deploy only what you need
- Unified API integration across data sources and platforms
- Human-in-the-loop AI with real-time optimization
- Mission-aware algorithms trained on domain-relevant tactical data
- Runs the full OODA loop (Observe-Orient-Decide-Act) with AI acceleration

## Funding History

| Round | Date | Amount | Lead Investor |
|-------|------|--------|---------------|
| Series A | April 2023 | $17M | — |
| Series B | December 2023 | $100M | — |
| Series C | May 2025 | $260M (oversubscribed) | Accel |

Series C participants: Meritech Capital, Eclipse, Riot Ventures, Menlo Ventures, 645 Ventures, ACME Capital, Space VC, Champion Hill Ventures, Narya.

**Total raised: ~$377M+ in under 3 years.** Hypergrowth trajectory.

## Key Milestones & News

- **April 2024 — Mission X-1:** First two Jackal spacecraft deployed to LEO. Mosaic full-stack software fielded.
- **December 2024 — Mission X-2:** Successful deployment of 1x Jackal in LEO. Captured first orbital imagery.
- **February 2025:** Long Beach engineering & production facility opened for scale.
- **Q1 2026 — Mission X-3:** Upcoming launch and test flight with latest Jackal.
- **Q2 2026 — VICTUS HAZE:** End-to-end kill chain and rendezvous proximity operations (RPO) demonstration with Firefly Aerospace. This is a Tactically Responsive Space (TacRS) mission for the U.S. Space Force.
- **2026:** First independent Jackal missions to GEO and cislunar space.

## Engineering Tech Stack (from job postings)

**Languages:** C++ (C++17/C++20), Python, TypeScript/JavaScript
**Backend/Systems:** gRPC, REST, WebSockets, GraphQL, distributed systems
**Frontend:** React (advanced patterns), Three.js, React Three Fiber (3D visualization)
**Testing:** Google Test (C++), Vitest, React Testing Library, end-to-end frameworks
**Build/Tooling:** CMake, GCC, Clang, sanitizers, benchmarking
**Math/Science:** Eigen (linear algebra), orbital mechanics, astrodynamics
**Embedded:** Real-time embedded software for spacecraft hardware
**Infrastructure:** Containerized deployments, GovCloud, air-gapped capable
**Design:** Figma, Git-based collaborative workflows
**Security:** DoD Secret and TS/SCI clearance eligible roles

## Engineering Departments

Applied Algorithms, Flight Software, Mission Engineering, Mission Ops R&D, Mission Readiness, Product, Security Engineering, Software Engineering, Space Operations, Spacecraft Development, Technical Operations

## Leadership (Key Players)

- **Even Rogers** — CEO & Co-Founder. Former USAF space operations officer. Author of six foundational doctrine texts for U.S. military space ops. VMI + MA from UT Austin.
- **Kyle Zakrzewski** — Chief Engineer & Co-Founder. Former NASA GNC Engineer. MS Aerospace Engineering, UMN.
- **Sarah Walter** — COO. Former VP Engineering at York Space Systems, CTO at Sierra Space. 20 years aerospace/defense.
- **Steve Kitay** — SVP Space Defense. Former Senior Director at Microsoft. Former Deputy Assistant Secretary of Defense for Space Policy (Senior Executive Service).

## Interview Process

1. Talent Screen (recruiter)
2. Hiring Manager Screen (culture + role fit)
3. Technical Panel (collaborative structured assessment)
4. Focused 1:1s (each panelist covers unique aspects)
5. Founder Interview (values and mission alignment)
6. Offer

## Benefits

- 100% employer-sponsored healthcare
- Equity options
- 401k and Roth 401k
- Generous PTO
- Learning & development budget

---

## Why AI Platform Engineer Matters Here

True Anomaly's entire competitive advantage rests on the intersection of hardware (Jackal) and software intelligence (Mosaic). The AI Platform Engineer role is mission-critical for several reasons:

1. **Mosaic IS an AI platform.** It translates human intent into autonomous spacecraft action using ML-driven decision support, real-time optimization, and mission-aware algorithms. Someone needs to build and scale the infrastructure that trains, serves, and monitors these models.

2. **Autonomy at orbital speed.** Space combat operates on timescales where human reaction is too slow. The AI platform must deliver real-time inference for maneuver planning, threat assessment, and sensor fusion — all with extreme reliability constraints.

3. **Containerized, multi-environment deployment.** Mosaic runs on GovCloud AND air-gapped classified networks. The AI platform engineer would architect ML pipelines that work across both, handling model versioning, deployment, and monitoring in highly constrained environments.

4. **Scale inflection point.** With $260M in fresh capital, three Jackal variants, and VICTUS HAZE on the horizon, they're scaling from prototype to production. The AI infrastructure needs to scale with it — from single-satellite ops to constellation-level autonomy.

5. **Sensor fusion + space domain awareness.** Fusing data from space-based and ground-based sensors into actionable intelligence is a core ML/AI problem. Platform engineering here means building the data pipelines, feature stores, and inference engines that power real-time situational awareness.

---

## Sloan's Angle — Positioning Notes

**Strengths to emphasize:**
- Infrastructure + Kubernetes + containerization experience maps directly to their containerized microservices architecture
- Systems thinking from operations leadership translates to mission-critical reliability
- AI engineering portfolio demonstrates ability to build ML pipelines end-to-end
- Denver-local — no relocation friction
- Builder mindset aligns perfectly with their stated value: "Be a proactive, hands-on problem solver"

**Gaps to address:**
- Security clearance: If you don't have one, note willingness to obtain. The Staff and Senior roles may require eligibility.
- Aerospace domain knowledge: Frame transferable skills from complex systems operations
- C++ depth: If lighter here, emphasize Python ML stack + willingness to go deep on systems languages

**Differentiation:**
- Most AI platform candidates come from pure tech. Your operations leadership background (managing complex systems under pressure, leading teams) is rare in this candidate pool and directly relevant to defense tech culture.
- Former chef → director of nutrition parallels their value of grit and non-traditional paths.
