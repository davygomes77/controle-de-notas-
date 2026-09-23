# Controle de Notas da Turma

Aplicação desktop em Python para registrar cinco alunos, três avaliações por aluno e acompanhar médias e situações acadêmicas.

## Funcionalidades

- Cadastro de cinco nomes em um vetor de cinco posições.
- Cadastro de três notas por aluno em uma matriz `5 x 3`.
- Validação de notas no intervalo de `0` a `10`.
- Cálculo da soma, média e situação individual.
- Aprovação para médias maiores ou iguais a `6,0`.
- Resumo com média da turma, aprovados, reprovados, maior e menor média.
- Botão **Limpar** para iniciar um novo preenchimento.
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

## Estrutura

- `main.py`: aplicação principal.
- `MEMORY.md`: decisões e contexto arquitetural.
- `ROADMAP.md`: planejamento de evolução.
- `ia/Prompt Python-1.md`: prompt pedagógico utilizado como diretriz.
