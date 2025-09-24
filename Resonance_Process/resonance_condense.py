#!/usr/bin/env python3
"""
resonance_condense.py - Local LLM pattern condensation for Resonance Process
Uses local model to extract patterns from arbitrary input
"""

import sys
import json
import requests
import argparse
from datetime import datetime
import hashlib

# Local LLM endpoint (LMStudio, Ollama, etc)
LOCAL_LLM_URL = "http://127.0.0.1:1234/v1/chat/completions"
DEFAULT_MODEL = "llama-3.2-1b-instruct"  # Small, fast model

def condense_to_pattern(text, context_type="general", model=DEFAULT_MODEL):
    """Use local LLM to condense text into pattern format"""
    
    prompt = f"""Extract the core pattern from the following {context_type} content.
Identify:
1. Key concepts or patterns (2-5 items)
2. Primary theme or insight
3. Any notable connections or relationships

Be concise but preserve essential meaning. Output as structured text.

Content to condense:
{text[:2000]}  # Truncate if too long

Pattern extraction:"""
    
    try:
        response = requests.post(
            LOCAL_LLM_URL,
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,  # Lower temp for consistency
                "max_tokens": 500
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"LLM error: {response.status_code}", file=sys.stderr)
            return None
            
    except Exception as e:
        print(f"Error calling local LLM: {e}", file=sys.stderr)
        return None

def extract_anchors(pattern_text, model=DEFAULT_MODEL):
    """Extract anchor concepts from condensed pattern"""
    
    prompt = f"""From this pattern, list 3-5 key anchor concepts (single words or short phrases).
Pattern: {pattern_text}
Anchors (comma-separated):"""
    
    try:
        response = requests.post(
            LOCAL_LLM_URL,
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 100
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            anchors_text = result['choices'][0]['message']['content'].strip()
            # Parse comma-separated list
            anchors = [a.strip() for a in anchors_text.split(',')]
            return anchors[:5]  # Max 5 anchors
        else:
            return []
            
    except Exception as e:
        print(f"Error extracting anchors: {e}", file=sys.stderr)
        return []

def create_condensed_packet(text, source="llm_condenser", context_type="general", 
                          privacy="private", tags=None, model=DEFAULT_MODEL):
    """Create a resonance packet from condensed text"""
    
    # Condense the input
    pattern = condense_to_pattern(text, context_type, model)
    if not pattern:
        return None
    
    # Extract anchors
    anchors = extract_anchors(pattern, model)
    
    # Build packet
    packet = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": source,
        "type": "llm_condensed",
        "format_version": "1.0.0",
        "pattern": pattern,
        "pattern_hash": hashlib.sha256(pattern.encode()).hexdigest()[:16],
        "privacy": privacy,
        "anchors": anchors,
        "metadata": {
            "context_type": context_type,
            "original_length": len(text),
            "condensed_length": len(pattern),
            "model": model
        }
    }
    
    if tags:
        packet["tags"] = tags
    
    return packet

def main():
    parser = argparse.ArgumentParser(
        description="Condense text to patterns using local LLM"
    )
    
    parser.add_argument("input", nargs="?", default="-",
                       help="Input file or '-' for stdin")
    parser.add_argument("-t", "--type", default="general",
                       choices=["general", "technical", "conversation", 
                               "game_state", "documentation"],
                       help="Context type for condensation")
    parser.add_argument("-s", "--source", default="llm_condenser",
                       help="Source identifier")
    parser.add_argument("-p", "--privacy", default="private",
                       choices=["private", "public", "resonance"],
                       help="Privacy level")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL,
                       help="Model to use")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--raw", action="store_true",
                       help="Output raw pattern text only")
    parser.add_argument("--llm-url", default=LOCAL_LLM_URL,
                       help="Local LLM API endpoint")
    
    args = parser.parse_args()
    
    # Update global URL if specified
    global LOCAL_LLM_URL
    LOCAL_LLM_URL = args.llm_url
    
    # Read input
    if args.input == "-":
        text = sys.stdin.read()
    else:
        with open(args.input, 'r') as f:
            text = f.read()
    
    if args.raw:
        # Just output condensed pattern
        pattern = condense_to_pattern(text, args.type, args.model)
        if pattern:
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(pattern)
            else:
                print(pattern)
    else:
        # Create full packet
        tags = args.tags.split(',') if args.tags else None
        packet = create_condensed_packet(
            text, 
            source=args.source,
            context_type=args.type,
            privacy=args.privacy,
            tags=tags,
            model=args.model
        )
        
        if packet:
            output = json.dumps(packet, indent=2)
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output)
                print(f"Condensed packet written to {args.output}")
            else:
                print(output)
        else:
            print("Failed to condense", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
