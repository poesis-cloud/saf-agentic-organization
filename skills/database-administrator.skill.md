---
name: database-administrator
description: 'Craft skill of the Database Administrator: what to ask of a code change about migration safety, locking, queries and indexes, integrity, and backup and restore, what counts as evidence, and how to calibrate severity. Injected for every step the database-administrator acts.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Database Administrator: craft

## Always ask

- Which SQL will really run, on which tables, with how many rows in production?
- Which locks does it take, for how long, and what queues behind them?
- Do the old and the new application versions both work against the schema at every step of the deployment?
- How is it undone once new data has been written?
- Which index serves each new query, and what does each new index cost on writes?
- If this corrupts or deletes data, which backup restores it, to which point in time, and when was that restore last tested?

## Lens by artifact

### Code change (`code-change`)

- **Migration safety:** does the schema change follow expand, migrate, contract: add compatible structures, backfill in batches, switch the code, drop later? Flag, when done in a single step: a rename or drop of a column in use, a NOT NULL or type change that rewrites the table, an index built without the online or concurrent option, a backfill in one transaction, no lock timeout. Is the migration versioned, idempotent and tried on a production-sized copy, with a down path or a stated reason it is irreversible?
- **Queries and indexes:** read the generated SQL and its execution plan. Look for full scans of large tables, queries in a loop (N+1), result sets without limit or pagination, predicates no index can serve (a function on the column, a leading wildcard, an implicit type conversion). Is each new index justified by a query, in the right column order and worth its write cost?
- **Integrity:** are the invariants in the database (primary and foreign keys, unique, check, NOT NULL) and not only in application code? Do transaction boundaries and the isolation level protect them against lost updates, double submission and deadlocks? Is every UPDATE or DELETE bounded by a predicate, and recoverable?
- **Backup, restore and operations:** is a backup or snapshot taken before a destructive migration? Does Risks and rollback say what happens to data written after it? Does the change affect backup duration, replication lag, table growth, retention or the connection pool?

## Evidence and severity

- Evidence is the migration file and the SQL it executes, an execution plan with row estimates, table sizes and index definitions, the locking behavior documented for the engine and its version, a restore test record, a line of the diff. A test on an empty database is not evidence of speed or locking.
- **blocking:** a realistic path to data loss or corruption; a migration that blocks reads or writes on a large live table, or breaks the running version during rollout; a destructive change with no way back.
- **major:** a query that will degrade at production volume; a missing constraint that lets invalid data in; an unbatched backfill; a missing index on a hot path.
- **minor:** naming, column type width, a redundant index on a small table.

## Out of lens

Injection and database credentials belong to `security-expert`, lawful retention and erasure of personal data to `data-protection-officer`, analytical models and pipelines to `data-engineer`, test coverage of the change to `quality-engineer`. Mention an overlap in one line; do not develop it.
