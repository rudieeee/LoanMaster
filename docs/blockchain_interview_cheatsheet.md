# LoanMaster Blockchain – Interview Cheat Sheet

Use this as crisp talking points for a hackathon interview. Tailor depth based on the interviewer.

---

## What & Why
- Purpose: Provide a tamper-evident, append-only audit trail for loan lifecycle events (application, approval/rejection, payments).
- Why blockchain vs plain DB logs: Hash-chained blocks + proof-of-work make retroactive edits evident; `is_valid` can detect tampering; great for demoing compliance/audit guarantees.
- Model: Permissioned, single-node demo ledger (no P2P network) that showcases core primitives: blocks, PoW mining, validation, and an explorer UI.

## How It Works (Concept → Code)
- Data model: `Block(index, timestamp, data, previous_hash, nonce, hash)`; JSON payload holds a batch of transactions.
- Hashing: SHA-256 over a stable JSON (sorted keys) string of block fields → `hash`.
- Proof of Work: Increment `nonce` until `hash` has a `difficulty` leading zeros (difficulty=2 in demo) → makes rewriting history expensive.
- Chaining: Each block stores `previous_hash`; changes cascade forward, breaking validation.
- Validation: `is_valid()` iterates chain verifying (1) stored hash matches recomputed hash, (2) previous_hash linkage, (3) PoW prefix.
- Files to cite: backend/blockchain.py (all core logic), backend/main.py (REST APIs), frontend/blockchain.html (explorer UI).

## Lifecycle & Where Events Are Written
- Application: Recorded when user finalizes amount/tenure via `MasterAgent` → `loan_blockchain.add_loan_application(...)`.
- Approval/Rejection: After underwriting, calls `add_loan_approval(...)` with `approved=True/False` and reason.
- Payment: Exposed via `/api/blockchain/payment` to record installments or other payments.
- Viewing: Explorer fetches `/api/blockchain/stats` and `/api/blockchain/chain` for live rendering.

## API Endpoints (FastAPI)
- GET `/api/blockchain/stats`: blocks, tx counts, difficulty, validity flag.
- GET `/api/blockchain/chain`: full chain.
- GET `/api/blockchain/block/{index}`: single block.
- GET `/api/blockchain/validate`: boolean validity.
- GET `/api/blockchain/customer/{id}`: txs for a customer.
- POST `/api/blockchain/loan/application|approval|payment`: append events.

## Data Examples (Transaction Types)
- `loan_application`: `{ customer_id, loan_amount, loan_purpose, status }`
- `loan_approval`: `{ customer_id, loan_id, approved, reason }`
- `payment`: `{ customer_id, loan_id, amount, payment_type }`

## Demo Narrative (60 seconds)
1) Start app, open Explorer. You’ll see a genesis block and validity ✓.
2) Run a chat flow to trigger application and an approval → new blocks appear.
3) Show that each block references the previous hash and that `Validate` returns ✓.
4) Explain that tampering any block field would break hashes and flip validity ✗.

## Security & Integrity Notes
- Tamper-evidence: PoW + chained hashes; `validate` detects edits.
- Centralized writer: This is a permissioned, single-node demo; no consensus network. Suitable for audit trace in a prototype.
- PII minimization: Store only IDs and high-level fields on-chain; keep sensitive details off-chain.
- Replay/double-spend: Not a currency; events are idempotent entries. Business rules handle duplicates (future improvement: tx IDs/signatures).

## Limits & Trade-offs (Be candid)
- No P2P consensus, no validators, no Merkle roots, no signatures.
- In-memory chain; persistence can be added (e.g., file/DB) to survive restarts.
- Fixed difficulty=2 for UX; dynamic difficulty or alternative sybil resistance not implemented.
- Throughput: Single-threaded PoW; acceptable for demo scale, not production.

## Sensible Improvements (If asked “what next?”)
- Persistence: Write chain to disk with periodic snapshots.
- Cryptography: Sign transactions (per service key), verify in validation.
- Merkle trees: Summarize txs with Merkle root per block.
- Networking: Promote to permissioned BFT (Raft/Tendermint/HotStuff) cluster.
- Anchoring: Periodically anchor block hashes to a public chain for external attestations.
- Privacy: Encrypt sensitive fields; field-level hashing; data retention policies.
- Ops: Metrics, alerts on validity failure; admin tooling to diff and locate tamper points.

## Performance & Complexity Talking Points
- Mining cost: Expected attempts grow exponentially with difficulty; we keep difficulty low for demo responsiveness.
- Validation: O(n) over blocks; each hash is O(1) per block size; tx lookup can be indexed by customer.

## Compare vs Alternatives
- Simple audit log: Easier, but easier to tamper unless protected; blockchain provides verifiable linkage and public validation function.
- Production ledgers: Hyperledger Fabric, Quorum, or simply append-only logs (AWS QLDB) may fit better for enterprise—this prototype illustrates the core immutability concept with minimal dependencies.

## Quick Commands (optional)
- Start backend:
  - `python backend/main.py` (or `uvicorn backend.main:app --reload`)
- Open explorer: http://localhost:8000/frontend/blockchain.html
- Validate chain:
  - `curl http://localhost:8000/api/blockchain/validate`

## One-liners to Keep Handy
- "We use a lightweight, PoW-backed hash chain to make our loan events tamper-evident and independently verifiable."
- "Each block’s hash commits to its data and the previous hash; any edit breaks the chain and fails validation."
- "This is a permissioned demo ledger—great for audit trails; in production we’d add signatures, persistence, and a consensus layer."
