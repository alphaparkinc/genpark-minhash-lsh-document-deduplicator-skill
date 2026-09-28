import sys
import json
from client import MinHashLSHDeduplicator

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-minhash-lsh-document-deduplicator-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "estimate_similarity",
                    "description": "Estimate Jaccard similarity between two text documents via MinHash signatures",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "doc_a": {"type": "string"},
                            "doc_b": {"type": "string"},
                            "num_perm": {"type": "integer", "default": 32}
                        },
                        "required": ["doc_a", "doc_b"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "estimate_similarity":
            np = args.get("num_perm", 32)
            lsh = MinHashLSHDeduplicator(num_perm=np)
            sig_a = lsh.compute_signature(args.get("doc_a", ""))
            sig_b = lsh.compute_signature(args.get("doc_b", ""))
            jaccard = lsh.estimate_jaccard(sig_a, sig_b)
            res = {"content": [{"type": "text", "text": json.dumps({"estimated_jaccard": jaccard, "is_near_duplicate": jaccard >= 0.7})}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
