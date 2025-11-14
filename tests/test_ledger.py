"""
Testes unitários para o módulo ledger da MiniCoin.
Testa a funcionalidade do blockchain, validação de transações e integridade.
"""

import pytest
from minicoin.ledger import Block, MiniCoinLedger


class TestBlock:
    """Testes para a classe Block."""
    
    def test_block_creation(self):
        """Testa a criação de um bloco."""
        block = Block(
            index=0,
            timestamp="2025-10-28T10:00:00",
            operation="CREATE",
            amount=100.0,
            balance=100.0,
            owner="Test User",
            previous_hash=None,
            hash="abc123"
        )
        
        assert block.index == 0
        assert block.operation == "CREATE"
        assert block.amount == 100.0
        assert block.balance == 100.0
        assert block.owner == "Test User"
        assert block.previous_hash is None
        assert block.hash == "abc123"
    
    def test_block_to_dict(self):
        """Testa a conversão de bloco para dicionário."""
        block = Block(
            index=1,
            timestamp="2025-10-28T10:00:00",
            operation="DEPOSIT",
            amount=50.0,
            balance=150.0,
            owner="Test User",
            previous_hash="abc123",
            hash="def456"
        )
        
        block_dict = block.to_dict()
        assert isinstance(block_dict, dict)
        assert block_dict["index"] == 1
        assert block_dict["operation"] == "DEPOSIT"
        assert block_dict["amount"] == 50.0


class TestMiniCoinLedger:
    """Testes para a classe MiniCoinLedger."""
    
    def test_ledger_initialization(self):
        """Testa a inicialização do ledger."""
        ledger = MiniCoinLedger("Test User", 100.0)
        
        assert ledger.owner == "Test User"
        assert len(ledger.chain) == 1
        assert ledger.get_balance() == 100.0
        assert ledger.chain[0].operation == "CREATE"
    
    def test_genesis_block(self):
        """Testa a criação do bloco genesis."""
        ledger = MiniCoinLedger("Alice", 50.0)
        
        genesis = ledger.chain[0]
        assert genesis.index == 0
        assert genesis.operation == "CREATE"
        assert genesis.amount == 50.0
        assert genesis.balance == 50.0
        assert genesis.owner == "Alice"
        assert genesis.previous_hash is None
        assert genesis.hash is not None
        assert len(genesis.hash) == 64  # SHA-256 hash length
    
    def test_deposit_valid(self):
        """Testa um depósito válido."""
        ledger = MiniCoinLedger("Bob", 100.0)
        
        success, message, block = ledger.deposit(50.0)
        
        assert success is True
        assert "sucesso" in message.lower()
        assert block is not None
        assert ledger.get_balance() == 150.0
        assert len(ledger.chain) == 2
        assert block.operation == "DEPOSIT"
        assert block.amount == 50.0
    
    def test_deposit_negative_amount(self):
        """Testa depósito com valor negativo."""
        ledger = MiniCoinLedger("Charlie", 100.0)
        
        success, message, block = ledger.deposit(-10.0)
        
        assert success is False
        assert "positivo" in message.lower()
        assert block is None
        assert ledger.get_balance() == 100.0
        assert len(ledger.chain) == 1
    
    def test_deposit_zero(self):
        """Testa depósito com valor zero."""
        ledger = MiniCoinLedger("Dave", 100.0)
        
        success, message, block = ledger.deposit(0.0)
        
        assert success is False
        assert block is None
        assert ledger.get_balance() == 100.0
    
    def test_withdraw_valid(self):
        """Testa uma retirada válida."""
        ledger = MiniCoinLedger("Eve", 100.0)
        
        success, message, block = ledger.withdraw(30.0)
        
        assert success is True
        assert "sucesso" in message.lower()
        assert block is not None
        assert ledger.get_balance() == 70.0
        assert len(ledger.chain) == 2
        assert block.operation == "WITHDRAW"
        assert block.amount == 30.0
    
    def test_withdraw_insufficient_balance(self):
        """Testa retirada com saldo insuficiente."""
        ledger = MiniCoinLedger("Frank", 100.0)
        
        success, message, block = ledger.withdraw(150.0)
        
        assert success is False
        assert "insuficiente" in message.lower()
        assert block is None
        assert ledger.get_balance() == 100.0
        assert len(ledger.chain) == 1
    
    def test_withdraw_negative_amount(self):
        """Testa retirada com valor negativo."""
        ledger = MiniCoinLedger("Grace", 100.0)
        
        success, message, block = ledger.withdraw(-20.0)
        
        assert success is False
        assert "positivo" in message.lower()
        assert block is None
        assert ledger.get_balance() == 100.0
    
    def test_multiple_transactions(self):
        """Testa múltiplas transações."""
        ledger = MiniCoinLedger("Heidi", 100.0)
        
        ledger.deposit(50.0)   # Balance: 150
        ledger.withdraw(30.0)  # Balance: 120
        ledger.deposit(20.0)   # Balance: 140
        ledger.withdraw(40.0)  # Balance: 100
        
        assert ledger.get_balance() == 100.0
        assert len(ledger.chain) == 5  # Genesis + 4 transactions
    
    def test_blockchain_integrity(self):
        """Testa a integridade da blockchain."""
        ledger = MiniCoinLedger("Ivan", 100.0)
        
        ledger.deposit(50.0)
        ledger.withdraw(30.0)
        ledger.deposit(20.0)
        
        valid, message = ledger.verify_integrity()
        
        assert valid is True
        assert "integra" in message.lower()
    
    def test_hash_chaining(self):
        """Testa o encadeamento de hashes."""
        ledger = MiniCoinLedger("Judy", 100.0)
        
        ledger.deposit(50.0)
        ledger.withdraw(30.0)
        
        # Verifica que cada bloco aponta para o hash do anterior
        for i in range(1, len(ledger.chain)):
            current_block = ledger.chain[i]
            previous_block = ledger.chain[i - 1]
            
            assert current_block.previous_hash == previous_block.hash
    
    def test_hash_uniqueness(self):
        """Testa que cada bloco tem um hash único."""
        ledger = MiniCoinLedger("Kevin", 100.0)
        
        ledger.deposit(50.0)
        ledger.deposit(50.0)  # Mesmo valor, mas timestamp diferente
        
        hashes = [block.hash for block in ledger.chain]
        
        # Todos os hashes devem ser únicos
        assert len(hashes) == len(set(hashes))
    
    def test_get_history(self):
        """Testa a obtenção do histórico."""
        ledger = MiniCoinLedger("Laura", 100.0)
        
        ledger.deposit(30.0)
        ledger.withdraw(20.0)
        
        history = ledger.get_history()
        
        assert len(history) == 3
        assert all(isinstance(entry, dict) for entry in history)
        assert history[0]["operation"] == "CREATE"
        assert history[1]["operation"] == "DEPOSIT"
        assert history[2]["operation"] == "WITHDRAW"
    
    def test_get_block_count(self):
        """Testa a contagem de blocos."""
        ledger = MiniCoinLedger("Mike", 100.0)
        
        assert ledger.get_block_count() == 1
        
        ledger.deposit(50.0)
        assert ledger.get_block_count() == 2
        
        ledger.withdraw(30.0)
        assert ledger.get_block_count() == 3
    
    def test_balance_consistency(self):
        """Testa a consistência do saldo através de múltiplas operações."""
        ledger = MiniCoinLedger("Nancy", 100.0)
        
        expected_balance = 100.0
        
        # Série de transações
        transactions = [
            ("deposit", 50.0),
            ("withdraw", 30.0),
            ("deposit", 25.0),
            ("withdraw", 45.0),
            ("deposit", 100.0)
        ]
        
        for operation, amount in transactions:
            if operation == "deposit":
                success, _, _ = ledger.deposit(amount)
                if success:
                    expected_balance += amount
            else:
                success, _, _ = ledger.withdraw(amount)
                if success:
                    expected_balance -= amount
        
        assert abs(ledger.get_balance() - expected_balance) < 0.001
    
    def test_zero_initial_deposit(self):
        """Testa criação de conta com depósito inicial zero."""
        ledger = MiniCoinLedger("Oscar", 0.0)
        
        assert ledger.get_balance() == 0.0
        
        # Não deve permitir retirada
        success, _, _ = ledger.withdraw(10.0)
        assert success is False
        
        # Deve permitir depósito
        success, _, _ = ledger.deposit(50.0)
        assert success is True
        assert ledger.get_balance() == 50.0


class TestEdgeCases:
    """Testes de casos extremos."""
    
    def test_large_amount(self):
        """Testa transações com valores grandes."""
        ledger = MiniCoinLedger("Patricia", 1000000.0)
        
        success, _, _ = ledger.deposit(5000000.0)
        assert success is True
        assert ledger.get_balance() == 6000000.0
    
    def test_small_amount(self):
        """Testa transações com valores pequenos."""
        ledger = MiniCoinLedger("Quinn", 100.0)
        
        success, _, _ = ledger.deposit(0.01)
        assert success is True
        assert abs(ledger.get_balance() - 100.01) < 0.001
    
    def test_exact_balance_withdrawal(self):
        """Testa retirada do saldo exato."""
        ledger = MiniCoinLedger("Rachel", 100.0)
        
        success, _, _ = ledger.withdraw(100.0)
        assert success is True
        assert ledger.get_balance() == 0.0
    
    def test_sequential_deposits(self):
        """Testa múltiplos depósitos sequenciais."""
        ledger = MiniCoinLedger("Steve", 100.0)
        
        for i in range(10):
            success, _, _ = ledger.deposit(10.0)
            assert success is True
        
        assert ledger.get_balance() == 200.0
        assert len(ledger.chain) == 11
    
    def test_sequential_withdrawals(self):
        """Testa múltiplas retiradas sequenciais."""
        ledger = MiniCoinLedger("Tina", 100.0)
        
        for i in range(5):
            success, _, _ = ledger.withdraw(10.0)
            assert success is True
        
        assert ledger.get_balance() == 50.0
        assert len(ledger.chain) == 6


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
