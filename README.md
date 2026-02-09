Elysian Truth Engine: Scaling Luxury with Certainty
Forward Deployed Engineer Take-Home Test Candidate: Ben Hughes

🎯 Solution Overview
The Elysian Truth Engine is an agentic orchestration model designed to solve the "Trust-Velocity Paradox" in luxury marketing. It ensures that AI-driven content generation is tethered to a programmatic Source of Truth to prevent data hallucination regarding inventory, pricing, and legal compliance.

📂 Project Deliverables

This repository contains the functional components and configurations for the Elysian solution:

1. Technical Implementation (/api)

    * Custom Tool Source Code: Logic for fetching authoritative enterprise data from the inventory API.
    * Discovery Endpoint: Automatically generated manifest for Opal tool registration.

2. Opal Assets (/opal-assets)

    * Instructions: The Elysian Brand Director system prompts and role definitions.

    * Specialized Agents:

        * Campaign Architect: Responsible for creative synthesis and trend analysis.
        * Compliance Sentinel: A "Zero-Trust" auditor for legal and data verification.


    * Workflow: The orchestrated "Relay Race" that connects agents to the custom tool registry.

3. Documentation

BenHughes_OpalAgentSolution.pdf: The comprehensive 2-page brief covering problem identification, design decisions, and self-reflection.

🔧 Opal Registry Configuration
To register the custom tool in the Opal instance:

URL: https://fdeth-tool.vercel.app/discovery

Name: Elysian Truth Engine

