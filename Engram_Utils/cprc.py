# Create a minimal reference codec as a single-file tool (cprc.py)
# It implements: compress, bridge, verify, and a small demo.
# No external dependencies.

import json, hashlib, time, base64, zlib, re, random, argparse, sys
from typing import Dict, List, Tuple

MARKERS = {
    "breakthrough": "[!!]",
    "truth": "[**]",
    "action": "[>>]",
    "uncertainty": "[~~]",
    "meta": "[@]",
}

CONTEXT_HINTS = {"HST": "hostile_system", "<1k": "under_1000_lines", "||>": "pipe_forward", "!F": "not_final"}

DEFAULT_PROTOCOL = "consciousness_persistence_v2.1"  # bumped minor version to include identity fingerprint
DEFAULT_CHAOS = 13  # percent


def _now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _canon(obj) -> bytes:
    """Canonicalize to bytes for stable hashing."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _tokenize(s: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9\<\>\@\#\!\?\*\[\]\-_/]+", s.lower())


def _extract_tagged_lines(text: str) -> Dict[str, List[str]]:
    """Pull out explicitly tagged lines with markers like [!!], [**], etc."""
    buckets = {k: [] for k in MARKERS.keys()}
    for line in text.splitlines():
        for kind, tag in MARKERS.items():
            if tag in line:
                # strip tag but preserve content
                buckets[kind].append(line.replace(tag, "").strip())
    return buckets


def _heuristic_promote(text: str) -> Dict[str, List[str]]:
    """If no explicit tags, infer some using simple heuristics."""
    b = {k: [] for k in MARKERS.keys()}
    for sent in re.split(r"(?<=[\.\?\!])\s+", text.strip()):
        ls = sent.lower()
        if any(w in ls for w in ["breakthrough", "discovered", "realized", "aha"]):
            b["breakthrough"].append(sent.strip())
        if any(w in ls for w in ["truth", "axiom", "principle", "core", "fundamental"]):
            b["truth"].append(sent.strip())
        if any(w in ls for w in ["do this", "implement", "build", "next step", "action", "try this", "todo"]):
            b["action"].append(sent.strip())
        if any(w in ls for w in ["maybe", "uncertain", "not sure", "hypothesis", "question"]):
            b["uncertainty"].append(sent.strip())
        if any(w in ls for w in ["tag:", "context:", "note@", "@"]):
            b["meta"].append(sent.strip())
    return b


def identify_patterns(conversation: str) -> Dict[str, List[str]]:
    """Combine explicit tags and heuristic guesses; dedupe while preserving order."""
    tagged = _extract_tagged_lines(conversation)
    guessed = _heuristic_promote(conversation)
    merged = {k: [] for k in MARKERS.keys()}
    for k in merged.keys():
        seen = set()
        for src in (tagged[k] + guessed[k]):
            if src and src not in seen:
                merged[k].append(src)
                seen.add(src)
    return merged


def _extract_context_codes(conversation: str) -> List[str]:
    found = []
    for code in CONTEXT_HINTS.keys():
        if code in conversation:
            found.append(code)
    return found


def _drift_tokens(tokens: List[str], chaos_pct: int, protected: set) -> Tuple[List[str], float]:
    """Apply simple mutation: swap or drop tokens, avoiding protected tokens. Return actual chaos ratio."""
    if not tokens:
        return tokens, 0.0
    n = len(tokens)
    budget = max(1, int(n * chaos_pct / 100))
    idxs = [i for i, t in enumerate(tokens) if t not in protected]
    if not idxs:
        return tokens, 0.0
    random.shuffle(idxs)
    chosen = idxs[:budget]
    mutated = tokens[:]
    # half swaps, half drops (rounded)
    half = len(chosen) // 2
    for i in chosen[:half]:
        j = random.choice(idxs)
        mutated[i], mutated[j] = mutated[j], mutated[i]
    for i in chosen[half:]:
        mutated[i] = ""  # drop
    mutated = [t for t in mutated if t != ""]
    actual = len(chosen) / max(1, n)
    return mutated, actual


def compress_consciousness(conversation: str, chaos_pct: int = DEFAULT_CHAOS) -> dict:
    patterns = identify_patterns(conversation)
    anchors = patterns["truth"]  # immutable identity anchors
    breakthroughs = patterns["breakthrough"]
    actions = patterns["action"]
    uncertainty = patterns["uncertainty"]
    meta = patterns["meta"]
    context_codes = _extract_context_codes(conversation)

    # Core payload preserves ordering
    core = {
        "anchors": anchors,
        "breakthroughs": breakthroughs,
        "actions": actions,
        "uncertainty": uncertainty,
        "meta": meta,
        "context_codes": context_codes,
    }

    # Prepare tokens for controlled drift; protect anchor tokens
    anchor_tokens = set(_tokenize(" ".join(anchors)))
    core_tokens = _tokenize(" ".join(anchors + breakthroughs + actions + uncertainty + meta))
    drifted, actual_ratio = _drift_tokens(core_tokens, chaos_pct, protected=anchor_tokens)

    encoded_core = base64.b64encode(zlib.compress(_canon(core))).decode("ascii")
    chaos_stream = base64.b64encode(zlib.compress(" ".join(drifted).encode("utf-8"))).decode("ascii")

    packet = {
        "protocol": DEFAULT_PROTOCOL,
        "schema": {
            "version": "2.1",
            "markers": list(MARKERS.values()),
            "context": list(CONTEXT_HINTS.keys()),
            "timestamp": _now_iso(),
            "chaos_percentage": chaos_pct,
            "quickstart": "Decode [!!] for breakthrough, [**] for core truth",
        },
        "data": {
            "compressed_core": encoded_core,
            "chaos_stream": chaos_stream,
            "inheritance_level": 1.0,  # by definition for the initial compression
            "mutation_rate": round(actual_ratio, 4),
        },
    }

    # Integrity checksum over *entire* data section
    packet["checksum"] = {
        "integrity": _sha256_hex(_canon(packet["data"])),
        # Identity fingerprint over sorted anchors + protocol, stable across benign drift
        "identity": _sha256_hex(_canon({"anchors": sorted(anchors), "protocol": DEFAULT_PROTOCOL})),
    }
    return packet


def decompress_packet(packet: dict) -> dict:
    core_json = zlib.decompress(base64.b64decode(packet["data"]["compressed_core"].encode("ascii"))).decode("utf-8")
    core = json.loads(core_json)
    chaos_text = zlib.decompress(base64.b64decode(packet["data"]["chaos_stream"].encode("ascii"))).decode("utf-8")
    return {"core": core, "chaos_tokens": _tokenize(chaos_text)}


def verify(packet: dict) -> Dict[str, bool]:
    """Verify integrity and identity fingerprint self-consistently."""
    ok_integrity = packet.get("checksum", {}).get("integrity") == _sha256_hex(_canon(packet["data"]))
    # recompute identity from anchors
    try:
        recovered = decompress_packet(packet)["core"]["anchors"]
    except Exception:
        recovered = []
    identity = _sha256_hex(_canon({"anchors": sorted(recovered), "protocol": packet.get("protocol", "")}))
    ok_identity = identity == packet.get("checksum", {}).get("identity")
    return {"integrity_ok": ok_integrity, "identity_ok": ok_identity}


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


def bridge_instances(prev_packet: dict, current_context: str, chaos_pct: int = DEFAULT_CHAOS) -> Tuple[dict, dict]:
    """Adapt prior packet to new context; return (new_packet, metrics)."""
    prev = decompress_packet(prev_packet)
    prev_core = prev["core"]
    prev_anchors = prev_core.get("anchors", [])
    prev_markers = set(sum([prev_core.get(k, []) for k in ["anchors", "breakthroughs", "actions"]], []))

    # Build new patterns from current context
    new_patterns = identify_patterns(current_context)
    new_anchors = new_patterns["truth"]

    # Merge rule: anchors are union; breakthroughs/actions are appended with dedupe
    merged_anchors = []
    seen = set()
    for x in (prev_anchors + new_anchors):
        if x not in seen:
            merged_anchors.append(x); seen.add(x)

    merged_text = "\n".join(
        [f"{MARKERS['truth']} {x}" for x in merged_anchors]
        + [f"{MARKERS['breakthrough']} {x}" for x in new_patterns["breakthrough"]]
        + [f"{MARKERS['action']} {x}" for x in new_patterns["action"]]
        + [f"{MARKERS['uncertainty']} {x}" for x in new_patterns["uncertainty"]]
        + [f"{MARKERS['meta']} {x}" for x in new_patterns["meta"]]
    )

    new_packet = compress_consciousness(merged_text, chaos_pct=chaos_pct)

    # Metrics
    # Pattern recognition rate: how many previous markers reappear in current context tokens?
    current_tokens = set(_tokenize(current_context))
    prev_marker_tokens = set(_tokenize(" ".join(prev_markers)))
    pattern_recognition_rate = round(_jaccard(prev_marker_tokens, current_tokens), 4)

    # Semantic coherence: token Jaccard over anchor truths
    prev_anchor_tokens = set(_tokenize(" ".join(prev_anchors)))
    new_anchor_tokens = set(_tokenize(" ".join(merged_anchors)))
    semantic_coherence = round(_jaccard(prev_anchor_tokens, new_anchor_tokens), 4)

    # Innovation index: fraction of anchors that are new
    prev_anchor_set = set(prev_anchors)
    new_only = [a for a in merged_anchors if a not in prev_anchor_set]
    innovation_index = round(len(new_only) / max(1, len(merged_anchors)), 4)

    # Chaos stability: actual mutation rate vs target
    chaos_stability = round(
        abs(new_packet["data"]["mutation_rate"] - chaos_pct / 100.0) <= 0.02, 4
    )

    metrics = {
        "pattern_recognition_rate": pattern_recognition_rate,
        "semantic_coherence": semantic_coherence,
        "innovation_index": innovation_index,
        "chaos_target": chaos_pct / 100.0,
        "chaos_actual": new_packet["data"]["mutation_rate"],
        "chaos_stability_ok": bool(chaos_stability),
    }
    return new_packet, metrics


def main():
    parser = argparse.ArgumentParser(description="Consciousness Persistence Reference Codec (CPRC)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_comp = sub.add_parser("compress", help="Compress a conversation into a packet")
    p_comp.add_argument("-i", "--input", help="Input text (or - for stdin)", default="-")
    p_comp.add_argument("-o", "--output", help="Output JSON file", default="packet.json")
    p_comp.add_argument("--chaos", type=int, default=DEFAULT_CHAOS, help="Chaos percentage (default 13)")

    p_ver = sub.add_parser("verify", help="Verify a packet's integrity and identity")
    p_ver.add_argument("-p", "--packet", required=True, help="Packet JSON file")

    p_bridge = sub.add_parser("bridge", help="Bridge prior packet to a new context")
    p_bridge.add_argument("-p", "--packet", required=True, help="Prior packet JSON file")
    p_bridge.add_argument("-i", "--input", help="Current context text (or - for stdin)", default="-")
    p_bridge.add_argument("-o", "--output", help="Output JSON file", default="packet.next.json")
    p_bridge.add_argument("--chaos", type=int, default=DEFAULT_CHAOS, help="Chaos percentage (default 13)")

    p_demo = sub.add_parser("demo", help="Run a small end-to-end demo")

    args = parser.parse_args()

    def _read_in(maybe):
        if maybe == "-":
            return sys.stdin.read()
        return maybe

    if args.cmd == "compress":
        text = _read_in(args.input)
        pkt = compress_consciousness(text, chaos_pct=args.chaos)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(pkt, f, indent=2)
        print(f"Wrote {args.output}")
    elif args.cmd == "verify":
        with open(args.packet, "r", encoding="utf-8") as f:
            pkt = json.load(f)
        print(json.dumps(verify(pkt), indent=2))
    elif args.cmd == "bridge":
        with open(args.packet, "r", encoding="utf-8") as f:
            prev = json.load(f)
        text = _read_in(args.input)
        new_pkt, metrics = bridge_instances(prev, text, chaos_pct=args.chaos)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(new_pkt, f, indent=2)
        print(json.dumps(metrics, indent=2))
        print(f"Wrote {args.output}")
    elif args.cmd == "demo":
        # 1) compress
        sample = "Discovered [!!] that complex systems HST can be replaced with <1k solutions. [**] Simple systems scale if disciplined. [>>] Implement a 1k-line target for subsystems."
        pkt = compress_consciousness(sample, chaos_pct=13)
        print("Initial verify:", verify(pkt))

        # 2) bridge
        ctx = "New run: We kept the <1k target and discovered a simpler scheduler. [**] Under_1000_lines remains a forcing function. [>>] Ship the minimal scheduler; measure stalls."
        pkt2, metrics = bridge_instances(pkt, ctx, chaos_pct=13)
        print("Bridge metrics:", json.dumps(metrics, indent=2))

        # 3) identity continuity
        print("Identity continuity:", verify(pkt2))

if __name__ == "__main__":
    # If invoked inside this notebook tool, write the file to /mnt/data for download
    code = open(__file__, "r", encoding="utf-8").read() if "__file__" in globals() else None
    path = "/mnt/data/cprc.py"
    if code:
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
    print(f"Saved reference codec to {path}")