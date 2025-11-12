#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

def deploy_site(lead_name, template_html, customizations):
    """Deploy a personalized demo site"""
    
    # Sanitize name
    subdomain = lead_name.lower().replace(' ', '-').replace('_', '-')
    subdomain = ''.join(c for c in subdomain if c.isalnum() or c == '-')
    site_name = f"demo-{subdomain}"
    
    # Create site directory
    site_path = Path(f"sites/{site_name}")
    site_path.mkdir(parents=True, exist_ok=True)
    
    # Personalize HTML
    html = template_html
    for key, value in customizations.items():
        html = html.replace(f"{{{{{key}}}}}", str(value))
    
    # Write files
    (site_path / "index.html").write_text(html)
    
    # Create metadata
    metadata = {
        "deployed": datetime.utcnow().isoformat() + "Z",
        "subdomain": site_name,
        "lead": lead_name,
        "customizations": customizations
    }
    (site_path / "deployed.json").write_text(json.dumps(metadata, indent=2))
    
    # Git commit
    subprocess.run(["git", "add", str(site_path)])
    subprocess.run(["git", "commit", "-m", f"Deploy demo for {lead_name}"])
    subprocess.run(["git", "push"])
    
    return site_name

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy_site.py 'Lead Name'")
        sys.exit(1)
    
    # Load template
    template = Path("template.html").read_text()
    
    # Deploy
    site = deploy_site(
        lead_name=sys.argv[1],
        template_html=template,
        customizations={
            "company_name": sys.argv[1],
            "industry": sys.argv[2] if len(sys.argv) > 2 else "your industry"
        }
    )
    
    print(f"✅ Deployed: https://[DOMAIN]/{site}")
