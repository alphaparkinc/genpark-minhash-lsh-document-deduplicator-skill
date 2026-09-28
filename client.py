"""MinHash & Locality-Sensitive Hashing (LSH) Engine
100% Python Standard Library (re).
"""

import re

class MinHashLSHDeduplicator:
    """Near-duplicate document detection using MinHash permutations and LSH banding."""
    def __init__(self, num_perm=32, num_bands=8, shingle_size=3):
        self.num_perm = num_perm
        self.num_bands = num_bands
        self.rows_per_band = num_perm // num_bands
        self.shingle_size = shingle_size
        self.prime = 4294967311
        self.hash_params = [(3 * i + 7, 5 * i + 11) for i in range(num_perm)]

    def _get_shingles(self, text):
        clean = re.sub(r"\s+", " ", text.lower().strip())
        shingles = set()
        for i in range(max(1, len(clean) - self.shingle_size + 1)):
            shingles.add(clean[i : i + self.shingle_size])
        return shingles

    def compute_signature(self, text):
        shingles = self._get_shingles(text)
        sig = [float('inf')] * self.num_perm
        for sh in shingles:
            hv = abs(hash(sh))
            for i, (a, b) in enumerate(self.hash_params):
                h = (a * hv + b) % self.prime
                if h < sig[i]:
                    sig[i] = h
        return sig

    def estimate_jaccard(self, sig1, sig2):
        matches = sum(1 for a, b in zip(sig1, sig2) if a == b)
        return round(matches / self.num_perm, 4)
