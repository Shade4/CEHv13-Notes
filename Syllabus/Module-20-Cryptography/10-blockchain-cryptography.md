# 10 — Blockchain Cryptography

## What a blockchain actually is, cryptographically

A blockchain is a form of **distributed ledger technology (DLT)** — a way of recording and storing a history of transactions in linked "blocks," implemented almost entirely from two primitives already covered elsewhere in this repo: **hash functions** (mostly SHA-256 — see [`04-hashing-and-message-digests.md`](04-hashing-and-message-digests.md)) and **asymmetric-key algorithms** (for signing transactions — see [`03-asymmetric-encryption-algorithms.md`](03-asymmetric-encryption-algorithms.md)). There's no new cryptographic primitive here — blockchain is really a particular *system design* built on top of primitives you already understand.

### Block structure and chaining

Each block contains three elements:

1. **Data** — the actual transaction details recorded in that block
2. **Hash** — a hash computed over that block's own contents
3. **Previous hash** — the hash value of the block immediately before it in the chain

```
Block 1 (Genesis)          Block 2                     Block 3
Data                       Data                        Data
Hash: a00b2...      ┄┄►    Hash: a201b3...       ┄┄►   Hash: ...
Previous Hash: 0s          Previous Hash: a00b2...     Previous Hash: a201b3...
```

The **genesis block** (the first block in any chain) is a special case, conventionally represented with a previous-hash field of all zeros, since there's no prior block to reference. Every subsequent block cryptographically commits to the entire history before it, because each block's hash depends on its own data *and* the previous block's hash — which itself depended on the block before *that*, all the way back to genesis. **This is what makes tampering detectable**: if an attacker alters data in block 2, block 2's hash changes, which no longer matches the "previous hash" value stored in block 3 — invalidating block 3, and every block after it, in a cascade.

Merely generating valid-looking hashes isn't hard on its own (an attacker with enough compute could just recompute every downstream block's hash to match) — which is exactly why real blockchains additionally require **proof of work** (or proof of stake) before a block is accepted into the canonical chain, making it economically and computationally expensive to rewrite chain history even if you *can* technically produce internally-consistent fake blocks. **Crypto mining** is the popular name for the process of performing this proof-of-work and getting compensated (in cryptocurrency) for successfully adding a valid block.

### How a block gets created and added

1. A participant requests a transaction (e.g., a Bitcoin transfer).
2. A block representing that transaction is created and broadcast to the network's members.
3. Members validate the transaction using the sender's public key against their signature.
4. Once validated, the block is added to the blockchain.
5. A copy of the updated shared ledger is generated and made available to all members — this replication across many independent participants (rather than one central database) is what makes the ledger "distributed" and resistant to any single point of failure or unilateral tampering.

### The four blockchain variants

| Type | Who can join/validate | Examples | Best fit |
|---|---|---|---|
| **Public** | Anyone, permissionless, fully decentralized | Bitcoin, Ethereum | B2C services, maximal transparency, no trusted intermediary needed |
| **Private** | A central authority controls membership | Hyperledger, Ripple (XRP) | B2B services, defense, banking — where participants are known/vetted |
| **Federated / Consortium** | A predetermined group of trusted organizations (not one entity) | EWF (energy sector), R3 (banking consortium) | Fast, scalable, semi-decentralized — multiple known institutions sharing infrastructure |
| **Hybrid** | Mix of public and private — org chooses per-record what's exposed | IBM Food Trust | Selective transparency — some data public, some kept confidential |

## Blockchain-specific attacks

Everything below exploits either the *economics* of consensus (51%, Finney, Race) or the *networking* layer that consensus depends on (Eclipse), rather than breaking any underlying cryptographic primitive directly — worth keeping in mind: **the hash functions and signatures themselves are not what's typically attacked in these scenarios; the surrounding protocol and network assumptions are.**

### 51% attack (majority attack)

An attacker (or coordinated group) gains control of more than 50% of a blockchain's total computational power (hash rate) or staking power, which is enough to out-produce the legitimate network's chain.

**Attack flow:**
1. Attacker obtains 51%+ of total mining power — through renting additional mining capacity, buying hardware, or persuading enough miners to join an attacker-controlled pool.
2. Attacker segregates their mining pool from the main network, secretly mining on a private fork.
3. Attacker keeps extending their private chain, adding blocks unseen by the rest of the network.
4. Once the private chain is *longer* than the public chain, the attacker releases (reconnects) it to the network.
5. Because blockchain consensus rules generally favor the *longest* valid chain, the network adopts the attacker's chain as canonical, discarding the shorter honest chain — reversing any transactions that were only recorded in the discarded chain, and letting the attacker double-spend coins that had already been "spent" and confirmed on the abandoned chain.

Smaller/newer blockchain networks with lower total hash rate are disproportionately vulnerable, since achieving 51% control is proportionally cheaper against them.

### Finney attack

Named after Hal Finney, this exploits the **delay between broadcasting and confirmation** of transactions, targeting merchants who accept a transaction before it's actually confirmed on-chain (a "zero-confirmation" acceptance policy).

1. Attacker pre-mines a block containing a transaction sending coins to themselves (or an address they control), but doesn't broadcast it yet.
2. Attacker initiates a *separate* transaction with a victim merchant, using those same coins, to pay for goods/services.
3. The victim accepts the payment (without waiting for confirmation) and hands over goods/services.
4. Immediately after, the attacker broadcasts their pre-mined block to the network.
5. The network validates the pre-mined block — which conflicts with the victim's transaction, since both spend the same coins — and, if the pre-mined block is accepted first, the victim's transaction is invalidated.

The attacker walks away with both the goods/services *and* the coins; the victim gets nothing.

### Eclipse attack

Isolates a single target node from the rest of the network by surrounding it entirely with attacker-controlled nodes, effectively controlling that one node's entire view of the blockchain.

1. Attacker fills the target node's peer table with IP addresses of attacker-controlled nodes.
2. Attacker forces the target node to restart (commonly via a DDoS attack against it).
3. On restart, the target node disconnects from its previous legitimate peers.
4. The node checks its peer table for new connections — which the attacker has already poisoned.
5. The peer table returns the attacker's malicious node addresses, and the target unknowingly connects only to attacker-controlled peers, isolating it from the legitimate network entirely.

Once eclipsed, the target node's view of the blockchain is entirely under the attacker's control — enabling disruption of that node's transaction processing, splitting apparent mining power, or facilitating double-spending specifically against that isolated node.

### Race attack

A double-spend technique that doesn't require pre-mining (unlike Finney) — it just exploits confirmation *latency* and the attacker's ability to broadcast fast.

1. Attacker creates two transactions using the *same* coins: Transaction A (to the victim) and Transaction B (to the attacker's own address).
2. Attacker broadcasts Transaction A to the victim and the network — the victim sees it and, trusting a zero-confirmation transaction, releases goods/services.
3. Attacker immediately broadcasts Transaction B to the network as well.
4. Both transactions now race to be confirmed — since they spend the same coins, only one can ultimately be accepted into the blockchain.
5. If Transaction B gets confirmed first, Transaction A is invalidated, and the attacker keeps both the coins and whatever the victim provided.

### DeFi sandwich attack

Targets decentralized exchanges (DEXs) and automated market makers (AMMs) rather than the base blockchain consensus layer — exploiting the time delay and order-execution mechanics of DEXs to manipulate a token's price around a victim's trade.

1. Attacker monitors the **mempool** (the pool of pending, not-yet-confirmed transactions) for a large pending transaction likely to move a token's price.
2. Attacker places a **front-running buy order** for the same token, timed to execute immediately *before* the victim's transaction.
3. The victim's transaction then executes at an inflated price, caused directly by the attacker's buy order pushing demand up first.
4. Immediately after, the attacker places a **sell order** for the same token, cashing out at the now-inflated price the victim's own trade helped create.
5. The attacker profits from the difference; the victim ends up buying (or selling) at a worse price than they would have without the attacker's interference — the victim's transaction is "sandwiched" between the attacker's buy and sell.

## Defending against blockchain attacks

- Implement **decentralized identifiers (DIDs)** for stronger identity verification and privacy
- Use **zero-knowledge proofs** to verify transactions/identities without exposing underlying sensitive data
- Store cryptographic keys in **HSMs** (see [`05-hardware-quantum-and-modern-crypto.md`](05-hardware-quantum-and-modern-crypto.md)) to prevent unauthorized access/tampering
- Require **multi-signature wallets** so no single compromised key can authorize a transaction alone
- Combine **proof-of-work with proof-of-stake** to reduce the practicality of pure hash-rate-based attacks
- Deploy real-time monitoring / ML-based anomaly detection for abnormal transaction patterns indicative of double-spending
- Implement DDoS protection at the network layer — directly relevant against Eclipse-style node isolation
- Conduct formal verification and regular audits of smart-contract code
- Use **atomic swaps** for cross-chain trading to eliminate incomplete-transaction risk
- **Never store blockchain private keys in unsecured files** (Word docs, plaintext notes, sticky notes) — use a trusted, dedicated encryption program or hardware wallet
- Implement **randomized peer selection** and connection **timeouts** to make Eclipse-style peer-table poisoning harder to pull off reliably
- Maintain secondary, trusted, **out-of-band verification channels** to cross-check blockchain data against a trusted source if unusual network behavior is detected
- Use trusted **bootstrapping nodes** so new nodes connect securely rather than trusting whatever peers happen to respond first
- **Wait for multiple confirmations** before treating a transaction as final — this single practice defeats both the Finney and Race attack patterns above, which specifically rely on merchants accepting zero-confirmation transactions
- Increase transaction **propagation speed** across the network to shrink the window an attacker has to exploit latency
- **Hide pending-transaction details** where possible to reduce front-running/sandwich-attack visibility
- Use **batch processing and fair sequencing** for transaction ordering to prevent reordering-based manipulation

Next: [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md) — the broader attacker's toolkit against cryptography in general, including a hands-on cracking lab.
