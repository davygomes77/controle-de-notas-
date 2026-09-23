# Memória do Projeto

## Contexto

O projeto registra notas de cinco alunos em três avaliações usando Python procedural e Tkinter.

## Decisões arquiteturais

- `alunos` é o vetor de cinco posições com os nomes.
- `notas` é a matriz de cinco linhas por três colunas.
- A linha `i` da matriz pertence ao aluno `i` do vetor.
- A média mínima para aprovação é `6.0`.
- A validação aceita somente notas entre `0` e `10`.
- A interface usa `tkinter.ttk` e `ttk.Treeview` para exibir os resultados.
- A solução evita classes próprias, mantendo o paradigma procedural solicitado.

## Fluxo principal

1. A interface cria os campos para os cinco alunos.
2. `ler_dados()` valida nomes e notas e atualiza vetor/matriz.
3. `calcular_resultados()` percorre os dados, calcula médias e classifica os alunos.
4. O resumo da turma é atualizado na própria janela.
5. `limpar_formulario()` zera os dados para um novo preenchimento.
