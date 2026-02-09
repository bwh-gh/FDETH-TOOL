# Elysian Truth Engine: Scaling Luxury with Certainty
**Forward Deployed Engineer Take-Home Test** | **Candidate:** Ben Hughes

## 🎯 Solution Overview
The **Elysian Truth Engine** is an agentic orchestration model designed to solve the "Trust-Velocity Paradox" in luxury marketing. It ensures that AI-driven content generation is tethered to a programmatic **Source of Truth** to prevent data hallucination regarding inventory, pricing, and legal compliance.

## 📂 Project Deliverables
This repository contains the functional components and configurations for the Elysian solution:

### 1. Technical Implementation
* **[Custom Tool Source Code](./api)**: Logic for fetching authoritative enterprise data from the inventory API.
* **Discovery Endpoint**: Automated manifest for Opal tool registration via the `@optimizely-opal/opal-tools-sdk`.

### 2. Opal Assets
* **[Instructions](./opal-assets/Instructions)**: The **Elysian Brand Director** system prompts and role definitions.
* **[Specialized Agents](./opal-assets/Specialized-Agents)**: Includes the **Campaign Architect** for creative synthesis and the **Compliance Sentinel** for "Zero-Trust" auditing.
* **[Workflow](./opal-assets/Workflow)**: The orchestrated "Relay Race" that connects agents to the custom tool registry.

### 3. Documentation
* **[Download/View Brief Write-Up](./BenHughes_OpalAgentSolution.pdf)**: The comprehensive 2-page brief covering problem identification, design decisions, and self-reflection.

## 🔧 Opal Registry Configuration
To register the custom tool in the Opal instance:
* **URL**: https://fdeth-tool.vercel.app/discovery
* **Name**: Elysian Truth Engine
* **Authentication**: Configured via **OptiID** for secure enterprise access

---
*Note: The agents are live in the provided Opal instance.*