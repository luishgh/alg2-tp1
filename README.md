# Trabalho Prático 1

Esse repositório contém o primeiro trabalho prático desenvolvido para o curso de Algoritmos 2 - DCC207 (UFMG)

## Integrantes
- [Luis Henrique Gomes Higino](https://github.com/luishgh)
- [Victoria Reis](https://github.com/Victoria-Reiss)

## Implementação

Toda a implementação foi realizada em Python 3.

### Interface
O app interativo foi desenvolvido utilizando a biblioteca...

### Estrutura de Dados

Para a busca retangular, foi implementada a estrutura de dados [árvore k-d](https://pt.wikipedia.org/wiki/%C3%81rvore_k-d), no arquivo [lib/kdtree.py](lib/kdtree.py). Em particular, foi desenvolvida uma classe `KDTree` que recebe uma lista de pontos, o número de dimensões e uma função que recebe um ponto e retorna a coordenada referente à dimensão (0-indexada). Isso permitiu utilizar a estrutura independentemente do formato dos dados, o que foi útil para testar a estrutura com dados simplificados e, posteriormente, utilizá-la com os dados de interesse. Além disso, foi escolhido realizar a divisão dos dados nos nós de forma local: a cada nível, os dados são segregados conforme a mesma dimensão, mas a escolha do pivô é baseada em uma ordenação apenas dos pontos pelos quais aquele nó é responsável. Isso significa que é necessária uma nova ordenação a cada nó, em vez de uma única ordenação prévia e uma divisão baseada apenas em índices. A vantagem é que a árvore fica mais balanceada, pois uma divisão igual em todos os nós de um determinado nível pode resultar em ramos significativamente desiguais. Ademais, seria possível encontrar a mediana através de um algoritmo de [quick select](https://en.wikipedia.org/wiki/Quickselect), mas testes experimentais mostraram que a função nativa `sort` apresenta melhores resultados. Por fim, em vez de guardar os pontos apenas em folhas, cada nó possui um ponto que está localizado nele mesmo. Assim, garante-se que o número de nós armazenados em memória corresponde exatamente ao número de pontos.

