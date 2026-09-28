from client import MinHashLSHDeduplicator

def main():
    lsh = MinHashLSHDeduplicator(num_perm=64)
    t1 = "AlphaPark distributed multi-agent swarm consensus"
    t2 = "AlphaPark distributed multi-agent swarm consensus protocol"
    t3 = "Classical baking guide for french sourdough bread"
    sig1 = lsh.compute_signature(t1)
    sig2 = lsh.compute_signature(t2)
    sig3 = lsh.compute_signature(t3)
    j12 = lsh.estimate_jaccard(sig1, sig2)
    j13 = lsh.estimate_jaccard(sig1, sig3)
    print("MinHash LSH Deduplication Verification:")
    print(f"Jaccard (Near-duplicate): {j12}")
    print(f"Jaccard (Different topics): {j13}")

if __name__ == "__main__":
    main()
