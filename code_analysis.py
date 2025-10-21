#!/usr/bin/env python3
"""
Complete Code Analysis - Trading MVP
"""
import os
import sys
from pathlib import Path
import subprocess

class CodeAnalyzer:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.issues = []
        self.improvements = []
        self.excellent_practices = []
    
    def analyze_all(self):
        """Perform complete code analysis."""
        print("=" * 80)
        print("🔍 COMPLETE CODE ANALYSIS - TRADING MVP")
        print("=" * 80)
        
        self.check_structure()
        self.check_imports()
        self.check_naming()
        self.check_documentation()
        self.check_security()
        self.check_performance()
        self.check_testing()
        self.check_dependencies()
        
        self.generate_report()
    
    def check_structure(self):
        """Check folder structure."""
        print("\n📁 STRUCTURE ANALYSIS:")
        
        required_dirs = [
            "trading-intelligence",
            "trading-executor", 
            "trading-dashboard",
            "config"
        ]
        
        for dir_name in required_dirs:
            if (self.base_dir / dir_name).exists():
                print(f"   ✅ {dir_name}/ present")
                self.excellent_practices.append(f"Well-organized structure: {dir_name}/")
            else:
                print(f"   ❌ {dir_name}/ missing")
                self.issues.append(f"Required folder missing: {dir_name}/")
        
        # Check Clean Architecture in trading-intelligence
        clean_arch_dirs = ["domain", "application", "infrastructure", "presentation"]
        ti_app = self.base_dir / "trading-intelligence" / "app"
        
        if ti_app.exists():
            for arch_dir in clean_arch_dirs:
                if (ti_app / arch_dir).exists():
                    print(f"   ✅ Clean Architecture: app/{arch_dir}/")
                    self.excellent_practices.append(f"Clean Architecture implemented: {arch_dir}")
                else:
                    self.issues.append(f"Clean Architecture layer missing: {arch_dir}")
    
    def check_imports(self):
        """Check import issues."""
        print("\n📥 IMPORT ANALYSIS:")
        
        # Check files that may have outdated imports
        files_to_check = [
            "test_clean_architecture.py",
            "start_clean_api.py", 
            "run_realtime.py"
        ]
        
        for file_name in files_to_check:
            file_path = self.base_dir / file_name
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                
                # Check old imports
                if "python.app" in content:
                    print(f"   ⚠️ {file_name}: outdated imports found")
                    self.issues.append(f"{file_name}: contains obsolete 'python.app' imports")
                else:
                    print(f"   ✅ {file_name}: imports updated")
                    
                if "dotnet/TradingExecutor" in content:
                    print(f"   ⚠️ {file_name}: old dotnet references")
                    self.issues.append(f"{file_name}: contains obsolete 'dotnet/TradingExecutor' references")
    
    def check_naming(self):
        """Check naming conventions."""
        print("\n🏷️ NAMING ANALYSIS:")
        
        # Check if all names follow Domain-Driven Design
        domain_names = [
            ("trading-intelligence", "Trading Intelligence (AI/ML)"),
            ("trading-executor", "Order Executor (.NET)"),
            ("trading-dashboard", "Monitoring Dashboard")
        ]
        
        for folder, description in domain_names:
            if (self.base_dir / folder).exists():
                print(f"   ✅ {folder}: {description}")
                self.excellent_practices.append(f"Domain-based naming: {folder}")
            else:
                self.issues.append(f"Domain-named folder missing: {folder}")
    
    def check_documentation(self):
        """Check documentation quality."""
        print("\n📚 DOCUMENTATION ANALYSIS:")
        
        docs = ["README.md", "SETUP_GUIDE.md", "REFACTORING_LOG.md"]
        
        for doc in docs:
            if (self.base_dir / doc).exists():
                size = (self.base_dir / doc).stat().st_size
                if size > 1000:  # More than 1KB indicates substantial documentation
                    print(f"   ✅ {doc}: comprehensive documentation ({size:,} bytes)")
                    self.excellent_practices.append(f"Complete documentation: {doc}")
                else:
                    print(f"   ⚠️ {doc}: documentation too short")
                    self.improvements.append(f"Expand documentation in {doc}")
            else:
                self.issues.append(f"Documentation missing: {doc}")
    
    def check_security(self):
        """Check security aspects."""
        print("\n🔒 SECURITY ANALYSIS:")
        
        # Check if .gitignore is protecting sensitive files
        gitignore = self.base_dir / ".gitignore"
        if gitignore.exists():
            content = gitignore.read_text()
            
            security_items = [
                (".env", "Environment variables"),
                ("*.key", "Key files"),
                ("*.pem", "Certificates"),
                ("artifacts/", "ML models"),
                (".venv/", "Virtual environment")
            ]
            
            for pattern, description in security_items:
                if pattern in content:
                    print(f"   ✅ Protected: {description}")
                    self.excellent_practices.append(f"Security: {description} protected")
                else:
                    print(f"   ⚠️ Not protected: {description}")
                    self.improvements.append(f"Add {pattern} to .gitignore")
    
    def check_performance(self):
        """Check performance aspects."""
        print("\n⚡ PERFORMANCE ANALYSIS:")
        
        # Check async/await usage
        async_files = []
        
        for py_file in self.base_dir.glob("**/*.py"):
            if py_file.is_file():
                try:
                    content = py_file.read_text(encoding='utf-8')
                    if "async def" in content:
                        async_files.append(py_file.name)
                except:
                    pass
        
        if async_files:
            print(f"   ✅ Asynchronous programming implemented in {len(async_files)} files")
            self.excellent_practices.append("Use of async/await for performance")
        else:
            self.improvements.append("Consider implementing asynchronous programming")
    
    def check_testing(self):
        """Check test coverage."""
        print("\n🧪 TESTING ANALYSIS:")
        
        test_files = list(self.base_dir.glob("test_*.py"))
        
        if test_files:
            print(f"   ✅ {len(test_files)} test files found")
            for test_file in test_files:
                print(f"      - {test_file.name}")
                self.excellent_practices.append(f"Test implemented: {test_file.name}")
        else:
            self.issues.append("No test files found")
            
        # Check if tests are updated
        for test_file in test_files:
            content = test_file.read_text(encoding='utf-8')
            if "python.app" in content:
                self.issues.append(f"{test_file.name}: outdated test imports")
    
    def check_dependencies(self):
        """Check dependency management."""
        print("\n📦 DEPENDENCY ANALYSIS:")
        
        # Python dependencies
        req_file = self.base_dir / "trading-intelligence" / "requirements.txt"
        if req_file.exists():
            print("   ✅ requirements.txt present")
            self.excellent_practices.append("Python dependency management")
        else:
            self.issues.append("requirements.txt missing")
            
        # .NET dependencies  
        csproj_files = list(self.base_dir.glob("**/*.csproj"))
        if csproj_files:
            print(f"   ✅ {len(csproj_files)} .NET project(s) found")
            self.excellent_practices.append(".NET dependency management")
        else:
            self.issues.append("No .NET projects found")
            
        # Node.js dependencies
        package_json = self.base_dir / "trading-dashboard" / "package.json"
        if package_json.exists():
            print("   ✅ package.json present")
            self.excellent_practices.append("Node.js dependency management")
        else:
            self.improvements.append("Check dashboard package.json")
    
    def generate_report(self):
        """Generate final report."""
        print("\n" + "=" * 80)
        print("📊 FINAL ANALYSIS REPORT")
        print("=" * 80)
        
        # Statistics
        total_issues = len(self.issues)
        total_improvements = len(self.improvements)
        total_excellent = len(self.excellent_practices)
        
        print(f"\n📈 STATISTICS:")
        print(f"   🏆 Excellent practices: {total_excellent}")
        print(f"   ⚠️ Issues found: {total_issues}")
        print(f"   💡 Suggested improvements: {total_improvements}")
        
        # Quality score
        total_items = total_issues + total_improvements + total_excellent
        if total_items > 0:
            quality_score = (total_excellent / total_items) * 100
            print(f"   🎯 Quality Score: {quality_score:.1f}%")
        
        # Issue details
        if self.issues:
            print(f"\n❌ CRITICAL ISSUES ({len(self.issues)}):")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")
        
        # Improvement details
        if self.improvements:
            print(f"\n💡 SUGGESTED IMPROVEMENTS ({len(self.improvements)}):")
            for i, improvement in enumerate(self.improvements, 1):
                print(f"   {i}. {improvement}")
        
        # Excellent practices
        if self.excellent_practices:
            print(f"\n🏆 EXCELLENT PRACTICES ({len(self.excellent_practices)}):")
            for i, practice in enumerate(self.excellent_practices, 1):
                print(f"   {i}. {practice}")
        
        # Final recommendations
        print(f"\n🎯 FINAL RECOMMENDATIONS:")
        if total_issues == 0:
            print("   ✅ Code is in excellent condition! Congratulations!")
        elif total_issues <= 3:
            print("   👍 Code is in good condition, few adjustments needed")
        elif total_issues <= 7:
            print("   ⚠️ Code needs some important adjustments")
        else:
            print("   🚨 Code needs significant review")
            
        print("\n" + "=" * 80)

if __name__ == "__main__":
    analyzer = CodeAnalyzer()
    analyzer.analyze_all()