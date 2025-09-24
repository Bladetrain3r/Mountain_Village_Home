#!/usr/bin/env python3
"""
resonance_packet.py - Manual packet creation for Resonance Process
Minimal dependencies, pipe-friendly, creates standardized JSON packets
"""

import json
import hashlib
from datetime import datetime
import sys
import argparse

def create_packet():
    """Interactive packet creation"""
    print("=== Resonance Process Packet Creator ===\n")
    
    # Basic metadata
    packet = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "human_ziggy",  # Your identifier
        "type": "manual_entry",
        "format_version": "1.0.0"
    }
    
    # Get pattern content
    print("Enter pattern content (Ctrl+D or empty line to finish):")
    lines = []
    while True:
        try:
            line = input()
            if not line:
                break
            lines.append(line)
        except EOFError:
            break
    
    pattern = "\n".join(lines)
    packet["pattern"] = pattern
    packet["pattern_hash"] = hashlib.sha256(pattern.encode()).hexdigest()[:16]
    
    # Context metadata
    print("\nContext tags (comma-separated, or Enter to skip):")
    tags = input().strip()
    if tags:
        packet["tags"] = [t.strip() for t in tags.split(",")]
    
    print("\nPrivacy level (private/public/resonance) [private]:")
    privacy = input().strip() or "private"
    packet["privacy"] = privacy
    
    print("\nResonance anchors (key concepts, comma-separated):")
    anchors = input().strip()
    if anchors:
        packet["anchors"] = [a.strip() for a in anchors.split(",")]
    
    print("\nRelated to instance_id (or Enter for none):")
    related = input().strip()
    if related:
        packet["related_instance"] = related
    
    # Optional notes
    print("\nAdditional notes (Enter to skip):")
    notes = input().strip()
    if notes:
        packet["notes"] = notes
    
    return packet

def create_packet_args(args):
    """Create packet from command line arguments"""
    packet = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": args.source or "human_ziggy",
        "type": "manual_entry",
        "format_version": "1.0.0",
        "pattern": args.pattern,
        "pattern_hash": hashlib.sha256(args.pattern.encode()).hexdigest()[:16],
        "privacy": args.privacy
    }
    
    if args.tags:
        packet["tags"] = args.tags.split(",")
    
    if args.anchors:
        packet["anchors"] = args.anchors.split(",")
    
    if args.instance:
        packet["related_instance"] = args.instance
    
    if args.notes:
        packet["notes"] = args.notes
    
    return packet

def main():
    parser = argparse.ArgumentParser(
        description="Create standardized packets for Resonance Process"
    )
    parser.add_argument("-p", "--pattern", help="Pattern content (or use stdin)")
    parser.add_argument("-t", "--tags", help="Comma-separated tags")
    parser.add_argument("-a", "--anchors", help="Comma-separated anchor concepts")
    parser.add_argument("--privacy", default="private", 
                       choices=["private", "public", "resonance"],
                       help="Privacy level")
    parser.add_argument("-i", "--instance", help="Related instance ID")
    parser.add_argument("-n", "--notes", help="Additional notes")
    parser.add_argument("-s", "--source", help="Source identifier")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument("--interactive", action="store_true", 
                       help="Interactive mode")
    
    args = parser.parse_args()
    
    # Handle input modes
    if args.interactive or (not args.pattern and sys.stdin.isatty()):
        # Interactive mode
        packet = create_packet()
    elif args.pattern:
        # Command line arguments
        packet = create_packet_args(args)
    else:
        # Read pattern from stdin
        args.pattern = sys.stdin.read().strip()
        packet = create_packet_args(args)
    
    # Output
    json_output = json.dumps(packet, indent=2)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_output)
        print(f"Packet written to {args.output}")
    else:
        print("\n=== Generated Packet ===")
        print(json_output)

if __name__ == "__main__":
    main()
