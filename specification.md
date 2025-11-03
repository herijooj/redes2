# Universidade Federal do Paraná
## Departamento de Informática
## Bacharelado em Ciência da Computação
## Prof. Elias P. Duarte Jr.

# Trabalho Prático de Redes de Computadores II - Turma 2025/2

# MiniCoin: Uma Moeda Virtual Baseada em Blockchain

## Entrega
Todos os trabalhos deverão estar disponibilizados até sexta-feira dia 14 de novembro de 2025; não serão aceitos trabalhos disponibilizados após esta data. Atenção, são mais de 3 semanas de prazo, organize-se! Termine antes da data limite!

Os alunos devem informar por e-mail a URL do trabalho, usando o subject "TP REDES II 2025-2"

O trabalho deve ser feito em dupla; o código, os testes e o relatório devem ser feitos por ambos os membros da dupla. Use esta oportunidade para melhorar sua habilidade de trabalhar em equipe.

## Descrição do Trabalho

Neste trabalho você vai implementar uma moeda virtual, a MiniCoin. A MiniCoin é baseada em blockchain, mas para simplificar a execução do trabalho, que tem que ser entregue em 3 semanas, apenas 1 servidor mantém toda a blockchain. A blockchain deve implementada como uma sequência encadeada de registros de movimentações de uma conta de MiniCoins.

O primeiro registro da lista encadeada tem o valor do depósito inicial, além do nome do proprietário e a data e hora em que a conta foi criada. Um campo adicional corresponde ao hash do registro. Cada dupla tem a liberdade para definir qual função hash vai usar.

A cada movimentação da conta (que pode ser ou um depósito ou uma retirada) um novo registro é adicionado à lista encadeada. Este registro tem: o a operação realizada na conta de MiniCoins, mais um hash. Só que desta vez o hash é gerado com o registro atual mais o hash do registro anterior.

Simule a chegada de solicitações de retiradas válidas e inválidas. Nas válidas deve ser possível fazer uma retirada ou depósito. Nas inválidas há a tentativa de fazer uma retirada maior que o saldo da conta de MiniCoins.

Cada dupla pode fazer a implementação na linguagem que escolher, como Python, C, C++, Java ou qualquer outra linguagem.

## ENTREGA DO TRABALHO
Deve ser construída uma página Web, que contém em documentos HTML, os seguintes itens:

- Relatório de como foi feito o trabalho e quais foram os resultados obtidos. Use desenhos, diagramas, figuras, todos os recursos que permitam ao professor compreender como a dupla estruturou o trabalho e quais resultados obteve. O objetivo é o professor entender como a dupla fez o trabalho, como o trabalho funciona.
- Código Fonte comentado. ATENÇÃO: acrescente a todo programa a terminação ".txt" para que possa ser diretamente aberto em um browser. Exemplos: cliente.py.txt ou servidor.c.txt
- Logs de execução dos processos cliente/servidores, que demonstrem a execução correta destes processos. Os testes devem ser exaustivos até o ponto que demonstrem com clareza a funcionalidade correta do sistema. 

## Observações

- Não serão aceitos trabalhos impressos, nem em meio ótico/magnético.
- Como neste semestre a turma não está grande, todos os trabalhos serão defendidos no laboratório, portanto certifique-se que seu trabalho funciona aqui.
- Pode ser usada qualquer linguagem de programação. A diversidade é bem vinda! 

Prof. Elias P. Duarte Jr.     Departamento de Informática     UFPR