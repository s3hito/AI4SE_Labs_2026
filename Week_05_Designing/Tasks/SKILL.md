---
name: propose-architectures-and-adr
description: "Propose at least three software architectures from a system description and create a well-structured Architecture Decision Record (ADR) for the selected architecture. Use for architecture analysis, system-design alternatives, modular monolith decisions, and ADR generation."
argument-hint: "Path to the system-description file and, optionally, the preferred architecture or ADR status"
user-invocable: true
---

# Propose Architectures and Create an ADR

## Purpose

Turn a requirements or system-description document into:

1. A concise requirements summary.
2. At least three materially different architecture proposals.
3. A comparison and recommendation.
4. A complete Architecture Decision Record for the selected architecture.

Use this workflow for system-design assignments, architecture discussions, and
documented technology decisions.

## Inputs

The user should provide:

- The path to the system-description or requirements file.
- The output directory or file path for the ADR, when relevant.
- The selected architecture and ADR status, if already decided.

If the output location is not specified, ask before creating a file. If the
user explicitly specifies a location, use it. Do not read unrelated files when
the user limits the source material.

## Procedure

### 1. Read and scope the requirements

Read the supplied system-description file and extract:

- User roles and permissions.
- Core business capabilities.
- Main entities and relationships.
- Functional workflows.
- Quality attributes, if stated.
- Constraints, assumptions, and missing information.

Do not invent requirements. Clearly label reasonable assumptions and identify
important unanswered questions.

### 2. Propose architecture alternatives

Provide at least three genuinely different alternatives. Select alternatives
appropriate to the system rather than listing superficial technology changes.
Common candidates include:

- Modular monolith.
- Layered application with a separate frontend and backend API.
- Microservices.
- Serverless or managed-cloud architecture.
- Event-driven architecture, when asynchronous workflows are central.

For each alternative, describe:

- Component or module structure.
- Data storage and ownership.
- Communication patterns.
- Authentication and authorization placement.
- How the key requirements are implemented.
- Benefits.
- Costs, risks, and operational implications.
- Conditions under which it is the best fit.

Include a simple text or Mermaid diagram when it clarifies the architecture.

### 3. Compare and recommend

Compare the alternatives using criteria relevant to the requirements, such as:

- Implementation complexity.
- Operational complexity.
- Scalability.
- Availability and fault isolation.
- Consistency and transaction handling.
- Testability.
- Deployment simplicity.
- Cost.
- Team and organizational fit.
- Ability to evolve.

Use a comparison table where practical. Recommend one architecture and explain
why it fits the current requirements and constraints. State the trade-offs and
the conditions that would justify revisiting the decision.

If the user has already selected an architecture, preserve that choice and use
the comparison only to provide context.

### 4. Create the ADR

Create a Markdown ADR with a descriptive filename such as
`ADR-001-modular-monolith.md`. Unless the user requests another format, include
the following sections:

```markdown
# ADR-NNN: <Decision title>

- **Status:** <Proposed | Approved | Accepted | Superseded | Rejected>
- **Date:** <YYYY-MM-DD>
- **Decision owners:** <team or role>

## Context
## Decision
## High-level structure
## Alternatives considered
## Consequences
## Architectural rules
## Data ownership
## Migration and evolution strategy
## Validation criteria
## Revisit triggers
```

The ADR must:

- Mark the status exactly as requested by the user.
- Explain the problem and relevant requirements, not just the solution.
- Define module or service boundaries.
- Describe authentication and authorization responsibilities.
- Describe data ownership and important consistency boundaries.
- Include a visual representation when useful.
- Document rejected alternatives and why they were not selected.
- Separate benefits from costs and risks.
- Define measurable validation criteria.
- Define concrete triggers for revisiting the decision.

For a modular monolith, explicitly document that the application is deployed as
one unit while its code is divided into business modules with public
interfaces. Explain how direct access to another module's internals is
restricted and how the design could evolve into separately deployed services.

### 5. Verify the result

After creating the ADR:

- Confirm the file exists at the requested location.
- Verify the frontmatter or metadata, if used, is syntactically valid.
- Confirm the status is correct.
- Check that all major roles and capabilities from the system description are
  addressed.
- Check that at least three alternatives were considered.
- Check that the selected architecture, consequences, and revisit triggers are
  consistent.
- Report the created file using a Markdown link.

Do not claim that an architecture has been implemented merely because the ADR
was created.

## Quality checklist

Before finishing, confirm:

- The proposals differ in deployment and responsibility boundaries.
- The recommendation is tied to stated requirements.
- Security responsibilities are explicit.
- Data ownership is not ambiguous.
- Failure and scaling implications are acknowledged.
- The ADR is informative without containing unrelated implementation details.
- The document can be understood by someone who did not participate in the
  architecture discussion.
