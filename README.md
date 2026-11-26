# SeparaPDF

Utilitário em Python para manipular PDFs pelo terminal: juntar, comprimir, separar, reorganizar e copiar páginas.

Nasceu de uma necessidade real: substituir o fluxo manual em ferramentas online (upload, ajuste e download a cada operação) por um programa simples e repetível.

## Funcionalidades

| Opção | Função | O que faz |
|---|---|---|
| 1 | Merging PDFs | Junta um segundo PDF ao final do primeiro |
| 2 | Compressing PDFs | Otimiza e comprime a estrutura do arquivo |
| 3 | Dividing PDFs | Extrai um intervalo de páginas para um novo PDF |
| 4 | Re-Arranging Pages | Move uma página para outra posição |
| 5 | Copying Pages | Copia uma página para uma posição (inclusive o final) |

O resultado é salvo com nome sequencial (`Document_001.pdf`, `Document_002.pdf`...), sem sobrescrever arquivos existentes.

## Requisitos

- Python 3.10 ou superior (usa `match/case`)
- [PyMuPDF](https://pymupdf.readthedocs.io/)

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
python main.py
```

## Exemplo de uso

```
Enter pdf file path: C:\Users\...\documento.pdf

---- *Functions* -----
1 - Merging PDFs
2 - Compressing PDFs
3 - Dividing PDFs
4 - Re-Arranging Pages
5 - Copying Pages
Enter function number: 5
Enter page to copy: 1
Enter position of the copy: 4
Done! Saved as Document_001.pdf
```

Entradas inválidas (página inexistente, arquivo que não é PDF, PDF com senha, número digitado errado) geram uma mensagem de erro clara e nenhum arquivo é criado.

## Decisões de projeto

- **Lógica separada da interface:** cada operação recebe o documento e devolve os bytes do PDF resultante. Só a função `main()` usa `input`, `print` e grava arquivos. Isso permite testar as operações isoladamente e reaproveitá-las em uma API.
- **Validação antes de processar:** páginas fora do intervalo geram um `PdfError` antes de qualquer alteração.
- **Nomes sequenciais:** evita perder arquivos gerados anteriormente.

## Próximos passos

- [ ] Testes automatizados com Pytest (casos válidos e de erro)
- [ ] Dividir a cada N páginas, gerando vários arquivos em um ZIP
- [ ] Pipeline de operações encadeadas (ex.: separar e clonar a página de assinatura em cada parte)
- [ ] Validação das instruções com Pydantic
- [ ] API com FastAPI (upload e download) e Docker
- [ ] Camada opcional com a API do Claude para interpretar instruções em linguagem natural
