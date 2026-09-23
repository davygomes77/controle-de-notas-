# Controle de Notas da Turma

Aplicação desktop em Python para configurar uma turma, registrar alunos e avaliações e acompanhar médias e situações acadêmicas.

## Funcionalidades

- Configuração da quantidade de alunos e avaliações pela interface.
- Configuração da nota máxima e da média mínima para aprovação.
- Cadastro dos nomes em uma lista dimensionada conforme a turma.
- Cadastro das notas em uma matriz com dimensões definidas pelo usuário.
- Validação de notas no intervalo de `0` até a nota máxima configurada.
- Cálculo da soma, média e situação individual.
- Aprovação para médias maiores ou iguais à média mínima configurada.
- Resumo com média da turma, aprovados, reprovados, maior e menor média.
- Botão **Limpar** para iniciar um novo preenchimento.
- Botão **Nova Turma** para alterar todas as configurações.
- Botão **Configurações** para alterar os parâmetros sem fechar a janela principal.
- Confirmação antes de descartar dados ao mudar dimensões da turma.
- Barras de rolagem para tabelas com muitos alunos ou avaliações.
- Interface nativa construída com `tkinter` e `tkinter.ttk`.

## Requisitos

- Python 3.10 ou superior.
- Tkinter, geralmente incluído na instalação padrão do Python para Windows.

## Execução

No terminal, dentro desta pasta, execute:

```bash
python main.py
```

## Organização pedagógica

O programa usa funções procedurais, listas como vetor/matriz, decisões condicionais e laços de repetição. Não há classes criadas pelo projeto. Os comentários no código relacionam as etapas com sequência, seleção e repetição.

A janela **Configurações da Turma** é modal e apresenta os valores atuais. `Salvar Configurações` valida e aplica as alterações; `Cancelar` preserva o estado anterior; `Restaurar Padrão` preenche os valores originais de 5 alunos, 3 avaliações, nota máxima 10 e média mínima 6.

## Estrutura

- `main.py`: aplicação principal.
- `MEMORY.md`: decisões e contexto arquitetural.
- `ROADMAP.md`: planejamento de evolução.
- `ia/Prompt Python-1.md`: prompt pedagógico utilizado como diretriz.
