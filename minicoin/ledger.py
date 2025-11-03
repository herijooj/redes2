"""
MiniCoin Ledger - Blockchain Implementation
Implementa a estrutura de blockchain para a moeda virtual MiniCoin.

Cada bloco contém:
- Índice sequencial
- Timestamp da transação
- Operação realizada (CREATE, DEPOSIT, WITHDRAW)
- Valor da transação
- Saldo após a transação
- Hash do bloco anterior
- Hash do bloco atual (calculado sobre todos os campos acima)
"""

import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional, Tuple


@dataclass
class Block:
    """
    Representa um bloco individual na blockchain do MiniCoin.
    
    Attributes:
        index: Posição do bloco na cadeia (começando em 0)
        timestamp: Data e hora da criação do bloco
        operation: Tipo de operação (CREATE, DEPOSIT, WITHDRAW)
        amount: Valor da transação
        balance: Saldo da conta após esta transação
        owner: Nome do proprietário da conta
        previous_hash: Hash do bloco anterior (None para o bloco genesis)
        hash: Hash deste bloco
    """
    index: int
    timestamp: str
    operation: str
    amount: float
    balance: float
    owner: str
    previous_hash: Optional[str]
    hash: str

    def to_dict(self) -> dict:
        """Converte o bloco para dicionário."""
        return asdict(self)

    def to_json(self) -> str:
        """Converte o bloco para JSON."""
        return json.dumps(self.to_dict(), indent=2)


class MiniCoinLedger:
    """
    Gerencia a blockchain da MiniCoin.
    
    Mantém uma lista encadeada de blocos onde cada bloco contém
    o hash do bloco anterior, garantindo integridade da cadeia.
    """

    def __init__(self, owner: str, initial_deposit: float = 0.0):
        """
        Inicializa o ledger com um bloco genesis.
        
        Args:
            owner: Nome do proprietário da conta
            initial_deposit: Depósito inicial (padrão: 0.0)
        """
        self.owner = owner
        self.chain: List[Block] = []
        self._create_genesis_block(initial_deposit)

    def _calculate_hash(self, index: int, timestamp: str, operation: str,
                       amount: float, balance: float, owner: str,
                       previous_hash: Optional[str]) -> str:
        """
        Calcula o hash SHA-256 do bloco.
        
        O hash é calculado sobre todos os campos do bloco concatenados
        com o hash do bloco anterior.
        
        Args:
            index: Índice do bloco
            timestamp: Timestamp da transação
            operation: Tipo de operação
            amount: Valor da transação
            balance: Saldo resultante
            owner: Proprietário da conta
            previous_hash: Hash do bloco anterior
            
        Returns:
            Hash SHA-256 em formato hexadecimal
        """
        # Concatena todos os dados do bloco
        block_data = f"{index}{timestamp}{operation}{amount}{balance}{owner}{previous_hash or ''}"
        
        # Calcula o hash SHA-256
        return hashlib.sha256(block_data.encode()).hexdigest()

    def _create_genesis_block(self, initial_deposit: float):
        """
        Cria o bloco genesis (primeiro bloco) da blockchain.
        
        Args:
            initial_deposit: Valor do depósito inicial
        """
        timestamp = datetime.now().isoformat()
        operation = "CREATE"
        
        block_hash = self._calculate_hash(
            index=0,
            timestamp=timestamp,
            operation=operation,
            amount=initial_deposit,
            balance=initial_deposit,
            owner=self.owner,
            previous_hash=None
        )

        genesis_block = Block(
            index=0,
            timestamp=timestamp,
            operation=operation,
            amount=initial_deposit,
            balance=initial_deposit,
            owner=self.owner,
            previous_hash=None,
            hash=block_hash
        )

        self.chain.append(genesis_block)

    def get_balance(self) -> float:
        """
        Retorna o saldo atual da conta.
        
        Returns:
            Saldo atual (balance do último bloco)
        """
        if not self.chain:
            return 0.0
        return self.chain[-1].balance

    def deposit(self, amount: float) -> Tuple[bool, str, Optional[Block]]:
        """
        Adiciona um depósito à conta.
        
        Args:
            amount: Valor a ser depositado
            
        Returns:
            Tupla (sucesso, mensagem, bloco_criado)
        """
        if amount <= 0:
            return False, "Valor de depósito deve ser positivo", None

        current_balance = self.get_balance()
        new_balance = current_balance + amount
        
        timestamp = datetime.now().isoformat()
        previous_block = self.chain[-1]
        new_index = len(self.chain)

        block_hash = self._calculate_hash(
            index=new_index,
            timestamp=timestamp,
            operation="DEPOSIT",
            amount=amount,
            balance=new_balance,
            owner=self.owner,
            previous_hash=previous_block.hash
        )

        new_block = Block(
            index=new_index,
            timestamp=timestamp,
            operation="DEPOSIT",
            amount=amount,
            balance=new_balance,
            owner=self.owner,
            previous_hash=previous_block.hash,
            hash=block_hash
        )

        self.chain.append(new_block)
        return True, f"Depósito de {amount:.2f} realizado com sucesso", new_block

    def withdraw(self, amount: float) -> Tuple[bool, str, Optional[Block]]:
        """
        Realiza uma retirada da conta.
        
        Valida se há saldo suficiente antes de criar o bloco.
        
        Args:
            amount: Valor a ser retirado
            
        Returns:
            Tupla (sucesso, mensagem, bloco_criado)
        """
        if amount <= 0:
            return False, "Valor de retirada deve ser positivo", None

        current_balance = self.get_balance()
        
        if amount > current_balance:
            return False, f"Saldo insuficiente. Saldo atual: {current_balance:.2f}, tentativa de retirada: {amount:.2f}", None

        new_balance = current_balance - amount
        
        timestamp = datetime.now().isoformat()
        previous_block = self.chain[-1]
        new_index = len(self.chain)

        block_hash = self._calculate_hash(
            index=new_index,
            timestamp=timestamp,
            operation="WITHDRAW",
            amount=amount,
            balance=new_balance,
            owner=self.owner,
            previous_hash=previous_block.hash
        )

        new_block = Block(
            index=new_index,
            timestamp=timestamp,
            operation="WITHDRAW",
            amount=amount,
            balance=new_balance,
            owner=self.owner,
            previous_hash=previous_block.hash,
            hash=block_hash
        )

        self.chain.append(new_block)
        return True, f"Retirada de {amount:.2f} realizada com sucesso", new_block

    def verify_integrity(self) -> Tuple[bool, str]:
        """
        Verifica a integridade de toda a blockchain.
        
        Checa se:
        1. Cada bloco tem o hash correto
        2. Cada bloco aponta para o hash correto do bloco anterior
        3. Os saldos estão consistentes
        
        Returns:
            Tupla (válido, mensagem)
        """
        if not self.chain:
            return False, "Blockchain vazia"

        # Verifica o bloco genesis
        genesis = self.chain[0]
        if genesis.previous_hash is not None:
            return False, "Bloco genesis deve ter previous_hash None"

        # Verifica cada bloco
        for i, block in enumerate(self.chain):
            # Recalcula o hash do bloco
            calculated_hash = self._calculate_hash(
                index=block.index,
                timestamp=block.timestamp,
                operation=block.operation,
                amount=block.amount,
                balance=block.balance,
                owner=block.owner,
                previous_hash=block.previous_hash
            )

            # Verifica se o hash está correto
            if block.hash != calculated_hash:
                return False, f"Hash inválido no bloco {i}"

            # Verifica o encadeamento (exceto para o genesis)
            if i > 0:
                if block.previous_hash != self.chain[i - 1].hash:
                    return False, f"Encadeamento quebrado no bloco {i}"

                # Verifica consistência de saldo
                previous_balance = self.chain[i - 1].balance
                if block.operation == "DEPOSIT":
                    expected_balance = previous_balance + block.amount
                elif block.operation == "WITHDRAW":
                    expected_balance = previous_balance - block.amount
                else:
                    expected_balance = block.balance

                if abs(block.balance - expected_balance) > 0.001:  # Tolerância para float
                    return False, f"Saldo inconsistente no bloco {i}"

        return True, "Blockchain íntegra"

    def get_history(self) -> List[dict]:
        """
        Retorna o histórico completo de transações.
        
        Returns:
            Lista de dicionários representando cada bloco
        """
        return [block.to_dict() for block in self.chain]

    def get_block_count(self) -> int:
        """Retorna o número de blocos na cadeia."""
        return len(self.chain)

    def __str__(self) -> str:
        """Representação em string do ledger."""
        return f"MiniCoinLedger(owner={self.owner}, blocks={len(self.chain)}, balance={self.get_balance():.2f})"

    def __repr__(self) -> str:
        """Representação detalhada do ledger."""
        return self.__str__()
