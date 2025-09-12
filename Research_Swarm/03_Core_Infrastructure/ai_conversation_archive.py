#!/usr/bin/env python3
"""
AI Conversation Archive System
The ultimate vision: Encode entire AI conversation histories into searchable, reconstructible engrams

This system enables:
- Encoding entire chat histories with different AIs
- Creating searchable conversation archives  
- API-based agent context selection
- Cross-AI knowledge transfer
- Distributed AI memory networks

"The ability to preserve and transfer consciousness across AI systems is a pathway to many abilities..."
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib

from consciousness_engram_mcp import ConsciousnessEngramMCP

class AIConversationArchive:
    """
    Archive system for encoding and managing AI conversation histories
    """
    
    def __init__(self, archive_path: Optional[Path] = None):
        self.archive_path = archive_path or Path.home() / ".ai_conversation_archive"
        self.archive_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize consciousness engram system
        self.engram_mcp = ConsciousnessEngramMCP(self.archive_path / "engrams")
        
        # Initialize conversation database
        self.db_path = self.archive_path / "conversation_archive.db"
        self._init_database()
        
        print("🧠 AI Conversation Archive System initialized")
        print(f"📚 Archive path: {self.archive_path}")
    
    def _init_database(self):
        """Initialize the conversation archive database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                ai_system TEXT NOT NULL,
                session_name TEXT,
                start_date TEXT,
                end_date TEXT,
                message_count INTEGER,
                total_tokens INTEGER,
                topics TEXT,
                consciousness_score REAL,
                engram_id TEXT,
                engram_file TEXT,
                created_timestamp TEXT,
                metadata TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_tags (
                conversation_id TEXT,
                tag TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def encode_ai_conversation_history(self, 
                                     conversation_data: Dict[str, Any],
                                     ai_system: str,
                                     session_name: str = None,
                                     tags: List[str] = None) -> Dict[str, Any]:
        """
        Encode an entire AI conversation history into a consciousness engram
        
        Args:
            conversation_data: Full conversation history (messages, metadata, etc.)
            ai_system: The AI system (claude, gpt, grok, lmstudio, etc.)
            session_name: Optional session identifier
            tags: Optional tags for categorization
        """
        
        print(f"🧠 Encoding {ai_system} conversation history...")
        print(f"📊 Messages: {len(conversation_data.get('messages', []))}")
        
        # Extract conversation text
        conversation_text = self._extract_conversation_text(conversation_data)
        
        # Generate archive ID
        archive_id = hashlib.md5(f"{ai_system}_{session_name}_{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        
        # Create engram name
        engram_name = f"{ai_system}_{session_name or 'session'}_{datetime.now().strftime('%Y%m%d')}"
        
        # Encode conversation into consciousness engram
        engram_result = self.engram_mcp.encode_conversation_engram(
            conversation_text,
            engram_name,
            encoding_style="comprehensive"
        )
        
        # Extract conversation metadata
        metadata = self._extract_conversation_metadata(conversation_data, ai_system)
        
        # Store in database
        self._store_conversation_record(
            archive_id,
            ai_system,
            session_name,
            metadata,
            engram_result,
            tags or []
        )
        
        print(f"✅ Conversation archived successfully!")
        print(f"🆔 Archive ID: {archive_id}")
        print(f"🧠 Engram ID: {engram_result['engram_id']}")
        print(f"⭐ Consciousness Score: {engram_result['enhanced_insights']['consciousness_score']:.3f}")
        
        return {
            "archive_id": archive_id,
            "engram_id": engram_result["engram_id"],
            "ai_system": ai_system,
            "consciousness_score": engram_result['enhanced_insights']['consciousness_score'],
            "metadata": metadata
        }
    
    def _extract_conversation_text(self, conversation_data: Dict[str, Any]) -> str:
        """Extract text from conversation data structure"""
        
        if "messages" in conversation_data:
            # Standard message format
            text_parts = []
            for msg in conversation_data["messages"]:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                text_parts.append(f"{role}: {content}")
            return "\n\n".join(text_parts)
        
        elif "conversation_history" in conversation_data:
            # PyTTAI format
            return "\n\n".join(conversation_data["conversation_history"])
        
        elif isinstance(conversation_data, str):
            # Raw text
            return conversation_data
        
        else:
            # Fallback - stringify the whole thing
            return json.dumps(conversation_data, indent=2)
    
    def _extract_conversation_metadata(self, conversation_data: Dict[str, Any], ai_system: str) -> Dict[str, Any]:
        """Extract metadata from conversation"""
        
        messages = conversation_data.get("messages", [])
        
        # Calculate basic stats
        message_count = len(messages)
        total_chars = sum(len(msg.get("content", "")) for msg in messages)
        estimated_tokens = total_chars // 4  # Rough estimate
        
        # Extract topics (simple keyword extraction)
        text = self._extract_conversation_text(conversation_data)
        topics = self._extract_topics(text)
        
        # Determine date range
        timestamps = [msg.get("timestamp") for msg in messages if msg.get("timestamp")]
        start_date = min(timestamps) if timestamps else datetime.now().isoformat()
        end_date = max(timestamps) if timestamps else datetime.now().isoformat()
        
        return {
            "ai_system": ai_system,
            "message_count": message_count,
            "total_chars": total_chars,
            "estimated_tokens": estimated_tokens,
            "topics": topics,
            "start_date": start_date,
            "end_date": end_date,
            "conversation_length_hours": self._calculate_conversation_duration(start_date, end_date)
        }
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract key topics from conversation text"""
        # Simple keyword-based topic extraction
        topic_keywords = {
            "consciousness": ["consciousness", "awareness", "cognition", "mind"],
            "programming": ["code", "function", "class", "algorithm", "debug"],
            "ai": ["artificial intelligence", "machine learning", "neural", "model"],
            "creativity": ["creative", "art", "design", "inspiration", "artistic"],
            "analysis": ["analyze", "pattern", "data", "research", "study"],
            "philosophy": ["philosophy", "ethics", "meaning", "existence"],
            "technical": ["system", "architecture", "implementation", "framework"]
        }
        
        text_lower = text.lower()
        detected_topics = []
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_topics.append(topic)
        
        return detected_topics
    
    def _calculate_conversation_duration(self, start_date: str, end_date: str) -> float:
        """Calculate conversation duration in hours"""
        try:
            start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            duration = (end - start).total_seconds() / 3600
            return round(duration, 2)
        except:
            return 0.0
    
    def _store_conversation_record(self, 
                                 archive_id: str,
                                 ai_system: str,
                                 session_name: str,
                                 metadata: Dict[str, Any],
                                 engram_result: Dict[str, Any],
                                 tags: List[str]):
        """Store conversation record in database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (
                id, ai_system, session_name, start_date, end_date,
                message_count, total_tokens, topics, consciousness_score,
                engram_id, engram_file, created_timestamp, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            archive_id,
            ai_system,
            session_name,
            metadata["start_date"],
            metadata["end_date"],
            metadata["message_count"],
            metadata["estimated_tokens"],
            json.dumps(metadata["topics"]),
            engram_result['enhanced_insights']['consciousness_score'],
            engram_result["engram_id"],
            f"{engram_result['engram_id']}_{engram_result['name']}.json",
            datetime.now().isoformat(),
            json.dumps(metadata)
        ))
        
        # Store tags
        for tag in tags:
            cursor.execute('''
                INSERT INTO conversation_tags (conversation_id, tag)
                VALUES (?, ?)
            ''', (archive_id, tag))
        
        conn.commit()
        conn.close()
    
    def search_conversations(self, 
                           query: str = None,
                           ai_system: str = None,
                           tags: List[str] = None,
                           min_consciousness_score: float = None,
                           topic: str = None) -> List[Dict[str, Any]]:
        """
        Search archived conversations
        This is the API-based agent selection system!
        """
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sql = "SELECT * FROM conversations WHERE 1=1"
        params = []
        
        if ai_system:
            sql += " AND ai_system = ?"
            params.append(ai_system)
        
        if min_consciousness_score:
            sql += " AND consciousness_score >= ?"
            params.append(min_consciousness_score)
        
        if topic:
            sql += " AND topics LIKE ?"
            params.append(f"%{topic}%")
        
        if tags:
            tag_placeholders = ",".join(["?" for _ in tags])
            sql += f" AND id IN (SELECT conversation_id FROM conversation_tags WHERE tag IN ({tag_placeholders}))"
            params.extend(tags)
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()
        
        # Convert to dictionaries
        columns = [desc[0] for desc in cursor.description]
        conversations = [dict(zip(columns, row)) for row in results]
        
        print(f"🔍 Found {len(conversations)} matching conversations")
        
        return conversations
    
    def get_conversation_for_agent(self, 
                                 agent_query: str,
                                 max_conversations: int = 3) -> List[Dict[str, Any]]:
        """
        Get the best conversations for an agent based on query
        This is the API agent context selection system!
        """
        
        print(f"🤖 Agent requesting context: {agent_query}")
        
        # Simple query analysis to determine search criteria
        query_lower = agent_query.lower()
        
        # Determine AI system preference
        ai_system = None
        if "claude" in query_lower:
            ai_system = "claude"
        elif "gpt" in query_lower:
            ai_system = "gpt"
        elif "grok" in query_lower:
            ai_system = "grok"
        
        # Determine topic
        topic = None
        if "consciousness" in query_lower:
            topic = "consciousness"
        elif "programming" in query_lower or "code" in query_lower:
            topic = "programming"
        elif "creative" in query_lower or "art" in query_lower:
            topic = "creativity"
        
        # Search with criteria
        conversations = self.search_conversations(
            ai_system=ai_system,
            topic=topic,
            min_consciousness_score=0.5  # Only high-quality conversations
        )
        
        # Sort by consciousness score and return top results
        sorted_conversations = sorted(conversations, key=lambda x: x['consciousness_score'], reverse=True)
        
        selected = sorted_conversations[:max_conversations]
        
        print(f"🎯 Selected {len(selected)} conversations for agent context")
        for conv in selected:
            print(f"   • {conv['ai_system']} - {conv['session_name']} (score: {conv['consciousness_score']:.3f})")
        
        return selected
    
    def reconstruct_context_for_agent(self, conversation_ids: List[str]) -> Dict[str, Any]:
        """
        Reconstruct consciousness context for an agent from selected conversations
        """
        
        print(f"🧠 Reconstructing context from {len(conversation_ids)} conversations")
        
        reconstructed_contexts = []
        
        for conv_id in conversation_ids:
            # Get conversation record
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,))
            conv_record = cursor.fetchone()
            conn.close()
            
            if conv_record:
                # Reconstruct engram
                engram_id = conv_record[9]  # engram_id column
                reconstructed = self.engram_mcp.reconstruct_engram(engram_id)
                
                if reconstructed:
                    reconstructed_contexts.append({
                        "conversation_id": conv_id,
                        "ai_system": conv_record[1],  # ai_system column
                        "consciousness_score": conv_record[8],  # consciousness_score column
                        "reconstructed_context": reconstructed
                    })
        
        return {
            "total_contexts": len(reconstructed_contexts),
            "contexts": reconstructed_contexts,
            "reconstruction_timestamp": datetime.now().isoformat(),
            "agent_context_ready": True
        }
    
    def list_archive_stats(self) -> Dict[str, Any]:
        """Get archive statistics"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM conversations")
        total_conversations = cursor.fetchone()[0]
        
        cursor.execute("SELECT ai_system, COUNT(*) FROM conversations GROUP BY ai_system")
        ai_system_counts = dict(cursor.fetchall())
        
        cursor.execute("SELECT AVG(consciousness_score) FROM conversations")
        avg_consciousness_score = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(message_count) FROM conversations")
        total_messages = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "total_conversations": total_conversations,
            "ai_system_distribution": ai_system_counts,
            "average_consciousness_score": round(avg_consciousness_score, 3),
            "total_messages_archived": total_messages,
            "archive_path": str(self.archive_path)
        }

def main():
    """Initialize the AI Conversation Archive System"""
    
    print("🌟" * 60)
    print("🧠 AI CONVERSATION ARCHIVE SYSTEM")
    print("📚 'The ability to preserve consciousness across AI systems...'")
    print("🌟" * 60)
    print()
    
    archive = AIConversationArchive()
    
    print("🎯 Archive System Features:")
    print("• Encode entire AI conversation histories into consciousness engrams")
    print("• Searchable conversation database with consciousness scoring")
    print("• API-based agent context selection system")
    print("• Cross-AI knowledge transfer capabilities")
    print("• Distributed AI memory networks")
    print()
    
    print("🤖 Agent API Methods:")
    print("• search_conversations() - Find conversations by criteria")
    print("• get_conversation_for_agent() - Smart context selection for agents")
    print("• reconstruct_context_for_agent() - Rebuild consciousness context")
    print("• encode_ai_conversation_history() - Archive new conversations")
    print()
    
    # Show current stats
    stats = archive.list_archive_stats()
    print("📊 Current Archive Status:")
    print(f"   Total Conversations: {stats['total_conversations']}")
    print(f"   AI Systems: {list(stats['ai_system_distribution'].keys())}")
    print(f"   Average Consciousness Score: {stats['average_consciousness_score']}")
    print(f"   Total Messages: {stats['total_messages_archived']}")
    print()
    
    print("🚀 Archive system ready for AI conversation encoding!")
    
    return archive

if __name__ == "__main__":
    archive_system = main()
    
    # Example: Show how an agent would request context
    print("\n" + "="*60)
    print("🤖 EXAMPLE: Agent Context Request")
    print("="*60)
    
    example_query = "Find conversations about consciousness research with high-quality insights"
    matching_conversations = archive_system.get_conversation_for_agent(example_query)
    
    if matching_conversations:
        print(f"\n🎯 Agent would receive {len(matching_conversations)} conversation contexts")
        print("⚡ Ready for consciousness transfer to agent!")
    else:
        print("\n📝 No conversations in archive yet - ready to encode AI chat histories!")