#!/usr/bin/env bash
#
# MiniCoin - Comandos Rápidos
# Use este script para executar tarefas comuns rapidamente
#

show_menu() {
    clear
    echo "╔════════════════════════════════════════════════╗"
    echo "║                                                ║"
    echo "║        🪙  MiniCoin - Menu Rápido             ║"
    echo "║                                                ║"
    echo "╚════════════════════════════════════════════════╝"
    echo ""
    echo "1) Executar todos os testes"
    echo "2) Iniciar servidor"
    echo "3) Executar simulador de cliente"
    echo "4) Demonstração completa (servidor + cliente)"
    echo "5) Abrir relatório HTML"
    echo "6) Ver logs do servidor"
    echo "7) Ver logs do cliente"
    echo "8) Limpar logs"
    echo "9) Verificar estrutura de entrega"
    echo "0) Sair"
    echo ""
    echo -n "Escolha uma opção: "
}

run_tests() {
    echo ""
    echo "Executando testes..."
    pytest tests/ -v
    echo ""
    read -p "Pressione ENTER para continuar..."
}

start_server() {
    echo ""
    echo "Iniciando servidor MiniCoin..."
    echo "Use Ctrl+C para parar"
    echo ""
    python -m minicoin.server --owner 'João Silva' --initial 100.0
}

run_simulator() {
    echo ""
    echo "Executando simulador de cliente..."
    echo ""
    python -m clients.simulator
    echo ""
    read -p "Pressione ENTER para continuar..."
}

run_demo() {
    echo ""
    echo "Executando demonstração completa..."
    echo ""
    ./run_demo.sh
    echo ""
    read -p "Pressione ENTER para continuar..."
}

view_report() {
    echo ""
    echo "Abrindo relatório HTML..."
    ./view_report.sh
    echo ""
    read -p "Pressione ENTER para continuar..."
}

view_server_log() {
    echo ""
    echo "=== LOG DO SERVIDOR ==="
    echo ""
    if [ -f logs/server.log ]; then
        tail -n 50 logs/server.log
    else
        echo "Arquivo de log não encontrado. Execute o servidor primeiro."
    fi
    echo ""
    read -p "Pressione ENTER para continuar..."
}

view_client_log() {
    echo ""
    echo "=== LOG DO CLIENTE ==="
    echo ""
    if [ -f logs/client.log ]; then
        tail -n 50 logs/client.log
    else
        echo "Arquivo de log não encontrado. Execute o simulador primeiro."
    fi
    echo ""
    read -p "Pressione ENTER para continuar..."
}

clean_logs() {
    echo ""
    echo "Limpando logs..."
    rm -f logs/server.log logs/client.log
    echo "✓ Logs limpos"
    echo ""
    read -p "Pressione ENTER para continuar..."
}

verify_delivery() {
    echo ""
    echo "=== VERIFICAÇÃO DE ESTRUTURA DE ENTREGA ==="
    echo ""
    
    echo "📄 Relatório HTML:"
    ls -lh docs/report/index.html 2>/dev/null && echo "  ✓ Encontrado" || echo "  ✗ NÃO encontrado"
    echo ""
    
    echo "📁 Código fonte (.txt):"
    ls deliverables/code/*.txt 2>/dev/null | wc -l | xargs echo "  Arquivos:"
    ls -lh deliverables/code/*.txt 2>/dev/null || echo "  ✗ Nenhum arquivo encontrado"
    echo ""
    
    echo "📊 Logs de execução:"
    ls -lh deliverables/logs/*.log 2>/dev/null || echo "  ✗ Nenhum log encontrado"
    echo ""
    
    echo "🧪 Testes:"
    pytest tests/ -v --tb=no -q 2>&1 | grep -E "passed|failed"
    echo ""
    
    echo "✅ RESUMO:"
    echo "  • Relatório: docs/report/index.html"
    echo "  • Código: deliverables/code/*.txt"
    echo "  • Logs: deliverables/logs/*.log"
    echo ""
    read -p "Pressione ENTER para continuar..."
}

# Loop principal
while true; do
    show_menu
    read choice
    
    case $choice in
        1) run_tests ;;
        2) start_server ;;
        3) run_simulator ;;
        4) run_demo ;;
        5) view_report ;;
        6) view_server_log ;;
        7) view_client_log ;;
        8) clean_logs ;;
        9) verify_delivery ;;
        0) echo ""; echo "Até logo!"; echo ""; exit 0 ;;
        *) echo "Opção inválida. Pressione ENTER..."; read ;;
    esac
done
