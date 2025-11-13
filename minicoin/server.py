"""
MiniCoin Server - Servidor TCP para gerenciamento da blockchain
Implementa um servidor assíncrono que recebe requisições de clientes
e executa operações na blockchain MiniCoin.

Operações suportadas:
- deposit: Adiciona fundos à conta
- withdraw: Remove fundos da conta (valida saldo)
- balance: Consulta o saldo atual
- history: Retorna o histórico completo de transações
- verify: Verifica a integridade da blockchain
- ping: Testa conectividade
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from minicoin.ledger import MiniCoinLedger


# Configuração de logging
def setup_logging(log_file: str = "logs/server.log"):
    """Configura o sistema de logging do servidor."""
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
    return logging.getLogger("MiniCoinServer")


class MiniCoinServer:
    """
    Servidor TCP assíncrono para a MiniCoin.
    
    Gerencia conexões de clientes e executa operações na blockchain.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8888, 
                 owner: str = "MiniCoin Account", initial_deposit: float = 100.0):
        """
        Inicializa o servidor MiniCoin.
        
        Args:
            host: Endereço IP do servidor
            port: Porta TCP para escutar
            owner: Nome do proprietário da conta
            initial_deposit: Depósito inicial da conta
        """
        self.host = host
        self.port = port
        self.ledger = MiniCoinLedger(owner, initial_deposit)
        self.logger = setup_logging()
        self.request_count = 0
        
        self.logger.info(f"MiniCoin Server initialized")
        self.logger.info(f"Owner: {owner}")
        self.logger.info(f"Initial deposit: {initial_deposit:.2f}")
        self.logger.info(f"Genesis block hash: {self.ledger.chain[0].hash}")

    async def handle_client(self, reader: asyncio.StreamReader, 
                           writer: asyncio.StreamWriter):
        """
        Gerencia a conexão com um cliente.
        
        Args:
            reader: Stream de entrada do cliente
            writer: Stream de saída do cliente
        """
        addr = writer.get_extra_info('peername')
        self.logger.info(f"New connection from {addr}")

        try:
            while True:
                # Lê dados do cliente (até 1KB)
                data = await reader.read(1024)
                
                if not data:
                    self.logger.info(f"Client {addr} disconnected")
                    break

                # Decodifica a mensagem
                message = data.decode().strip()
                self.logger.info(f"Received from {addr}: {message}")

                # Processa a requisição
                response = await self.process_request(message)
                
                # Envia a resposta
                response_json = json.dumps(response) + "\n"
                writer.write(response_json.encode())
                await writer.drain()
                
                self.logger.info(f"Sent to {addr}: {response_json.strip()}")

        except Exception as e:
            self.logger.error(f"Error handling client {addr}: {e}", exc_info=True)
        finally:
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"Connection closed with {addr}")

    async def process_request(self, message: str) -> dict:
        """
        Processa uma requisição do cliente.
        
        Args:
            message: Mensagem JSON do cliente
            
        Returns:
            Dicionário com a resposta
        """
        self.request_count += 1
        request_id = self.request_count

        try:
            # Parse da mensagem JSON
            request = json.loads(message)
            action = request.get("action", "").lower()
            
            self.logger.info(f"[Request #{request_id}] Action: {action}")

            # Processa cada tipo de ação
            if action == "deposit":
                return await self.handle_deposit(request, request_id)
            
            elif action == "withdraw":
                return await self.handle_withdraw(request, request_id)
            
            elif action == "balance":
                return await self.handle_balance(request, request_id)
            
            elif action == "history":
                return await self.handle_history(request, request_id)
            
            elif action == "verify":
                return await self.handle_verify(request, request_id)
            
            elif action == "ping":
                return await self.handle_ping(request, request_id)
            
            else:
                return {
                    "status": "error",
                    "message": f"Unknown action: {action}",
                    "request_id": request_id,
                    "timestamp": datetime.now().isoformat()
                }

        except json.JSONDecodeError as e:
            self.logger.error(f"[Request #{request_id}] Invalid JSON: {e}")
            return {
                "status": "error",
                "message": "Invalid JSON format",
                "request_id": request_id,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"[Request #{request_id}] Error: {e}", exc_info=True)
            return {
                "status": "error",
                "message": str(e),
                "request_id": request_id,
                "timestamp": datetime.now().isoformat()
            }

    async def handle_deposit(self, request: dict, request_id: int) -> dict:
        """Processa uma requisição de depósito."""
        amount = request.get("amount", 0)
        client_id = request.get("client_id", request.get("id", "unknown"))
        
        success, message, block = self.ledger.deposit(amount)
        
        if success:
            self.logger.info(f"[Request #{request_id}] Deposit successful: {amount:.2f}")
            return {
                "status": "ok",
                "message": message,
                "balance": self.ledger.get_balance(),
                "block_index": block.index,
                "block_hash": block.hash,
                "request_id": request_id,
                "client_id": client_id,
                "timestamp": datetime.now().isoformat()
            }
        else:
            self.logger.warning(f"[Request #{request_id}] Deposit failed: {message}")
            return {
                "status": "error",
                "message": message,
                "balance": self.ledger.get_balance(),
                "request_id": request_id,
                "client_id": client_id,
                "timestamp": datetime.now().isoformat()
            }

    async def handle_withdraw(self, request: dict, request_id: int) -> dict:
        """Processa uma requisição de retirada."""
        amount = request.get("amount", 0)
        client_id = request.get("client_id", request.get("id", "unknown"))
        
        current_balance = self.ledger.get_balance()
        success, message, block = self.ledger.withdraw(amount)
        
        if success:
            self.logger.info(f"[Request #{request_id}] Withdrawal successful: {amount:.2f}")
            return {
                "status": "ok",
                "message": message,
                "balance": self.ledger.get_balance(),
                "block_index": block.index,
                "block_hash": block.hash,
                "request_id": request_id,
                "client_id": client_id,
                "timestamp": datetime.now().isoformat()
            }
        else:
            self.logger.warning(f"[Request #{request_id}] Withdrawal rejected: {message}")
            return {
                "status": "error",
                "message": message,
                "balance": current_balance,
                "request_id": request_id,
                "client_id": client_id,
                "timestamp": datetime.now().isoformat()
            }

    async def handle_balance(self, request: dict, request_id: int) -> dict:
        """Processa uma requisição de consulta de saldo."""
        client_id = request.get("client_id", request.get("id", "unknown"))
        balance = self.ledger.get_balance()
        
        self.logger.info(f"[Request #{request_id}] Balance query: {balance:.2f}")
        return {
            "status": "ok",
            "balance": balance,
            "block_count": self.ledger.get_block_count(),
            "request_id": request_id,
            "client_id": client_id,
            "timestamp": datetime.now().isoformat()
        }

    async def handle_history(self, request: dict, request_id: int) -> dict:
        """Processa uma requisição de histórico."""
        client_id = request.get("client_id", request.get("id", "unknown"))
        history = self.ledger.get_history()
        
        self.logger.info(f"[Request #{request_id}] History query: {len(history)} blocks")
        return {
            "status": "ok",
            "history": history,
            "block_count": len(history),
            "request_id": request_id,
            "client_id": client_id,
            "timestamp": datetime.now().isoformat()
        }

    async def handle_verify(self, request: dict, request_id: int) -> dict:
        """Processa uma requisição de verificação de integridade."""
        client_id = request.get("client_id", request.get("id", "unknown"))
        valid, message = self.ledger.verify_integrity()
        
        self.logger.info(f"[Request #{request_id}] Integrity check: {message}")
        return {
            "status": "ok" if valid else "error",
            "valid": valid,
            "message": message,
            "request_id": request_id,
            "client_id": client_id,
            "timestamp": datetime.now().isoformat()
        }

    async def handle_ping(self, request: dict, request_id: int) -> dict:
        """Processa uma requisição de ping."""
        client_id = request.get("client_id", request.get("id", "unknown"))
        
        self.logger.debug(f"[Request #{request_id}] Ping from {client_id}")
        return {
            "status": "ok",
            "message": "pong",
            "request_id": request_id,
            "client_id": client_id,
            "timestamp": datetime.now().isoformat()
        }

    async def start(self):
        """Inicia o servidor."""
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )

        addr = server.sockets[0].getsockname()
        self.logger.info(f"Server listening on {addr[0]}:{addr[1]}")
        
        print(f"\n{'='*60}")
        print(f"MiniCoin Server Started")
        print(f"{'='*60}")
        print(f"Address: {addr[0]}:{addr[1]}")
        print(f"Owner: {self.ledger.owner}")
        print(f"Initial Balance: {self.ledger.get_balance():.2f} MiniCoins")
        print(f"{'='*60}\n")

        async with server:
            await server.serve_forever()


def main():
    """Função principal para executar o servidor."""
    import argparse
    
    parser = argparse.ArgumentParser(description="MiniCoin Server")
    parser.add_argument("--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8888, help="Server port (default: 8888)")
    parser.add_argument("--owner", default="João Silva", help="Account owner name")
    parser.add_argument("--initial", type=float, default=100.0, help="Initial deposit (default: 100.0)")
    
    args = parser.parse_args()
    
    server = MiniCoinServer(
        host=args.host,
        port=args.port,
        owner=args.owner,
        initial_deposit=args.initial
    )
    
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\nServer stopped by user")


if __name__ == "__main__":
    main()
