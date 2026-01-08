#!/usr/bin/env python3
"""
Password Strength Checker (CLI) - WINDOWS FIXED VERSION
"""

import sys
import re
import argparse
import getpass
import math
from typing import Tuple

class PasswordStrengthChecker:
    def __init__(self):
        self.common_passwords = {
            'password', '123456', '123456789', '12345678', '12345', 'qwerty',
            'abc123', 'password', '111111', 'admin', 'letmein', 'welcome',
            'monkey', 'dragon', 'master', 'sunshine', 'ashley', 'football',
            'paper', 'nicole', 'ginger', 'cheese', 'princess', 'jordan',
            'taylor', 'shadow', 'robert', 'thomas', 'lakers', 'michael',
            'jennifer', 'hunter', 'buster', 'soccer', 'harley', 'batman',
            'superman', 'iloveyou', 'trustno1', 'ninja', 'abcde'
        }
    
    def calculate_entropy(self, password: str) -> float:
        """Calculate password entropy in bits - FIXED."""
        if not password:
            return 0
        
        charset_count = 0
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_symbol = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'"\\|,.<>/?`~]', password))
        
        if has_lower: charset_count += 26
        if has_upper: charset_count += 26
        if has_digit: charset_count += 10
        if has_symbol: charset_count += 32
        
        if charset_count == 0:
            return 0
        
        return len(password) * math.log2(max(26, charset_count))
    
    def check_criteria(self, password: str) -> dict:
        checks = {
            'length': len(password) >= 12,
            'lowercase': bool(re.search(r'[a-z]', password)),
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'digits': bool(re.search(r'\d', password)),
            'symbols': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'"\\|,.<>/?`~]', password)),
            'no_username': not re.search(r'(user|admin|root|test)', password, re.IGNORECASE),
            'no_common': password.lower() not in self.common_passwords,
            'no_keyboard_patterns': not self._has_keyboard_pattern(password),
            'no_repetitions': not self._has_repetitions(password),
            'no_sequential': not self._has_sequential(password)
        }
        return checks
    
    def _has_keyboard_pattern(self, password: str) -> bool:
        keyboard_patterns = [r'qwertyuiop', r'asdfghjkl', r'zxcvbnm', r'1234567890']
        return any(re.search(pattern, password.lower()) for pattern in keyboard_patterns)
    
    def _has_repetitions(self, password: str) -> bool:
        for i in range(len(password) - 3):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False
    
    def _has_sequential(self, password: str) -> bool:
        seq_patterns = [r'123', r'abc', r'xyz', r'456', r'789', r'012']
        return any(re.search(pattern, password.lower()) for pattern in seq_patterns)
    
    def _generate_bar(self, score: int) -> str:
        filled = "█" * (score // 4)
        empty = "░" * max(0, 25 - len(filled))
        return f"[{filled}{empty}] {score}%"
    
    def get_strength_score(self, password: str) -> Tuple[str, int, str]:
        if not password:
            return "Empty", 0, "No password provided"
        
        checks = self.check_criteria(password)
        passed = sum(checks.values())
        
        entropy = self.calculate_entropy(password)
        entropy_score = min(40, entropy / 8)
        criteria_score = (passed / 10) * 40
        length_score = min(20, (len(password) / 20) * 20)
        
        total_score = int(entropy_score + criteria_score + length_score)
        
        if total_score >= 90: rating, color = "Very Strong", "\033[92m"
        elif total_score >= 75: rating, color = "Strong", "\033[92m"
        elif total_score >= 60: rating, color = "Good", "\033[93m"
        elif total_score >= 40: rating, color = "Weak", "\033[93m"
        else: rating, color = "Very Weak", "\033[91m"
        
        reset = "\033[0m"
        bar = self._generate_bar(total_score)
        message = f"{total_score}/100 | {passed}/10 checks"
        if password.lower() in self.common_passwords:
            message += " | COMMON - DO NOT USE!"
        
        return rating, total_score, f"{color}{bar} {message}{reset}"
    
    def detailed_report(self, password: str):
        print("\n" + "="*50)
        print("DETAILED ANALYSIS")
        print("="*50)
        checks = self.check_criteria(password)
        entropy = self.calculate_entropy(password)
        print(f"Length: {len(password)} chars | Entropy: {entropy:.1f} bits")
        print("\nCHECKLIST:")
        names = {
            'length': '12+ chars ✓', 'lowercase': 'Lowercase ✓', 'uppercase': 'Uppercase ✓',
            'digits': 'Numbers ✓', 'symbols': 'Symbols ✓', 'no_username': 'No username words ✓',
            'no_common': 'Not common ✓', 'no_keyboard_patterns': 'No patterns ✓',
            'no_repetitions': 'No repeats ✓', 'no_sequential': 'No sequences ✓'
        }
        passed = 0
        for key, value in checks.items():
            status = "✓" if value else "✗"
            print(f"  {status} {names[key]}")
            if value: passed += 1
        print(f"\n{passed}/10 criteria passed ✓")
    
    def analyze(self, password: str):
        rating, score, strength = self.get_strength_score(password)
        print(f"\n{rating}")
        print(strength)
        if score < 75:
            print("\n💡 IMPROVE:")
            checks = self.check_criteria(password)
            if len(password) < 12: print("  • 12+ characters")
            if not re.search(r'[a-z]', password): print("  • Lowercase (a-z)")
            if not re.search(r'[A-Z]', password): print("  • Uppercase (A-Z)")
            if not re.search(r'\d', password): print("  • Numbers (0-9)")
            if not re.search(r'[!@#$%^&*]', password): print("  • Symbols (!@#$%)")
        self.detailed_report(password)

def main():
    parser = argparse.ArgumentParser(description="Password Strength Checker")
    parser.add_argument("password", nargs="?", help="Password")
    parser.add_argument("-i", "--interactive", action="store_true")
    parser.add_argument("-b", "--batch", type=argparse.FileType('r'))
    args = parser.parse_args()
    checker = PasswordStrengthChecker()
    
    if args.batch:
        print("BATCH MODE:")
        for i, line in enumerate(args.batch, 1):
            pw = line.strip()
            if pw: 
                print(f"\n{i}. {pw}", end='')
                checker.analyze(pw)
        return
    
    if args.interactive:
        print("Password Checker (Ctrl+C to exit)")
        print("-" * 35)
        try:
            while True:
                pw = getpass.getpass("Password: ")
                checker.analyze(pw)
                print()
        except KeyboardInterrupt:
            print("\nBye!")
        return
    
    pw = args.password or getpass.getpass("Password: ")
    checker.analyze(pw)

if __name__ == "__main__":
    main()