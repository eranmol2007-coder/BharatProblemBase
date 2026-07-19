#!/usr/bin/env python3
"""
Bug Condition Exploration Test - Deployment Infrastructure Verification

**Validates: Requirements 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5**

This test verifies that deployment infrastructure components exist.
This test MUST FAIL on the current unfixed code to confirm the bug exists.

Property 1: Bug Condition - Deployment Infrastructure Verification
"""

import os
import json
import sys
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent

class DeploymentInfrastructureTest:
    def __init__(self):
        self.failures = []
        self.passes = []
        
    def log_pass(self, message):
        """Log a passing test"""
        self.passes.append(f"✓ PASS: {message}")
        print(f"✓ PASS: {message}")
        
    def log_fail(self, message):
        """Log a failing test"""
        self.failures.append(f"✗ FAIL: {message}")
        print(f"✗ FAIL: {message}")
        
    def test_github_actions_workflow_exists(self):
        """Test 1: Check if GitHub Actions workflow file exists"""
        workflow_path = PROJECT_ROOT / ".github" / "workflows" / "deploy.yml"
        
        if not workflow_path.exists():
            self.log_fail("GitHub Actions workflow not found at .github/workflows/deploy.yml")
            return False
            
        self.log_pass("GitHub Actions workflow file exists")
        return True
        
    def test_workflow_contains_required_steps(self):
        """Test 2: Check if workflow contains required Vercel deployment steps"""
        workflow_path = PROJECT_ROOT / ".github" / "workflows" / "deploy.yml"
        
        if not workflow_path.exists():
            self.log_fail("Cannot verify workflow steps - file doesn't exist")
            return False
            
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
            # Check for required elements
            checks = {
                "push trigger": "push" in content and "main" in content,
                "frontend build": ("npm install" in content or "npm ci" in content) and "npm run build" in content,
                "vercel deployment": "vercel" in content and ("prod" in content or "production" in content),
            }
            
            all_passed = True
            for check_name, passed in checks.items():
                if not passed:
                    self.log_fail(f"Workflow missing required step: {check_name}")
                    all_passed = False
                    
            if all_passed:
                self.log_pass("Workflow contains all required deployment steps")
                
            return all_passed
            
        except Exception as e:
            self.log_fail(f"Error reading workflow file: {e}")
            return False
            
    def test_vercel_json_configuration(self):
        """Test 3: Check if vercel.json contains frontend build configuration"""
        vercel_config_path = PROJECT_ROOT / "vercel.json"
        
        if not vercel_config_path.exists():
            self.log_fail("vercel.json file not found")
            return False
            
        try:
            with open(vercel_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # Check for build configuration
            has_build_command = False
            
            # Check in buildCommand field
            if "buildCommand" in config:
                build_cmd = config["buildCommand"].lower()
                if "npm" in build_cmd and "build" in build_cmd:
                    has_build_command = True
                    
            # Check in builds array
            if "builds" in config:
                for build in config["builds"]:
                    if "frontend" in str(build.get("src", "")).lower():
                        # Frontend static build is configured
                        pass
                        
            # Verify API routing
            has_api_routing = False
            if "routes" in config:
                for route in config["routes"]:
                    if route.get("src", "").startswith("/api"):
                        has_api_routing = True
                        break
                        
            if not has_build_command:
                self.log_fail("vercel.json missing explicit frontend buildCommand")
                return False
                
            if not has_api_routing:
                self.log_fail("vercel.json missing API routing configuration")
                return False
                
            self.log_pass("vercel.json contains proper configuration")
            return True
            
        except json.JSONDecodeError as e:
            self.log_fail(f"vercel.json is not valid JSON: {e}")
            return False
        except Exception as e:
            self.log_fail(f"Error reading vercel.json: {e}")
            return False
            
    def test_vercelignore_exists(self):
        """Test 4: Check if .vercelignore file exists"""
        vercelignore_path = PROJECT_ROOT / ".vercelignore"
        
        if not vercelignore_path.exists():
            self.log_fail(".vercelignore file not found")
            return False
            
        try:
            with open(vercelignore_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for important patterns
            required_patterns = [".venv", "node_modules", "__pycache__"]
            missing_patterns = []
            
            for pattern in required_patterns:
                if pattern not in content:
                    missing_patterns.append(pattern)
                    
            if missing_patterns:
                self.log_fail(f".vercelignore missing patterns: {', '.join(missing_patterns)}")
                return False
                
            self.log_pass(".vercelignore file exists with correct patterns")
            return True
            
        except Exception as e:
            self.log_fail(f"Error reading .vercelignore: {e}")
            return False
            
    def test_readme_has_production_url(self):
        """Test 5: Check if README.md contains production URL section"""
        readme_path = PROJECT_ROOT / "README.md"
        
        if not readme_path.exists():
            self.log_fail("README.md file not found")
            return False
            
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
            # Check for production URL indicators
            has_production_url = False
            
            # Look for vercel URL patterns
            if "vercel.app" in content:
                has_production_url = True
                
            # Look for production/deployment sections
            if "production" in content or "deployment" in content or "live site" in content:
                # Check if it's just localhost
                if "localhost" not in content or "vercel" in content or "https://" in content:
                    has_production_url = True
                    
            if not has_production_url:
                self.log_fail("README.md missing production URL section (only shows localhost:8000)")
                return False
                
            self.log_pass("README.md contains production URL information")
            return True
            
        except Exception as e:
            self.log_fail(f"Error reading README.md: {e}")
            return False
            
    def run_all_tests(self):
        """Run all deployment infrastructure tests"""
        print("=" * 70)
        print("Bug Condition Exploration Test - Deployment Infrastructure")
        print("=" * 70)
        print()
        print("This test verifies deployment infrastructure components exist.")
        print("Expected: This test SHOULD FAIL on unfixed code.")
        print()
        print("-" * 70)
        
        # Run all tests
        self.test_github_actions_workflow_exists()
        self.test_workflow_contains_required_steps()
        self.test_vercel_json_configuration()
        self.test_vercelignore_exists()
        self.test_readme_has_production_url()
        
        # Print summary
        print()
        print("=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Passed: {len(self.passes)}")
        print(f"Failed: {len(self.failures)}")
        print()
        
        if self.failures:
            print("FAILED CHECKS (Missing Infrastructure Components):")
            for failure in self.failures:
                print(f"  {failure}")
            print()
            print("RESULT: ✗ BUG CONFIRMED - Deployment infrastructure is incomplete")
            print("These failures demonstrate that the deployment system is not properly configured.")
            return False
        else:
            print("RESULT: ✓ All deployment infrastructure components exist")
            print("This indicates the deployment system is properly configured.")
            return True

def main():
    """Main entry point"""
    tester = DeploymentInfrastructureTest()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
