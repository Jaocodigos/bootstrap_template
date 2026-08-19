"""
bots/pdf_bot/main.py
Modelo de exemplo 2: busca uma palavra dentro de um PDF, destaca as
ocorrencias encontradas e salva uma copia do PDF com o destaque.
 
Roda dentro do venv proprio do pdf_bot (criado e populado pelo bootstrap.py).
Chamado como: python main.py <ambiente>
"""
 
import os
import sys
 
import fitz  # pacote pymupdf
 
PASTA_ENTRADA = "input"
PASTA_SAIDA = "output"
ARQUIVO_PDF = "20240625LG.pdf"
PALAVRA_BUSCADA = "expediente"
 
 
def buscar_palavra_no_pdf(caminho_arquivo: str, palavra: str):
    documento = fitz.open(caminho_arquivo)
    ocorrencias = []
 
    for pagina_num in range(len(documento)):
        pagina = documento.load_page(pagina_num)
        instancias = pagina.search_for(palavra)
        for inst in instancias:
            ocorrencias.append({"page": pagina_num + 1, "bbox": inst})
 
    return ocorrencias, documento
 
 
def destacar_ocorrencias(documento: "fitz.Document", ocorrencias: list) -> None:
    for ocorrencia in ocorrencias:
        pagina = documento.load_page(ocorrencia["page"] - 1)
        pagina.add_highlight_annot(ocorrencia["bbox"])
 
 
def executar(ambiente: str = "DEV") -> None:
    caminho_entrada = os.path.join(PASTA_ENTRADA, ARQUIVO_PDF)
 
    if not os.path.exists(caminho_entrada):
        raise FileNotFoundError(f"PDF nao encontrado: {caminho_entrada}")
 
    print(f"[pdf_bot] Ambiente={ambiente} | Buscando '{PALAVRA_BUSCADA}' em {caminho_entrada}...")
 
    ocorrencias, documento = buscar_palavra_no_pdf(caminho_entrada, PALAVRA_BUSCADA)
 
    if not ocorrencias:
        print(f"[pdf_bot] Nenhuma ocorrencia de '{PALAVRA_BUSCADA}' encontrada.")
        documento.close()
        return
 
    for ocorrencia in ocorrencias:
        print(f"[pdf_bot] Encontrada na pagina {ocorrencia['page']} na posicao {ocorrencia['bbox']}")
 
    destacar_ocorrencias(documento, ocorrencias)
 
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    caminho_saida = os.path.join(PASTA_SAIDA, "arquivo_destacado.pdf")
    documento.save(caminho_saida)
    documento.close()
 
    print(f"[pdf_bot] Arquivo com a palavra destacada salvo em: {caminho_saida}")
 
 
if __name__ == "__main__":
    ambiente_arg = sys.argv[1] if len(sys.argv) > 1 else "DEV"
    executar(ambiente_arg)