# Memória do Projeto

## Contexto

O projeto permite configurar a quantidade de alunos e avaliações usando Python procedural e Tkinter.

## Decisões arquiteturais

- `alunos` é a lista dimensionada pela quantidade configurada.
- `notas` é a matriz dimensionada por alunos e avaliações.
- A linha `i` da matriz pertence ao aluno `i` do vetor.
- A média mínima e a nota máxima são informadas no início de cada turma.
- A validação aceita somente notas entre `0` e a nota máxima configurada.
- A interface usa `tkinter.ttk` e `ttk.Treeview` para exibir os resultados.
- Canvas e barras de rolagem acomodam formulários e resultados grandes.
- A janela modal de configurações usa `tk.Toplevel()` e mantém valores temporários até o salvamento.
- Alterações dimensionais confirmadas recriam formulário e tabela; dados preenchidos geram aviso antes do descarte.
- A solução evita classes próprias, mantendo o paradigma procedural solicitado.

## Fluxo principal

1. A interface solicita as configurações da turma.
2. `criar_formulario_dinamico()` cria os campos conforme as quantidades escolhidas.
3. `ler_dados()` valida nomes e notas e atualiza lista/matriz.
4. `calcular_resultados()` percorre os dados, calcula médias e classifica os alunos.
5. O resumo da turma é atualizado na própria janela.
6. `limpar_formulario()` zera os dados e `nova_turma()` permite reconfigurar a turma.
