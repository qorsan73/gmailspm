#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import smtplib
import csv
import time
import random
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import getpass

class GhostMailer:
    def __init__(self):
        print("""
╔══════════════════════════════════════╗
║     GHOST MAILER - GMAIL EDITION     ║
║      Stealth Protocol: ACTIVE        ║
╚══════════════════════════════════════╝
        """)
        
        # Configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.recipients_file = ""
        self.sender_email = ""
        self.sender_password = ""
        self.subject = ""
        self.message_body = ""
        self.recipients = []
        
        # Stealth parameters
        self.min_delay = 5  # seconds
        self.max_delay = 15  # seconds
        self.batch_size = 10  # send in small batches
        
        self.initialize()
    
    def initialize(self):
        """Gather all required intel"""
        print("[+] Phase 1: Target Acquisition")
        
        # Get recipients file
        while True:
            self.recipients_file = input("[?] Enter CSV file path: ").strip()
            if os.path.exists(self.recipients_file):
                break
            print("[!] File not found. Try again.")
        
        # Get sender credentials
        self.sender_email = input("[?] Enter your Gmail address: ").strip()
        self.sender_password = getpass.getpass("[?] Enter your Gmail password/app password: ")
        
        # Get message details
        self.subject = input("[?] Enter email subject: ").strip()
        print("[?] Enter message body (end with 'END' on a new line):")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        self.message_body = "\n".join(lines)
        
        # Load targets
        self.load_recipients()
        
        # Confirm mission
        print(f"\n[+] Targets loaded: {len(self.recipients)}")
        print(f"[+] Subject: {self.subject}")
        print(f"[+] Message length: {len(self.message_body)} characters")
        
        confirm = input("\n[?] Launch sequence? (y/n): ").strip().lower()
        if confirm != 'y':
            print("[!] Mission aborted.")
            sys.exit(0)
        
        self.execute()
    
    def load_recipients(self):
        """Extract targets from CSV"""
        try:
            with open(self.recipients_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                # Skip header if exists
                try:
                    # Try to detect header
                    first_row = next(reader)
                    # Check if first cell looks like email
                    if '@' in first_row[0]:
                        self.recipients.append(first_row[0].strip())
                    # Add the rest
                    for row in reader:
                        if row and row[0].strip():
                            self.recipients.append(row[0].strip())
                except StopIteration:
                    pass
            
            # Deduplicate
            self.recipients = list(set(self.recipients))
            print(f"[+] Unique targets identified: {len(self.recipients)}")
            
        except Exception as e:
            print(f"[!] CSV extraction failed: {e}")
            sys.exit(1)
    
    def craft_message(self, recipient):
        """Forge untraceable message"""
        msg = MIMEMultipart('alternative')
        
        # Stealth headers - mimic legitimate mail
        msg['From'] = self.sender_email
        msg['To'] = recipient
        msg['Subject'] = Header(self.subject, 'utf-8')
        msg['X-Priority'] = '3'  # Normal priority
        msg['X-Mailer'] = 'Microsoft Outlook 16.0'
        msg['MIME-Version'] = '1.0'
        
        # Plain text version (for inbox placement)
        text_part = MIMEText(self.message_body, 'plain', 'utf-8')
        msg.attach(text_part)
        
        return msg
    
    def execute(self):
        """Begin covert operation"""
        print("\n[+] Phase 2: Stealth Transmission Initiated")
        print(f"[+] Using SMTP: {self.smtp_server}:{self.smtp_port}")
        print("[+] Evasion protocols: ACTIVE")
        print("─" * 50)
        
        successful = 0
        failed = 0
        
        try:
            # Establish secure connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Upgrade to secure connection
            server.login(self.sender_email, self.sender_password)
            
            print("[✓] Secure tunnel established")
            
            # Send in small batches with random delays
            for i, recipient in enumerate(self.recipients, 1):
                try:
                    # Craft unique message for each recipient
                    msg = self.craft_message(recipient)
                    
                    # Send
                    server.sendmail(self.sender_email, recipient, msg.as_string())
                    
                    print(f"[{i}/{len(self.recipients)}] ✓ Sent to: {recipient}")
                    successful += 1
                    
                    # Stealth delay (except for last email)
                    if i < len(self.recipients):
                        delay = random.randint(self.min_delay, self.max_delay)
                        print(f"    [⏱] Cooling down for {delay}s...")
                        time.sleep(delay)
                    
                    # Small batch pause every 10 emails
                    if i % self.batch_size == 0 and i < len(self.recipients):
                        long_delay = random.randint(30, 60)
                        print(f"    [🛡] Batch complete. Deep stealth: {long_delay}s")
                        time.sleep(long_delay)
                        
                except Exception as e:
                    print(f"[{i}/{len(self.recipients)}] ✗ Failed: {recipient} | Error: {str(e)[:50]}")
                    failed += 1
                    
                    # Longer delay on failure
                    time.sleep(random.randint(20, 30))
            
            # Mission complete
            server.quit()
            
            print("\n" + "═" * 50)
            print("[✓] MISSION ACCOMPLISHED")
            print(f"[+] Successful deliveries: {successful}")
            print(f"[+] Failed targets: {failed}")
            print(f"[+] Evasion rate: {(successful/len(self.recipients))*100:.1f}%")
            
            # Save report
            self.generate_report(successful, failed)
            
        except Exception as e:
            print(f"[!] Critical failure: {e}")
            sys.exit(1)
    
    def generate_report(self, success, failed):
        """Create mission debrief"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        report_file = f"mail_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("GHOST MAILER - MISSION DEBRIEF\n")
            f.write("=" * 40 + "\n")
            f.write(f"Timestamp: {time.ctime()}\n")
            f.write(f"Sender: {self.sender_email}\n")
            f.write(f"Targets: {len(self.recipients)}\n")
            f.write(f"Successful: {success}\n")
            f.write(f"Failed: {failed}\n")
            f.write(f"Subject: {self.subject}\n")
            f.write("\nRecipients:\n")
            for recipient in self.recipients:
                f.write(f"  - {recipient}\n")
        
        print(f"[+] Debrief saved to: {report_file}")

if __name__ == "__main__":
    # Check for required modules
    try:
        import smtplib, csv
    except ImportError as e:
        print(f"[!] Missing module: {e}")
        print("[!] Install with: pip install secure-smtplib")
        sys.exit(1)
    
    # Launch
    try:
        GhostMailer()
    except KeyboardInterrupt:
        print("\n[!] Mission terminated by user.")
    except Exception as e:
        print(f"[!] Fatal error: {e}")
