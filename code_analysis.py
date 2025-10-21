#!/usr/bin/env python3
"""
Análise Completa do Código - Trading MVP
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
        """Realizar análise completa do código."""
        print("=" * 80)
        print("🔍 ANÁLISE COMPLETA DO CÓDIGO - TRADING MVP")
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
        """Verificar estrutura de pastas."""
        print("\n📁 ANÁLISE DE ESTRUTURA:")
        
        required_dirs = [
            "trading-intelligence",
            "trading-executor", 
            "trading-dashboard",
            "config"
        ]
        
        for dir_name in required_dirs:
            if (self.base_dir / dir_name).exists():
                print(f"   ✅ {dir_name}/ presente")
                self.excellent_practices.append(f"Estrutura bem organizada: {dir_name}/")
            else:
                print(f"   ❌ {dir_name}/ ausente")
                self.issues.append(f"Pasta obrigatória ausente: {dir_name}/")
        
        # Verificar Clean Architecture no trading-intelligence
        clean_arch_dirs = ["domain", "application", "infrastructure", "presentation"]
        ti_app = self.base_dir / "trading-intelligence" / "app"
        
        if ti_app.exists():
            for arch_dir in clean_arch_dirs:
                if (ti_app / arch_dir).exists():
                    print(f"   ✅ Clean Architecture: app/{arch_dir}/")
                    self.excellent_practices.append(f"Clean Architecture implementada: {arch_dir}")
                else:
                    self.issues.append(f"Camada Clean Architecture ausente: {arch_dir}")
    
    def check_imports(self):
        """Verificar problemas de imports."""
        print("\n📥 ANÁLISE DE IMPORTS:")
        
        # Verificar arquivos que podem ter imports desatualizados
        files_to_check = [
            "test_clean_architecture.py",
            "start_clean_api.py", 
            "run_realtime.py"
        ]
        
        for file_name in files_to_check:
            file_path = self.base_dir / file_name
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                
                # Verificar imports antigos
                if "python.app" in content:
                    print(f"   ⚠️ {file_name}: imports desatualizados encontrados")
                    self.issues.append(f"{file_name}: contém imports 'python.app' obsoletos")
                else:
                    print(f"   ✅ {file_name}: imports atualizados")
                    
                if "dotnet/TradingExecutor" in content:
                    print(f"   ⚠️ {file_name}: referências antigas ao dotnet")
                    self.issues.append(f"{file_name}: contém referências 'dotnet/TradingExecutor' obsoletas")
    
    def check_naming(self):
        """Verificar convenções de nomenclatura."""
        print("\n🏷️ ANÁLISE DE NOMENCLATURA:")
        
        # Verificar se todos os nomes seguem Domain-Driven Design
        domain_names = [
            ("trading-intelligence", "Inteligência de Trading (IA/ML)"),
            ("trading-executor", "Executor de Ordens (.NET)"),
            ("trading-dashboard", "Dashboard de Monitoramento")
        ]
        
        for folder, description in domain_names:
            if (self.base_dir / folder).exists():
                print(f"   ✅ {folder}: {description}")
                self.excellent_practices.append(f"Nomenclatura baseada em domínio: {folder}")
            else:
                self.issues.append(f"Pasta com nomenclatura de domínio ausente: {folder}")
    
    def check_documentation(self):
        """Verificar qualidade da documentação."""
        print("\n📚 ANÁLISE DE DOCUMENTAÇÃO:")
        
        docs = ["README.md", "SETUP_GUIDE.md", "REFACTORING_LOG.md"]
        
        for doc in docs:
            if (self.base_dir / doc).exists():
                size = (self.base_dir / doc).stat().st_size
                if size > 1000:  # Mais de 1KB indica documentação substancial
                    print(f"   ✅ {doc}: documentação abrangente ({size:,} bytes)")
                    self.excellent_practices.append(f"Documentação completa: {doc}")
                else:
                    print(f"   ⚠️ {doc}: documentação muito curta")
                    self.improvements.append(f"Expandir documentação em {doc}")
            else:
                self.issues.append(f"Documentação ausente: {doc}")
    
    def check_security(self):
        """Verificar aspectos de segurança."""
        print("\n🔒 ANÁLISE DE SEGURANÇA:")
        
        # Verificar se .gitignore está protegendo arquivos sensíveis
        gitignore = self.base_dir / ".gitignore"
        if gitignore.exists():
            content = gitignore.read_text()
            
            security_items = [
                (".env", "Variáveis de ambiente"),
                ("*.key", "Arquivos de chave"),
                ("*.pem", "Certificados"),
                ("artifacts/", "Modelos ML"),
                (".venv/", "Ambiente virtual")
            ]
            
            for pattern, description in security_items:
                if pattern in content:
                    print(f"   ✅ Protegido: {description}")
                    self.excellent_practices.append(f"Segurança: {description} protegido")
                else:
                    print(f"   ⚠️ Não protegido: {description}")
                    self.improvements.append(f"Adicionar {pattern} ao .gitignore")
    
    def check_performance(self):
        """Verificar aspectos de performance."""
        print("\n⚡ ANÁLISE DE PERFORMANCE:")
        
        # Verificar uso de async/await
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
            print(f"   ✅ Programação assíncrona implementada em {len(async_files)} arquivos")
            self.excellent_practices.append("Uso de async/await para performance")
        else:
            self.improvements.append("Considerar implementar programação assíncrona")
    
    def check_testing(self):
        """Verificar cobertura de testes."""
        print("\n🧪 ANÁLISE DE TESTES:")
        
        test_files = list(self.base_dir.glob("test_*.py"))
        
        if test_files:
            print(f"   ✅ {len(test_files)} arquivos de teste encontrados")
            for test_file in test_files:
                print(f"      - {test_file.name}")
                self.excellent_practices.append(f"Teste implementado: {test_file.name}")
        else:
            self.issues.append("Nenhum arquivo de teste encontrado")
            
        # Verificar se tests estão atualizados
        for test_file in test_files:
            content = test_file.read_text(encoding='utf-8')
            if "python.app" in content:
                self.issues.append(f"{test_file.name}: imports de teste desatualizados")
    
    def check_dependencies(self):
        """Verificar gestão de dependências."""
        print("\n📦 ANÁLISE DE DEPENDÊNCIAS:")
        
        # Python dependencies
        req_file = self.base_dir / "trading-intelligence" / "requirements.txt"
        if req_file.exists():
            print("   ✅ requirements.txt presente")
            self.excellent_practices.append("Gestão de dependências Python")
        else:
            self.issues.append("requirements.txt ausente")
            
        # .NET dependencies  
        csproj_files = list(self.base_dir.glob("**/*.csproj"))
        if csproj_files:
            print(f"   ✅ {len(csproj_files)} projeto(s) .NET encontrados")
            self.excellent_practices.append("Gestão de dependências .NET")
        else:
            self.issues.append("Nenhum projeto .NET encontrado")
            
        # Node.js dependencies
        package_json = self.base_dir / "trading-dashboard" / "package.json"
        if package_json.exists():
            print("   ✅ package.json presente")
            self.excellent_practices.append("Gestão de dependências Node.js")
        else:
            self.improvements.append("Verificar package.json do dashboard")
    
    def generate_report(self):
        """Gerar relatório final."""
        print("\n" + "=" * 80)
        print("📊 RELATÓRIO FINAL DE ANÁLISE")
        print("=" * 80)
        
        # Estatísticas
        total_issues = len(self.issues)
        total_improvements = len(self.improvements)
        total_excellent = len(self.excellent_practices)
        
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"   🏆 Excelentes práticas: {total_excellent}")
        print(f"   ⚠️ Problemas encontrados: {total_issues}")
        print(f"   💡 Melhorias sugeridas: {total_improvements}")
        
        # Score de qualidade
        total_items = total_issues + total_improvements + total_excellent
        if total_items > 0:
            quality_score = (total_excellent / total_items) * 100
            print(f"   🎯 Score de Qualidade: {quality_score:.1f}%")
        
        # Detalhes dos problemas
        if self.issues:
            print(f"\n❌ PROBLEMAS CRÍTICOS ({len(self.issues)}):")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")
        
        # Detalhes das melhorias
        if self.improvements:
            print(f"\n💡 MELHORIAS SUGERIDAS ({len(self.improvements)}):")
            for i, improvement in enumerate(self.improvements, 1):
                print(f"   {i}. {improvement}")
        
        # Práticas excelentes
        if self.excellent_practices:
            print(f"\n🏆 PRÁTICAS EXCELENTES ({len(self.excellent_practices)}):")
            for i, practice in enumerate(self.excellent_practices, 1):
                print(f"   {i}. {practice}")
        
        # Recomendações finais
        print(f"\n🎯 RECOMENDAÇÕES FINAIS:")
        if total_issues == 0:
            print("   ✅ Código em excelente estado! Parabéns!")
        elif total_issues <= 3:
            print("   👍 Código em bom estado, poucos ajustes necessários")
        elif total_issues <= 7:
            print("   ⚠️ Código precisa de alguns ajustes importantes")
        else:
            print("   🚨 Código precisa de revisão significativa")
            
        print("\n" + "=" * 80)

if __name__ == "__main__":
    analyzer = CodeAnalyzer()
    analyzer.analyze_all()