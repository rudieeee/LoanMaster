# LoanMaster – AI-Powered Revenue Growth from Existing Customers

Version: Oct 2025

---

## 1) Problem Statement You Wish to Address — and Why

NBFCs struggle to grow revenue from existing customers despite owning rich first‑party data. The current journey for selling personal loans is fragmented and slow.

- Business pain points
  - Low conversion from pre-approved offers due to friction (forms, branches, callbacks)
  - High turnaround time (TAT) and manual ops → drop-offs, stale leads
  - One-size-fits-all pricing and messaging → poor engagement
  - Siloed KYC/credit systems → delays and rework
  - Limited cross-sell/upsell nudges at the moment of intent

- Why now
  - Customers expect instant, chat-first experiences (WhatsApp/web chat)
  - Mature real-time underwriting rules and reliable bureau/kyc signals
  - WebSockets + lightweight UIs enable low-latency, scalable journeys

- Opportunity
  - Convert known users with pre-approved limits into instant loans
  - Personalize rate/tenure with risk-based pricing to maximize yield
  - Automate verification and sanction letters to reduce cost-to-serve
  
---

## 2) Your Approach to Solving the Problem

- Output form factor
  - Web-based Chatbot (live in this project). Real-time via WebSockets.

- Key user groups
  - Existing Retail Customers with pre-approved limits
  - NBFC Sales/Operations (monitor exceptions; lower manual work)

- User journey (happy path)
  1. Customer lands on web chat and enters Customer ID (demo IDs supported)
  2. Bot presents pre-approved limit and prompts for amount/tenure
  3. Sales Agent computes EMI and rate based on credit score
  4. Customer confirms → Verification Agent checks KYC
  5. Underwriting Agent runs rules (EMI-to-income, caps, salary verification)
  6. If approved → auto-generate sanction letter with fees and terms
  7. Display next steps and enable re-application or queries

- What’s implemented in this repo
  - FastAPI backend with `/ws/{client_id}` chat; MasterAgent orchestrates Sales, Verification, Underwriting, Sanction agents
  - Risk-based pricing (10.5–15.5%), EMI calc, instant/conditional/reject logic
  - Frontend chat UI with quick actions and document upload UX

---

## 3) Planned Solution Design

- High-level architecture (as-is + planned integrations)

```
[Browser: Chat UI]
   |  WebSocket (JSON messages)
   v
[FastAPI (main.py)] -- orchestrates --> [MasterAgent]
                              |----> [SalesAgent] (EMI, pricing)
                              |----> [VerificationAgent] (KYC)
                              |----> [UnderwritingAgent] (rules)
                              |----> [SanctionLetterGenerator]
                              
Planned external integrations:
- Credit Bureau API  ----> enrich credit score/history
- KYC e-Verification -> PAN/Aadhaar checks
- Salary/Bank APIs   -> income verification
- Core LMS/LOS       -> booking/disbursal
```

- Key technology components
  - Frontend: HTML/CSS/Vanilla JS chat UI (Font Awesome, Poppins)
  - Realtime: WebSocket channel for low-latency conversations
  - Backend: FastAPI + Uvicorn, Pydantic for models
  - AI Logic: Multi-agent orchestration with state machine
  - Rules & Data: Mock datasets for customers, KYC, bureau, salary slips (ready to swap for real APIs)

- Security & compliance (planned)
  - JWT session for chat, PII redaction logs, audit events
  - TLS in transit, encrypted storage, least-privileged service access

---

## 4) Potential Benefit and ROI

- Conversion and revenue levers
  - Higher conversion: instant approvals within pre-approved limits
  - Higher ticket size: EMI transparency nudges safe upsell
  - Yield optimization: risk-based pricing
  - Fee income: 1% processing fee per disbursal (shown in sanction letter)
  - Lower cost-to-serve: automation reduces manual handling

- KPIs to track (with targets)
  - Chat-to-application conversion: 5–8% (from 2–3%)
  - Instant approvals among eligible: >70%
  - Average ticket size uplift: +10–20%
  - Time-to-approval (TAT): minutes instead of days
  - Drop-off rate during underwriting: -30–50%

- Illustrative impact (1,000 existing customers targeted)
  - Before: 2% convert × ₹2,00,000 = ₹40,00,000 principal; fee ₹40,000; interest @13% ≈ ₹5.2L
  - After: 5% convert × ₹2,00,000 = ₹1,00,00,000 principal; fee ₹1,00,000; interest @13% ≈ ₹13L
  - Incremental interest ≈ ₹7.8L; incremental fees ≈ ₹60k; plus lower ops cost

- Beyond revenue
  - Better CX, higher NPS, higher reactivation of dormant users
  - Scalable architecture for voice/WhatsApp bot, and agent-assist

Notes for PPT transfer: Use one slide per section, place the ASCII diagram as an image replacement later if needed, and add your team/brand on the cover.
