#!/usr/bin/env bash
#
# Script para executar demonstração completa do MiniCoin
# Inicia o servidor, executa o simulador, e para o servidor
#

echo "=========================================="
echo "  MiniCoin - Demonstração Completa"
echo "=========================================="
echo ""

echo "Iniciando servidor MiniCoin..."
python -m minicoin.server --owner 'João Silva' --initial 100.0 &
SERVER_PID=$!

# Aguarda o servidor inicializar
sleep 3

echo ""
echo "Executando simulador de transações..."
echo ""

# Executa o simulador
python -m clients.simulator

echo ""
echo "=========================================="
echo "  Demonstração concluída!"
echo "=========================================="
echo ""
echo "Logs gerados:"
echo "  - logs/server.log"
echo "  - logs/client.log"
echo ""

# Para o servidor
echo "Parando servidor..."
kill $SERVER_PID 2>/dev/null

echo "Concluído!"
