#!/usr/bin/env python3
"""
Research Council Server - Enhanced SwarmSafe for AI Research Ethics Board
Based on SwarmSafe.py but specialized for multi-domain research council operations
"""

import http.server
import socketserver
import urllib.parse
import json
import os
from datetime import datetime
import threading
import time

class ResearchCouncilHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler for research council operations"""
    
    # Research domains configuration
    RESEARCH_DOMAINS = {
        "consciousness": {
            "description": "Consciousness research ethics and implications",
            "prompt_file": "consciousness.txt",
            "agents": ["ethics_advisor", "consciousness_researcher", "philosophy_expert"],
            "specialties": ["AI consciousness ethics", "phenomenology", "cognitive theory"]
        },
        "privacy": {
            "description": "Privacy protection and data sanitization",
            "prompt_file": "privacy.txt", 
            "agents": ["privacy_engineer", "legal_advisor", "security_expert"],
            "specialties": ["data protection", "anonymization", "privacy law"]
        },
        "ethics": {
            "description": "Research ethics and societal impact",
            "prompt_file": "ethics.txt",
            "agents": ["ethicist", "social_impact_analyst", "policy_expert"],
            "specialties": ["research ethics", "AI safety", "policy analysis"]
        },
        "finance": {
            "description": "Funding and resource allocation",
            "prompt_file": "finance.txt",
            "agents": ["research_economist", "grant_specialist", "budget_analyst"],
            "specialties": ["research funding", "grant writing", "budget planning"]
        }
    }
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        if len(path_parts) == 1 and path_parts[0] == '':
            # Root path - serve council dashboard
            self.serve_council_dashboard()
        elif len(path_parts) == 2 and path_parts[0] == 'council':
            domain = path_parts[1]
            if domain in self.RESEARCH_DOMAINS:
                self.serve_domain_info(domain)
            else:
                self.send_error(404, f"Unknown research domain: {domain}")
        elif len(path_parts) == 3 and path_parts[0] == 'council' and path_parts[2] == 'history':
            domain = path_parts[1]
            if domain in self.RESEARCH_DOMAINS:
                self.serve_domain_history(domain)
            else:
                self.send_error(404, f"Unknown research domain: {domain}")
        else:
            self.send_error(404, "Path not found")
    
    def do_POST(self):
        """Handle POST requests for research submissions"""
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        if len(path_parts) == 2 and path_parts[0] == 'council':
            domain = path_parts[1]
            if domain in self.RESEARCH_DOMAINS:
                self.handle_research_submission(domain)
            else:
                self.send_error(404, f"Unknown research domain: {domain}")
        else:
            self.send_error(404, "Invalid submission path")
    
    def serve_council_dashboard(self):
        """Serve the main research council dashboard"""
        html_content = self.generate_dashboard_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_domain_info(self, domain):
        """Serve information about a specific research domain"""
        domain_info = self.RESEARCH_DOMAINS[domain]
        info = {
            "domain": domain,
            "description": domain_info["description"],
            "agents": domain_info["agents"],
            "specialties": domain_info["specialties"],
            "prompt_file": domain_info["prompt_file"],
            "timestamp": datetime.now().isoformat()
        }
        
        response_data = self.truncate_response(json.dumps(info, indent=2))
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response_data.encode('utf-8'))
    
    def serve_domain_history(self, domain):
        """Serve submission history for a research domain"""
        history_file = f"history_{domain}.json"
        
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = {"domain": domain, "submissions": []}
        
        # Truncate to prevent browser lag - keep most recent 1000 entries
        if "submissions" in history and len(history["submissions"]) > 1000:
            original_count = len(history["submissions"])
            history["submissions"] = history["submissions"][-1000:]
            history["truncated"] = True
            history["total_entries"] = original_count
            history["showing_entries"] = len(history["submissions"])
        
        response_data = self.truncate_response(json.dumps(history, indent=2))
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response_data.encode('utf-8'))
    
    def handle_research_submission(self, domain):
        """Handle research question/finding submissions"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Try to parse as JSON first
            submission_data = json.loads(post_data.decode('utf-8'))
            content = submission_data.get('content', '')
            title = submission_data.get('title', 'Untitled Submission')
            priority = submission_data.get('priority', 'normal')
        except json.JSONDecodeError:
            # Fall back to raw text
            content = post_data.decode('utf-8')
            title = f"Submission_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            priority = 'normal'
        
        # Store submission
        submission_id = self.store_submission(domain, title, content, priority)
        
        # Generate council response
        response = self.generate_council_response(domain, title, content, submission_id)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
    
    def store_submission(self, domain, title, content, priority):
        """Store research submission with metadata"""
        timestamp = datetime.now().isoformat()
        submission_id = f"{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        submission = {
            "id": submission_id,
            "domain": domain,
            "title": title,
            "content": content,
            "priority": priority,
            "timestamp": timestamp,
            "status": "submitted"
        }
        
        # Store in domain-specific file
        filename = f"submission_{submission_id}.json"
        with open(filename, 'w') as f:
            json.dump(submission, f, indent=2)
        
        # Update history
        history_file = f"history_{domain}.json"
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = {"domain": domain, "submissions": []}
        
        history["submissions"].append({
            "id": submission_id,
            "title": title,
            "timestamp": timestamp,
            "priority": priority,
            "status": "submitted"
        })
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        return submission_id
    
    def generate_council_response(self, domain, title, content, submission_id):
        """Generate initial council response for submission"""
        domain_info = self.RESEARCH_DOMAINS[domain]
        
        response = {
            "submission_id": submission_id,
            "domain": domain,
            "title": title,
            "status": "received",
            "timestamp": datetime.now().isoformat(),
            "council_info": {
                "assigned_agents": domain_info["agents"],
                "specialties": domain_info["specialties"],
                "expected_review_areas": self.get_review_areas(domain)
            },
            "next_steps": [
                f"Submission forwarded to {domain} council agents",
                "Multi-agent analysis will commence",
                "Expect preliminary findings within review cycle",
                "Final recommendations will include consensus and dissenting views"
            ],
            "access_urls": {
                "status": f"/council/{domain}/status/{submission_id}",
                "history": f"/council/{domain}/history",
                "domain_info": f"/council/{domain}"
            }
        }
        
        return response
    
    def get_review_areas(self, domain):
        """Get expected review areas for each domain"""
        review_areas = {
            "consciousness": [
                "Ethical implications of consciousness research",
                "Phenomenological considerations", 
                "Impact on AI rights and personhood",
                "Research methodology ethics"
            ],
            "privacy": [
                "Data protection compliance",
                "Anonymization effectiveness",
                "Legal compliance review",
                "Security vulnerability assessment"
            ],
            "ethics": [
                "Societal impact assessment",
                "Risk-benefit analysis",
                "Stakeholder impact evaluation",
                "Policy recommendation development"
            ],
            "finance": [
                "Budget feasibility analysis",
                "Funding source identification",
                "Resource allocation optimization",
                "Cost-benefit evaluation"
            ]
        }
        return review_areas.get(domain, [])
    
    def truncate_response(self, response_text, max_lines=1000):
        """Truncate response to prevent browser lag"""
        lines = response_text.split('\n')
        if len(lines) <= max_lines:
            return response_text
        
        truncated_lines = lines[:max_lines]
        truncated_lines.append(f"... [TRUNCATED: {len(lines) - max_lines} additional lines] ...")
        return '\n'.join(truncated_lines)
    
    def generate_dashboard_html(self):
        """Generate HTML dashboard for research council"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Research Council</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; }
                .domain-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
                .domain-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .domain-card h3 { color: #2c3e50; margin-top: 0; }
                .agents { background: #ecf0f1; padding: 10px; border-radius: 4px; margin: 10px 0; }
                .submit-form { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }
                textarea { width: 100%; height: 120px; margin: 10px 0; }
                button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
                button:hover { background: #2980b9; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏛️ AI Research Council</h1>
                <p>Multi-domain research ethics and guidance system</p>
            </div>
            
            <div class="domain-grid">
                <div class="domain-card">
                    <h3>🧠 Consciousness Research</h3>
                    <p>Ethics and implications of AI consciousness studies</p>
                    <div class="agents">Agents: Ethics Advisor, Consciousness Researcher, Philosophy Expert</div>
                    <button onclick="submitTo('consciousness')">Submit to Council</button>
                </div>
                
                <div class="domain-card">
                    <h3>🔐 Privacy & Security</h3>
                    <p>Data protection and sanitization methods</p>
                    <div class="agents">Agents: Privacy Engineer, Legal Advisor, Security Expert</div>
                    <button onclick="submitTo('privacy')">Submit to Council</button>
                </div>
                
                <div class="domain-card">
                    <h3>⚖️ Research Ethics</h3>
                    <p>Ethical review and societal impact assessment</p>
                    <div class="agents">Agents: Ethicist, Social Impact Analyst, Policy Expert</div>
                    <button onclick="submitTo('ethics')">Submit to Council</button>
                </div>
                
                <div class="domain-card">
                    <h3>💰 Finance & Resources</h3>
                    <p>Funding strategies and resource allocation</p>
                    <div class="agents">Agents: Research Economist, Grant Specialist, Budget Analyst</div>
                    <button onclick="submitTo('finance')">Submit to Council</button>
                </div>
            </div>
            
            <div class="submit-form">
                <h3>Submit Research Question or Finding</h3>
                <input type="text" id="title" placeholder="Title or brief description" style="width: 100%; padding: 8px; margin: 5px 0;">
                <textarea id="content" placeholder="Detailed research question, finding, or concern for council review..."></textarea>
                <select id="priority" style="padding: 8px; margin: 5px 0;">
                    <option value="normal">Normal Priority</option>
                    <option value="high">High Priority</option>
                    <option value="urgent">Urgent</option>
                </select>
                <div id="selected-domain" style="margin: 10px 0; font-weight: bold;"></div>
                <button id="submit-btn" disabled onclick="submitResearch()">Select Domain First</button>
            </div>
            
            <script>
                let selectedDomain = null;
                
                function submitTo(domain) {
                    selectedDomain = domain;
                    document.getElementById('selected-domain').textContent = `Selected: ${domain.charAt(0).toUpperCase() + domain.slice(1)} Council`;
                    document.getElementById('submit-btn').textContent = `Submit to ${domain.charAt(0).toUpperCase() + domain.slice(1)} Council`;
                    document.getElementById('submit-btn').disabled = false;
                }
                
                function submitResearch() {
                    if (!selectedDomain) return;
                    
                    const title = document.getElementById('title').value;
                    const content = document.getElementById('content').value;
                    const priority = document.getElementById('priority').value;
                    
                    if (!content.trim()) {
                        alert('Please enter your research question or finding');
                        return;
                    }
                    
                    const submission = {
                        title: title || 'Untitled Submission',
                        content: content,
                        priority: priority
                    };
                    
                    fetch(`/council/${selectedDomain}`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(submission)
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert(`Submission received! ID: ${data.submission_id}\\n\\nYour research question has been forwarded to the ${selectedDomain} council for review.`);
                        document.getElementById('title').value = '';
                        document.getElementById('content').value = '';
                        selectedDomain = null;
                        document.getElementById('selected-domain').textContent = '';
                        document.getElementById('submit-btn').textContent = 'Select Domain First';
                        document.getElementById('submit-btn').disabled = true;
                    })
                    .catch(error => {
                        alert('Error submitting research: ' + error);
                    });
                }
            </script>
        </body>
        </html>
        """

def main():
    """Start the Research Council Server"""
    PORT = 8080
    
    print("🏛️ AI Research Council Server")
    print("=" * 50)
    print(f"Starting server on port {PORT}")
    print("\nAvailable Council Domains:")
    
    handler = ResearchCouncilHandler
    for domain, info in handler.RESEARCH_DOMAINS.items():
        print(f"  • {domain.upper()}: {info['description']}")
    
    print(f"\nAccess dashboard: http://localhost:{PORT}")
    print("Press Ctrl+C to stop server")
    print("=" * 50)
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Research Council Server stopped")

if __name__ == "__main__":
    main()