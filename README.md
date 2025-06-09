# Trabalho Prático 1

Esse repositório contém o primeiro trabalho prático desenvolvido para o curso de Algoritmos 2 - DCC207 (UFMG)

## Integrantes
- [Luis Henrique Gomes Higino](https://github.com/luishgh)
- [Victoria Oliveira dos Reis](https://github.com/Victoria-Reiss)

## Implementação

Toda a implementação foi realizada em Python 3.

### Processamento dos Dados

O processamento dos dados foi realizado em um notebook Jupyter, utilizando as seguintes bibliotecas:

- **pandas**: Utilizada para a manipulação e análise estruturada dos dados em DataFrames.
- **tqdm**: Empregada para exibir barras de progresso, permitindo o monitoramento de operações de longa duração.
- **re**: Módulo de expressões regulares, utilizado para limpeza e padronização de strings.
- **lib.utils**: Módulo customizado contendo funções auxiliares para serialização/desserialização de objetos (`.pkl`) e normalização de nomes.
- **lib.geoinfo**: Módulo customizado responsável por encapsular a lógica de requisição à API de geocodificação Nominatim OpenStreetMap.

Os dados analisados foram fornecidos pela Prefeitura de Belo Horizonte (PBH) e contêm informações sobre o tipo de comércio das empresas cadastradas.

### Etapas do Processamento:

1. **Leitura dos Dados**
   Realizamos a leitura inicial dos dados disponibilizados pela PBH.

2. **Padronização de Logradouros**
   Construímos um dicionário para mapear os tipos de logradouro utilizados pela PBH para os formatos reconhecidos pelo OpenStreetMap (OSM). Exemplos:

   * `AVE` → `AV`
   * `PCA` → `PC`

3. **Filtragem por Categoria**
   Filtramos os dados para considerar apenas estabelecimentos classificados como *bares* ou *restaurantes*.

4. **Formatação de Endereços**
   Formatamos os endereços de modo a adequá-los aos padrões aceitos pelo OSM, o que possibilitou consultas mais precisas à API.

5. **Criação de Identificadores Únicos**
   Para cada estabelecimento, criamos um identificador único, mesmo nos casos em que o CNPJ e o nome do proprietário fossem iguais. Isso foi necessário para distinguir, por exemplo, dois bares pertencentes ao mesmo dono, mas localizados em diferentes endereços.

6. **Geocodificação via Nominatim (OpenStreetMap API)**
   Utilizamos a biblioteca Nominatim para realizar a geocodificação dos endereços. Como a API permite apenas uma requisição por segundo, o processamento foi relativamente lento. Ainda assim, conseguimos obter coordenadas para a maioria dos estabelecimentos.

   Os casos em que a geocodificação falhou estavam, em geral, relacionados a divergências entre a forma como os endereços estavam registrados na PBH e no OSM — por exemplo, um endereço listado como "avenida" pela PBH, mas registrado como "rua" no OSM.
## 🔗 Junção dos Dados Geolocalizados com Dados da PBH

Após a geocodificação, os dados foram combinados com as informações tratadas da PBH. Isso permitiu agregar as coordenadas geográficas aos estabelecimentos comerciais classificados como bares e restaurantes.

---

## 🍽️ Processamento dos Dados do Comida di Buteco

Em um segundo notebook, desenvolvemos um script responsável por processar os dados do evento **Comida di Buteco**.
Inicialmente, tentamos utilizar a página fornecida pelo professor, porém ela não estava carregando corretamente os **detalhes dos pratos**. Por esse motivo, optamos por utilizar uma outra fonte.

### 📥 Coleta dos dados HTML do Comida di Buteco

Realizamos um **processo de web scraping** para extrair os dados da página.
O conteúdo foi processado para extrair as seguintes informações de cada bar participante:

* Nome do bar

* Endereço

* Nome do prato

* Descrição do prato

* Imagem do prato

Esses dados foram estruturados em um DataFrame, o que possibilitou a integração com os dados geolocalizados e tratados anteriormente.
Durante o processo de integração com os dados da PBH, enfrentamos dificuldades de correspondência entre os nomes dos bares. Isso aconteceu por motivos como:

* Troca na ordem dos nomes

* Omissão de partes do nome (ex: abreviações, etc.)

Devido a essas inconsistências, nem todos os bares puderam ser casados automaticamente com os registros da PBH.
Como solução, optamos por tratar manualmente os registros restantes, realizando ajustes nos nomes e combinando os dados para garantir a integridade das informações.

### Interface
## 🗺️ Interface Interativa com Mapa

Para visualizar os dados tratados e geolocalizados, desenvolvemos uma interface interativa utilizando **Dash**. Essa interface possibilita explorar visualmente os bares e restaurantes mapeados, além de destacar os participantes do concurso **Comida di Buteco**.

### 🧰 Bibliotecas Utilizadas

- **dash**: Utilizada para a criação da aplicação web interativa baseada em componentes do React, diretamente com Python.
- **dash_leaflet**: Responsável pela renderização do mapa interativo, permitindo plotar marcadores geográficos, layers e interações com o usuário.
- **dash_extensions**: Complementa o `dash_leaflet`, fornecendo componentes adicionais e suporte para eventos personalizados (como o retângulo de seleção).

### 🗺️ Mapa com Geolocalização

No mapa, todos os bares e restaurantes tratados aparecem com seus respectivos **marcadores geolocalizados**. Os pontos representam estabelecimentos que passaram pelo processamento e têm coordenadas obtidas via API do OpenStreetMap.

Além disso, realizamos uma **interseção** com os dados do evento **Comida di Buteco**:  
- Bares que participam do concurso são destacados com a **cor vermelha** e os outros bares estão destacados com **a cor azul**.  
- Ao clicar sobre esses pontos, são exibidas as **informações do prato** (nome e descrição), assim como a **imagem do prato** fornecida pelos próprios estabelecimentos.

### 🔍 Sistema de Busca com Retângulo

Implementamos também uma funcionalidade de **filtro geográfico por retângulo**:

- O usuário pode **desenhar um retângulo** sobre o mapa.
- A aplicação usa o **KDTree** para realizar buscas espaciais rápidas.
- Combinamos isso com a análise via **GeoJSON** para garantir que os **bares dentro do retângulo (incluindo as bordas)** sejam corretamente filtrados.
- Apenas os bares contidos nesse retângulo são exibidos ou destacados, facilitando a análise regional.

O filtro por retângulo utiliza a KDTree para identificar e exibir apenas os bares que estão dentro da interseção com o polígono desenhado. Sempre é considerado para a busca o último retângulo desenhado no mapa para determinar quais bares/restaurantes serão exibidos. Ao clicar sobre qualquer um dos ícones exibidos no mapa, são mostradas informações detalhadas sobre o bar/restaurante, como latitude e longitude, endereço e se participa ou não do concurso Comida di Buteco. Caso o estabelecimento participe desse evento, é exibido o nome do prato com a sua descrição e a imagem de como o prato é preparado.

Devido a limitações da biblioteca utilizada, não foi possível restringir facilmente a exibição para manter somente um retângulo visível no mapa. Por isso, embora a busca leve em conta apenas o último retângulo, os demais retângulos desenhados permanecem visíveis.
Para facilitar o uso, existe uma funcionalidade de "clear all", que permite apagar todos os retângulos do mapa e reiniciar a busca com uma área nova, garantindo flexibilidade no processo de filtragem. 

### Estrutura de Dados

Para a busca retangular, foi implementada a estrutura de dados [árvore k-d](https://pt.wikipedia.org/wiki/%C3%81rvore_k-d), no arquivo [lib/kdtree.py](lib/kdtree.py). Em particular, foi desenvolvida uma classe `KDTree` que recebe uma lista de pontos, o número de dimensões e uma função que recebe um ponto e retorna a coordenada referente à dimensão (0-indexada). Isso permitiu utilizar a estrutura independentemente do formato dos dados, o que foi útil para testar a estrutura com dados simplificados e, posteriormente, utilizá-la com os dados de interesse. Além disso, foi escolhido realizar a divisão dos dados nos nós de forma local: a cada nível, os dados são segregados conforme a mesma dimensão, mas a escolha do pivô é baseada em uma ordenação apenas dos pontos pelos quais aquele nó é responsável. Isso significa que é necessária uma nova ordenação a cada nó, em vez de uma única ordenação prévia e uma divisão baseada apenas em índices. A vantagem é que a árvore fica mais balanceada, pois uma divisão igual em todos os nós de um determinado nível pode resultar em ramos significativamente desiguais. Ademais, seria possível encontrar a mediana através de um algoritmo de [quick select](https://en.wikipedia.org/wiki/Quickselect), mas testes experimentais mostraram que a função nativa `sort` apresenta melhores resultados. Por fim, em vez de guardar os pontos apenas em folhas, cada nó possui um ponto que está localizado nele mesmo. Assim, garante-se que o número de nós armazenados em memória corresponde exatamente ao número de pontos.

