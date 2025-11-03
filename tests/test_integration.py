"""
Testes de integração para o sistema MiniCoin completo.
Testa a comunicação cliente-servidor e cenários end-to-end.
"""

import pytest
import asyncio
import json
from minicoin.server import MiniCoinServer
from clients.simulator import MiniCoinClient


@pytest.fixture
async def server():
    """Fixture que cria e inicia um servidor de teste."""
    test_server = MiniCoinServer(
        host="127.0.0.1",
        port=9999,
        owner="Test Account",
        initial_deposit=100.0
    )
    
    # Inicia o servidor em background
    server_task = asyncio.create_task(test_server.start())
    
    # Aguarda um pouco para o servidor iniciar
    await asyncio.sleep(0.5)
    
    yield test_server
    
    # Cleanup: cancela o servidor
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass


@pytest.fixture
async def client():
    """Fixture que cria um cliente de teste."""
    test_client = MiniCoinClient(
        host="127.0.0.1",
        port=9999,
        client_id="test-client"
    )
    return test_client


@pytest.mark.asyncio
async def test_server_initialization(server):
    """Testa a inicialização do servidor."""
    assert server.ledger.owner == "Test Account"
    assert server.ledger.get_balance() == 100.0
    assert len(server.ledger.chain) == 1


@pytest.mark.asyncio
async def test_client_connection(server, client):
    """Testa a conexão do cliente ao servidor."""
    reader, writer = await client.connect()
    
    assert reader is not None
    assert writer is not None
    
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_ping_pong(server, client):
    """Testa a comunicação básica ping/pong."""
    reader, writer = await client.connect()
    
    response = await client.ping(reader, writer)
    
    assert response is not None
    assert response["status"] == "ok"
    assert response["message"] == "pong"
    
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_deposit_transaction(server, client):
    """Testa uma transação de depósito."""
    reader, writer = await client.connect()
    
    initial_balance = server.ledger.get_balance()
    response = await client.deposit(reader, writer, 50.0)
    
    assert response["status"] == "ok"
    assert response["balance"] == initial_balance + 50.0
    assert "block_index" in response
    assert "block_hash" in response
    
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_withdraw_transaction(server, client):
    """Testa uma transação de retirada."""
    reader, writer = await client.connect()
    
    initial_balance = server.ledger.get_balance()
    response = await client.withdraw(reader, writer, 30.0)
    
    assert response["status"] == "ok"
    assert response["balance"] == initial_balance - 30.0
    
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_overdraft_rejection(server, client):
    """Testa a rejeição de overdraft."""
    reader, writer = await client.connect()
    
    # Tenta retirar mais do que o saldo disponível
    current_balance = server.ledger.get_balance()
    response = await client.withdraw(reader, writer, current_balance + 100.0)
    
    assert response["status"] == "error"
    assert "insuficiente" in response["message"].lower()
    assert response["balance"] == current_balance
    
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_balance_query(server, client):
    """Testa consulta de saldo."""
    reader, writer = await client.connect()
    
    response = await client.get_balance(reader, writer)
    
    assert response["status"] == "ok"
    assert "balance" in response
    assert "block_count" in response
    assert response["balance"] == server.ledger.get_balance()
    
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_history_query(server, client):
    """Testa consulta de histórico."""
    reader, writer = await client.connect()
    
    # Faz algumas transações
    await client.deposit(reader, writer, 50.0)
    await client.withdraw(reader, writer, 30.0)
    
    # Consulta histórico
    response = await client.get_history(reader, writer)
    
    assert response["status"] == "ok"
    assert "history" in response
    assert len(response["history"]) >= 3  # Genesis + 2 transações
    
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_integrity_verification(server, client):
    """Testa verificação de integridade."""
    reader, writer = await client.connect()
    
    # Faz algumas transações
    await client.deposit(reader, writer, 25.0)
    await client.withdraw(reader, writer, 15.0)
    
    # Verifica integridade
    response = await client.verify_integrity(reader, writer)
    
    assert response["status"] == "ok"
    assert response["valid"] is True
    
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_multiple_sequential_transactions(server, client):
    """Testa múltiplas transações sequenciais."""
    reader, writer = await client.connect()
    
    initial_balance = server.ledger.get_balance()
    
    # Série de transações
    await client.deposit(reader, writer, 50.0)
    await client.withdraw(reader, writer, 30.0)
    await client.deposit(reader, writer, 20.0)
    await client.withdraw(reader, writer, 10.0)
    
    # Verifica saldo final
    response = await client.get_balance(reader, writer)
    expected_balance = initial_balance + 50 - 30 + 20 - 10
    
    assert abs(response["balance"] - expected_balance) < 0.001
    
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_concurrent_clients():
    """Testa múltiplos clientes simultâneos."""
    # Inicia servidor
    test_server = MiniCoinServer(
        host="127.0.0.1",
        port=9998,
        owner="Concurrent Test",
        initial_deposit=1000.0
    )
    
    server_task = asyncio.create_task(test_server.start())
    await asyncio.sleep(0.5)
    
    try:
        # Cria múltiplos clientes
        clients = [
            MiniCoinClient("127.0.0.1", 9998, f"client-{i}")
            for i in range(3)
        ]
        
        async def client_operation(client, amount):
            reader, writer = await client.connect()
            response = await client.deposit(reader, writer, amount)
            writer.close()
            await writer.wait_closed()
            return response
        
        # Executa operações concorrentes
        tasks = [
            client_operation(clients[0], 100.0),
            client_operation(clients[1], 150.0),
            client_operation(clients[2], 200.0)
        ]
        
        responses = await asyncio.gather(*tasks)
        
        # Verifica que todas foram bem-sucedidas
        assert all(r["status"] == "ok" for r in responses)
        
        # Verifica saldo final
        assert test_server.ledger.get_balance() == 1450.0
        
    finally:
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass


@pytest.mark.asyncio
async def test_invalid_json_handling(server):
    """Testa o tratamento de JSON inválido."""
    reader, writer = await asyncio.open_connection("127.0.0.1", 9999)
    
    # Envia JSON inválido
    writer.write(b"{ invalid json }\n")
    await writer.drain()
    
    data = await reader.read(1024)
    response = json.loads(data.decode().strip())
    
    assert response["status"] == "error"
    assert "Invalid JSON" in response["message"]
    
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_unknown_action(server, client):
    """Testa o tratamento de ação desconhecida."""
    reader, writer = await client.connect()
    
    response = await client.send_request(reader, writer, "unknown_action")
    
    assert response["status"] == "error"
    assert "Unknown action" in response["message"]
    
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_negative_deposit(server, client):
    """Testa depósito com valor negativo."""
    reader, writer = await client.connect()
    
    response = await client.deposit(reader, writer, -50.0)
    
    assert response["status"] == "error"
    assert "positivo" in response["message"].lower()
    
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_session_persistence(server, client):
    """Testa que o ledger persiste entre conexões diferentes."""
    # Primeira conexão: faz um depósito
    reader1, writer1 = await client.connect()
    await client.deposit(reader1, writer1, 100.0)
    writer1.close()
    await writer1.wait_closed()
    
    # Segunda conexão: verifica que o depósito foi registrado
    client2 = MiniCoinClient("127.0.0.1", 9999, "client-2")
    reader2, writer2 = await client2.connect()
    response = await client2.get_balance(reader2, writer2)
    
    assert response["balance"] == 200.0  # 100 inicial + 100 depositado
    
    writer2.close()
    await writer2.wait_closed()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
