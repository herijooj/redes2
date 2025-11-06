"""
MiniCoin Client Simulator - Simulador de requisições para teste
Gera transações válidas e inválidas para testar o servidor MiniCoin.

Funcionalidades:
- Conexão TCP com o servidor
- Envio de depósitos válidos
- Envio de retiradas válidas
- Tentativas de retiradas inválidas (overdraft)
- Consultas de saldo e histórico
- Logging detalhado de todas as operações
"""

import asyncio
import json
import logging
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


def setup_logging(log_file: str = "logs/client.log"):
    """Configura o sistema de logging do cliente."""
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("MiniCoinClient")


class MiniCoinClient:
    """
    Cliente para conectar ao servidor MiniCoin e realizar transações.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8888):
        """
        Inicializa o cliente MiniCoin.
        
        Args:
            host: Endereço do servidor
            port: Porta do servidor
        """
        self.host = host
        self.port = port
        self.logger = setup_logging()
        self.request_counter = 0
        
        self.logger.info(f"MiniCoin Client initialized")

    async def connect(self) -> tuple:
        """
        Estabelece conexão com o servidor.
        
        Returns:
            Tupla (reader, writer) para comunicação
        """
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port)
            self.logger.info(f"Connected to server at {self.host}:{self.port}")
            return reader, writer
        except Exception as e:
            self.logger.error(f"Failed to connect to server: {e}")
            raise

    async def send_request(self, reader: asyncio.StreamReader, 
                          writer: asyncio.StreamWriter, 
                          action: str, **kwargs) -> Optional[dict]:
        """
        Envia uma requisição ao servidor e aguarda resposta.
        
        Args:
            reader: Stream de entrada
            writer: Stream de saída
            action: Tipo de ação (deposit, withdraw, balance, etc.)
            **kwargs: Parâmetros adicionais da requisição
            
        Returns:
            Dicionário com a resposta do servidor
        """
        self.request_counter += 1
        request_id = f"{self.request_counter:04d}"
        
        request = {
            "action": action,
            "id": request_id,
            **kwargs
        }
        
        try:
            # Envia a requisição
            request_json = json.dumps(request) + "\n"
            writer.write(request_json.encode())
            await writer.drain()
            
            self.logger.info(f"[{request_id}] Sent: {action.upper()} {kwargs}")
            
            # Aguarda resposta
            data = await reader.read(4096)
            response = json.loads(data.decode().strip())
            
            self.logger.info(f"[{request_id}] Response: {response.get('status', 'unknown')} - {response.get('message', '')}")
            
            return response
            
        except Exception as e:
            self.logger.error(f"[{request_id}] Error: {e}")
            return None

    async def deposit(self, reader, writer, amount: float) -> dict:
        """Realiza um depósito."""
        return await self.send_request(reader, writer, "deposit", amount=amount)

    async def withdraw(self, reader, writer, amount: float) -> dict:
        """Realiza uma retirada."""
        return await self.send_request(reader, writer, "withdraw", amount=amount)

    async def get_balance(self, reader, writer) -> dict:
        """Consulta o saldo."""
        return await self.send_request(reader, writer, "balance")

    async def get_history(self, reader, writer) -> dict:
        """Consulta o histórico."""
        return await self.send_request(reader, writer, "history")

    async def verify_integrity(self, reader, writer) -> dict:
        """Verifica a integridade da blockchain."""
        return await self.send_request(reader, writer, "verify")

    async def ping(self, reader, writer) -> dict:
        """Testa a conexão."""
        return await self.send_request(reader, writer, "ping")


class TransactionSimulator:
    """
    Simulador que gera cenários de teste para o MiniCoin.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8888):
        """
        Inicializa o simulador.
        
        Args:
            host: Endereço do servidor
            port: Porta do servidor
        """
        self.host = host
        self.port = port
        self.logger = setup_logging()
        self.results = []

    async def run_scenario(self, scenario_name: str, transactions: List[Dict]):
        """
        Executa um cenário de teste.
        
        Args:
            scenario_name: Nome do cenário
            transactions: Lista de transações a executar
        """
        print(f"\n{'='*60}")
        print(f"Scenario: {scenario_name}")
        print(f"{'='*60}\n")
        
        self.logger.info(f"Starting scenario: {scenario_name}")
        
        client = MiniCoinClient(self.host, self.port)
        
        try:
            reader, writer = await client.connect()
            
            # Testa conectividade
            await client.ping(reader, writer)
            await asyncio.sleep(0.5)
            
            # Executa cada transação
            for i, transaction in enumerate(transactions, 1):
                action = transaction.get("action")
                amount = transaction.get("amount")
                description = transaction.get("description", "")
                
                print(f"\n[Transaction {i}/{len(transactions)}] {description}")
                
                if action == "deposit":
                    response = await client.deposit(reader, writer, amount)
                elif action == "withdraw":
                    response = await client.withdraw(reader, writer, amount)
                elif action == "balance":
                    response = await client.get_balance(reader, writer)
                elif action == "history":
                    response = await client.get_history(reader, writer)
                elif action == "verify":
                    response = await client.verify_integrity(reader, writer)
                
                if response:
                    status = response.get("status", "unknown")
                    message = response.get("message", "")
                    balance = response.get("balance", 0)
                    
                    if status == "ok":
                        print(f"✓ SUCCESS: {message}")
                        if "balance" in response:
                            print(f"  Balance: {balance:.2f} MiniCoins")
                    else:
                        print(f"✗ REJECTED: {message}")
                        if "balance" in response:
                            print(f"  Balance: {balance:.2f} MiniCoins")
                    
                    self.results.append({
                        "scenario": scenario_name,
                        "transaction": i,
                        "action": action,
                        "amount": amount,
                        "status": status,
                        "message": message,
                        "balance": balance
                    })
                
                await asyncio.sleep(0.5)
            
            # Consulta final
            print("\n--- Final Status ---")
            balance_response = await client.get_balance(reader, writer)
            if balance_response:
                print(f"Final Balance: {balance_response.get('balance', 0):.2f} MiniCoins")
                print(f"Total Blocks: {balance_response.get('block_count', 0)}")
            
            # Verifica integridade
            verify_response = await client.verify_integrity(reader, writer)
            if verify_response:
                if verify_response.get("valid"):
                    print("✓ Blockchain integrity verified")
                else:
                    print("✗ Blockchain integrity check FAILED")
            
            writer.close()
            await writer.wait_closed()
            
        except Exception as e:
            self.logger.error(f"Scenario {scenario_name} failed: {e}", exc_info=True)
            print(f"\n✗ Scenario failed: {e}")
        
        print(f"\n{'='*60}\n")
        self.logger.info(f"Scenario {scenario_name} completed")

    async def run_all_scenarios(self):
        """Executa todos os cenários de teste."""
        
        # Cenário 1: Transações básicas válidas
        scenario1 = [
            {"action": "balance", "description": "Check initial balance"},
            {"action": "deposit", "amount": 50.0, "description": "Deposit 50 MiniCoins"},
            {"action": "balance", "description": "Check balance after deposit"},
            {"action": "withdraw", "amount": 30.0, "description": "Withdraw 30 MiniCoins"},
            {"action": "balance", "description": "Check balance after withdrawal"},
        ]
        await self.run_scenario("basic-valid-transactions", scenario1)
        await asyncio.sleep(1)
        
        # Cenário 2: Tentativas de overdraft
        scenario2 = [
            {"action": "balance", "description": "Check current balance"},
            {"action": "withdraw", "amount": 50.0, "description": "Valid withdrawal: 50 MiniCoins"},
            {"action": "withdraw", "amount": 100.0, "description": "INVALID: Try to withdraw 100 (overdraft)"},
            {"action": "withdraw", "amount": 200.0, "description": "INVALID: Try to withdraw 200 (overdraft)"},
            {"action": "balance", "description": "Balance should be unchanged after rejections"},
        ]
        await self.run_scenario("overdraft-attempts", scenario2)
        await asyncio.sleep(1)
        
        # Cenário 3: Múltiplos depósitos e retiradas
        scenario3 = [
            {"action": "deposit", "amount": 100.0, "description": "Deposit 100 MiniCoins"},
            {"action": "deposit", "amount": 50.0, "description": "Deposit 50 MiniCoins"},
            {"action": "withdraw", "amount": 80.0, "description": "Withdraw 80 MiniCoins"},
            {"action": "deposit", "amount": 30.0, "description": "Deposit 30 MiniCoins"},
            {"action": "withdraw", "amount": 120.0, "description": "Withdraw 120 MiniCoins"},
            {"action": "balance", "description": "Final balance check"},
        ]
        await self.run_scenario("multiple-transactions", scenario3)
        await asyncio.sleep(1)
        
        # Cenário 4: Valores inválidos
        scenario4 = [
            {"action": "deposit", "amount": -10.0, "description": "INVALID: Negative deposit"},
            {"action": "withdraw", "amount": -5.0, "description": "INVALID: Negative withdrawal"},
            {"action": "deposit", "amount": 0.0, "description": "INVALID: Zero deposit"},
            {"action": "balance", "description": "Balance should be unchanged"},
        ]
        await self.run_scenario("invalid-values", scenario4)
        await asyncio.sleep(1)
        
        # Cenário 5: Transações aleatórias
        print("\n" + "="*60)
        print("Scenario: Random Transactions")
        print("="*60)
        print("Generating random transactions...")
        
        random_transactions = []
        for i in range(10):
            if random.random() > 0.5:
                amount = random.uniform(10, 100)
                random_transactions.append({
                    "action": "deposit",
                    "amount": round(amount, 2),
                    "description": f"Random deposit: {amount:.2f}"
                })
            else:
                amount = random.uniform(10, 150)  # Pode causar overdraft
                random_transactions.append({
                    "action": "withdraw",
                    "amount": round(amount, 2),
                    "description": f"Random withdrawal: {amount:.2f}"
                })
        
        await self.run_scenario("random-transactions", random_transactions)
        
        # Relatório final
        self.print_summary()

    def print_summary(self):
        """Imprime um resumo dos resultados."""
        print("\n" + "="*60)
        print("SIMULATION SUMMARY")
        print("="*60)
        
        total = len(self.results)
        successful = sum(1 for r in self.results if r["status"] == "ok")
        rejected = sum(1 for r in self.results if r["status"] == "error")
        
        print(f"Total Transactions: {total}")
        print(f"Successful: {successful} ({successful/total*100:.1f}%)")
        print(f"Rejected: {rejected} ({rejected/total*100:.1f}%)")
        print("="*60 + "\n")
        
        self.logger.info(f"Simulation completed: {successful}/{total} successful")


async def main():
    """Função principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description="MiniCoin Client Simulator")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")
    parser.add_argument("--port", type=int, default=8888, help="Server port")
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("MiniCoin Transaction Simulator")
    print("="*60)
    print(f"Target Server: {args.host}:{args.port}")
    print("="*60 + "\n")
    
    simulator = TransactionSimulator(args.host, args.port)
    
    try:
        await simulator.run_all_scenarios()
    except KeyboardInterrupt:
        print("\nSimulation stopped by user")
    except Exception as e:
        print(f"\nSimulation error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
