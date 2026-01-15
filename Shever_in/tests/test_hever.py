from unittest.mock import patch, MagicMock
import pytest
import os
import hever  # Ajuste o nome do import para o seu arquivo

@pytest.fixture
def fs_setup(tmp_path):
    """
    Cria uma estrutura de pastas temporária
    /root
        /pasta_a
            arquivo_a.txt
            arquivo_raiz.txt
            imagem_raiz.png
    """
    # Arquivos na raiz
    (tmp_path / "arquivo_raiz.txt").write_text("conteudo")
    (tmp_path / "imagem_raiz.png").write_text("dados")
    
    # Subdiretório e arquivo dentro
    pasta_a = tmp_path / "pasta_a"
    pasta_a.mkdir()
    (pasta_a / "arquivo_a.txt").write_text("texto")
    
    return tmp_path

# 1. Teste de Profundidade (Depth)
def test_hever_depth_zero(fs_setup):
    # Depth 0: Deve ver apenas o que está na raiz (2 arquivos + 1 pasta)
    resultado = list(hever(str(fs_setup), depth=0))
    nomes = [item["name"] for item in resultado]
    
    assert len(resultado) == 3
    assert "arquivo_raiz.txt" in nomes
    assert "pasta_a" in nomes
    assert "arquivo_a.txt" not in nomes  # Está no subdiretório

def test_hever_depth_one(fs_setup):
    # Depth 1: Deve ver a raiz e entrar um nível (deve achar o arquivo_a.txt)
    resultado = list(hever(str(fs_setup), depth=1))
    nomes = [item["name"] for item in resultado]
    
    assert "arquivo_a.txt" in nomes

# 2. Teste de Tipo (typehever)
def test_hever_filter_files(fs_setup):
    # Filtra apenas por arquivos (singular)
    resultado = list(hever(str(fs_setup), typehever="file", depth=1))
    for item in resultado:
        assert item["type"] == "file"
    
    nomes = [item["name"] for item in resultado]
    assert "pasta_a" not in nomes

def test_hever_filter_dirs_plural(fs_setup):
    # Filtra apenas por diretórios (plural)
    resultado = list(hever(str(fs_setup), typehever="dirs", depth=1))
    assert len(resultado) == 1
    assert resultado[0]["name"] == "pasta_a"
    assert resultado[0]["type"] == "directory"

# 3. Teste de Padrão (Pattern)
def test_hever_pattern_match(fs_setup):
    # Busca apenas quem tem "imagem" no nome
    resultado = list(hever(str(fs_setup), Pattern={"imagem"}))
    assert len(resultado) == 1
    assert resultado[0]["name"] == "imagem_raiz.png"

def test_hever_pattern_case_insensitive(fs_setup):
    # Busca com letra maiúscula para testar o lower()
    resultado = list(hever(str(fs_setup), Pattern={"ARQUIVO"}))
    # Deve achar 'arquivo_raiz.txt' e 'arquivo_a.txt' (se depth fosse maior)
    # Como o padrão é depth=0, acha só o da raiz
    nomes = [item["name"] for item in resultado]
    assert "arquivo_raiz.txt" in nomes

# 4. Teste da Estrutura do Dicionário
def test_hever_dict_structure(fs_setup):
    resultado = list(hever(str(fs_setup), depth=0))
    item = resultado[0]
    
    chaves_esperadas = {"name", "size_kb", "modification", "creation", "path", "type"}
    assert chaves_esperadas.issubset(item.keys())
    assert isinstance(item["size_kb"], float)
    assert "/" in item["modification"]  # Formato dd/mm/yyyy e o esperado
    
    # 1. Testando Erro de Permissão (PermissionError) ======= nao tinha funcionado ai fiz o que deu pra corrigir
def test_hever_permission_error(tmp_path):
    # Criamos uma pasta real
    pasta = tmp_path / "pasta_bloqueada"
    pasta.mkdir()
    
    # Vamos simular que o scandir trava ao tentar abrir essa pasta
    # O 'patch' substitui temporariamente o os.scandir real pelo nosso ator legal(funciona pelo amor de d'us)
    with patch("os.scandir") as mock_scandir:
        mock_scandir.side_effect = PermissionError("Acesso negado")
        
        # O resultado deve ser um gerador vazio, e NÃO deve travar o programa
        resultado = list(hever(str(pasta)))
        
        assert len(resultado) == 0
        mock_scandir.assert_called_once()

# 2. Testando OSError durante o processamento de um arquivo
def test_hever_os_error_handling(tmp_path, capsys):
    # Criamos um arquivo real
    f = tmp_path / "arquivo_problematico.txt"
    f.write_text("conteudo")
    
    # Criamos um objeto ator para tentar uma entrada do scandir
    mock_entry = MagicMock()
    mock_entry.name = "arquivo_problematico.txt"
    mock_entry.path = str(f)
    mock_entry.is_dir.return_value = False
    mock_entry.is_file.return_value = True
    # Fazemos o stat() desse arquivo dar um erro de Disco
    mock_entry.stat.side_effect = OSError("Falha física no disco")
    
    # Simulamos o scandir devolvendo esse arquivo problemático (dessa vez vai)
    with patch("os.scandir") as mock_scandir:
        # O mock_scandir quando usado com 'with' (context manager)
        mock_scandir.return_value.__enter__.return_value = [mock_entry]
        
        resultado = list(hever(str(tmp_path)))
        
        # O item não deve ser adicionado (pois o stat falhou)
        assert len(resultado) == 0
        
        # Capturamos o que foi impresso no terminal (o seu print(f"{err}..."))
        captured = capsys.readouterr()
        assert "Falha física no disco" in captured.out