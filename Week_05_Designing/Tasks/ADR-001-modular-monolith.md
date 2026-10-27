# ADR-001: Adopt a Modular Monolith Architecture

- **Status:** Approved
- **Date:** 2026-10-27
- **Decision owners:** RentYourExpert project team

## Context

RentYourExpert connects customers with workers who provide expert services. The
system must support three roles:

- Customers can register, log in, manage their profiles, search for workers,
  submit and delete requests, ask questions, and create, update, or delete
  reviews.
- Workers can register, log in, manage their profiles, view requests, accept
  or reject requests, and answer customer questions.
- Administrators can manage customers, workers, requests, questions, answers,
  and reviews.

The platform also requires worker search by skill and location, worker profile
pages, review display, and authenticated access with role-based authorization.
These capabilities share users, profiles, requests, and content, so they
require consistent business rules and transactional data updates.

The system is expected to start as a relatively small application. There is no
current requirement for independently deployable services, very high traffic,
multiple development teams, or geographically distributed operation.

## Decision

We will implement RentYourExpert as a **modular monolith**.

The application will be deployed as one backend system, but its source code
will be divided into explicit business modules with well-defined interfaces.
Modules must not access another module's internal implementation directly.
Cross-module interaction should use application services, domain events, or
other documented interfaces.

The initial modules are:

1. **Identity and Authorization**
   - Registration and login
   - Password and session/token handling
   - Customer, worker, and administrator roles
   - Role-based access control
2. **Customer Profiles**
   - Customer profile viewing and editing
   - Customer request history
3. **Worker Profiles and Catalogue**
   - Worker registration and profile management
   - Worker catalogue
   - Search by skill and location
   - Individual worker profile pages
4. **Service Requests**
   - Customer request creation and deletion
   - Worker request listing
   - Accepting and rejecting requests
   - Administrator request management
5. **Questions and Answers**
   - Customer questions for workers
   - Worker answers
   - Public display of a worker's questions and answers
   - Administrator moderation
6. **Reviews**
   - Customer review creation, editing, and deletion
   - Worker review display
   - Administrator moderation
7. **Administration**
   - Customer and worker management
   - Cross-module moderation and administrative workflows

The modules will use a shared relational database initially. Database tables,
repositories, and business rules remain owned by their respective modules even
when the physical database is shared. Authentication and authorization checks
must be enforced in the backend, not only in the user interface.

## High-level structure

```text
Web or mobile client
          |
          v
      REST API
          |
          v
  Application and domain modules
  +-----------------------------+
  | Identity and Authorization  |
  | Customer Profiles           |
  | Worker Catalogue            |
  | Service Requests            |
  | Questions and Answers       |
  | Reviews                     |
  | Administration              |
  +-----------------------------+
          |
          v
   Relational database
```

Each module follows the same internal layering where practical:

```text
API/controller -> application service -> domain rules -> repository
```

## Alternatives considered

### Layered backend with a separate frontend

This would provide a clear client/API boundary and is compatible with the
selected decision. It is not a competing deployment architecture for the
initial implementation; the modular monolith will expose a REST API and can
therefore use a separate web or mobile frontend.

### Microservices

Microservices would allow independent scaling and deployment of identity,
catalogue, requests, Q&A, and reviews. They would also introduce distributed
transactions, service-to-service communication, operational monitoring,
deployment complexity, and more difficult local testing. The current
requirements do not justify those costs.

### Serverless architecture

Serverless functions and managed services could reduce server administration
and scale automatically. However, the system's closely related workflows would
be split across functions and managed services, increasing debugging,
observability, and vendor lock-in concerns. This is not necessary for the
initial scale.

## Consequences

### Benefits

- One deployment and one operational environment are simple to develop,
  test, monitor, and release.
- Shared transactions are straightforward for requests, profiles, questions,
  answers, and reviews.
- Module boundaries keep the codebase organized and make business ownership
  explicit.
- Backend authorization can be applied consistently across all user roles.
- A relational database supports the system's related entities and
  administrative queries well.
- Modules can later be extracted into services if scale or team structure
  requires it.

### Costs and risks

- All modules initially scale and deploy together.
- A severe application failure can affect the complete platform.
- A shared database can encourage unintended coupling if ownership rules are
  not enforced.
- The codebase will require discipline to preserve module boundaries.
- Extracting a module later will require identifying and replacing shared
  database access.

## Architectural rules

1. Every endpoint must authenticate the caller when authentication is
   required and must enforce the caller's role and resource ownership.
2. Controllers must delegate business decisions to application or domain
   services rather than implementing them directly.
3. A module may use another module only through its public application
   interface or a documented event.
4. Direct access to another module's repositories and internal tables is
   prohibited.
5. Requests, reviews, questions, and answers must record their owning users
   and support authorization checks and moderation.
6. Schema changes must preserve referential integrity and be applied through
   versioned migrations.
7. Search should begin with database indexes for skills and location. A
   dedicated search engine may be introduced later if catalogue performance
   requires it.
8. Logging, validation, authorization failures, and moderation actions must be
   observable and must not fail silently.

## Data ownership

| Module | Primary data |
|---|---|
| Identity and Authorization | Accounts, credentials, roles, sessions or tokens |
| Customer Profiles | Customer profile information |
| Worker Catalogue | Worker profiles, skills, locations |
| Service Requests | Requests, request status, customer and worker references |
| Questions and Answers | Questions, answers, authors, moderation state |
| Reviews | Reviews, ratings, authors, worker references, moderation state |
| Administration | Administrative actions and audit records |

Foreign keys or stable identifiers may reference entities owned by another
module, but writes to another module's data must go through that module's
public interface.

## Migration and evolution strategy

The initial implementation will keep all modules in one deployable application
and one relational database. If a module later becomes a scaling or ownership
boundary, it can be extracted by:

1. Defining and versioning its public API and events.
2. Replacing direct database references with API or event-based integration.
3. Moving its data to a service-owned database.
4. Deploying and scaling the extracted service independently.

Potential future extraction candidates are catalogue search, authentication,
notifications, and reviews, depending on measured usage and operational
needs. No extraction should occur without evidence from performance,
availability, or organizational requirements.

## Validation criteria

The decision is considered successfully implemented when:

- Customers, workers, and administrators can access only the operations
  allowed by their roles.
- Worker search supports both skill and location criteria.
- Requests can be created, listed, deleted, accepted, rejected, and
  administratively managed.
- Questions and answers are visible on worker pages and can be moderated.
- Reviews can be created, updated, deleted, displayed, and moderated.
- Each module can be unit tested without depending on another module's
  internal implementation.
- Integration tests verify authentication, authorization, relationships, and
  transaction boundaries.
- Database migrations can create the schema from an empty database.

## Revisit triggers

Reconsider this decision if one or more of the following occur:

- A module needs independent scaling or release frequency.
- The application requires multiple independently owned development teams.
- Availability requirements require isolation between major capabilities.
- Catalogue search or another workload cannot meet performance targets within
  the monolith.
- The shared database becomes a measurable bottleneck or a source of
  unacceptable coupling.
