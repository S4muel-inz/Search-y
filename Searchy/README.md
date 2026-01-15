## Search-Y

Uma ferramenta Python leve e eficiente para busca de arquivos e diretórios. Utiliza **Geradores (`yield`)** para garantir que o consumo de memória RAM permaneça baixo, mesmo ao escanear milhões de arquivos.

## ✨ Funcionalidades

- **Geradores Nativos**: Processa um arquivo por vez sem carregar listas gigantes na memória, tornando-o mais eficiente possivel.
- **Controle de Profundidade**: Argumento `depth` para limitar a recursividade.
- **Filtros Flexíveis**: Busca por arquivos, diretórios ou ambos, com suporte a padrões (Pattern matching).
- **Dados Completos**: Retorna dicionários com nome, tamanho (KB), datas de criação/modificação, seu caminho e tipo.

## 🚀 Como Usar:

### **Instalando a Biblioteca**:
```Bash
pip install Search-y    
```
### **Importando a Biblioteca**
Pode importar a biblioteca apenas passando seu nome
```Python
import searchy
```
### **Parametros**:
O searchy pode receber até 4 Parametros sendo apenas um deles obrigatorio e posicional:
- **Path** é o unico argumento é deve ser apresentado como uma String
```Python
searchy("C:/User/seuUsuario/seuCaminho") 
```
- **typeSearch**: é um parametro opcional que recebe uma *string* que defini quais tipos de arquivo serão buscados; 
    - Podendo ser *'dir'* para diretorios/pastas: 
     ```Python
     searchy('C:/', typesearch='dir'): #seram buscados apenas pastas/diretorios no caminho 'C:/'
     ```
    - Podendo ser *'file'* para arquivos:
    ```Python
     searchy('C:/', typesearch='file'): #seram buscados apenas arquivos nesse caso
    ```
    > [!WARNING] 
    >Se não for passado nenhum argumento no parametro **typeSearch** ele mostrara tudo encontrado:
    ```Python
     searchy('C:/'): #sera buscado tudo que tem na pasta 'C:/' 
     ```
    > [!WARNING] 
    >Mesmo se for passado um argumento que não existe

- **Pattern**: é um parametro opcional que funciona como um filtro de nomes sobre o resultado da busca:
```Python
 searchy('C:/', Pattern={'program', 'win', 'xbox'}): #sera buscado na pasta 'C:/' todos os arquivos e diretorios que tem 'program', 'win', 'xbox' no nome
```
> [!WARNING]
    > Para passar valores no Pattern esses itens devem ser uma *string* dentro do *set* do Pattern.
    >  ex: Pattern={'valor1', 'valor2', 'valor3'}

- **Depth**: é um parametro opcional que recebe um valor *int* que determina quantas subpastas serão buscadas tambem:
```Python
searchy('C:/', Depth=2): #toda pasta que ele achar no caminho que você passou ele ira abrir, e assim por diante de acordo com o valor do *depth*
```
>[!TIP]
>Passar valores maiores no **Depth** tambem resultara em listas mais longas, mas o tempo de procura será o mesmo


## 🌊 **Resultado Da Função**:
* **Retorno**: A função retorna um gerador de dicionários. Cada dicionário representa um arquivo ou diretório, contendo as seguintes chaves:

| Chave | Descrição |
| :--- | :--- |
| **name** | Nome do *arquivo* ou *pasta* |
| **size_kb** | Tamanho convertido para Kilobytes |
| **modification** | Data de modificação (DD/MM/AAAA) |
| **creation** | Data de criação (DD/MM/AAAA) |
| **full_path** | Caminho absoluto no sistema |
| **type_entry** | Identifica se é *'file'* ou *'directory'* |

- 🧪 **Testes**
Este projeto utiliza pytest. Para rodar os testes, no terminal:
```Bash
pytest
```