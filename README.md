  
# Desafio: Explorando Ranqueamento através da Ciência de Dados em Grafos no Campeonato Brasileirão

Na apresentação, discutimos como a ciência de dados em grafos emergiu entre os séculos 18 e 19 para resolver desafios como detectar conluios entre enxadristas, ajudando a decidir quem deveria receber a maior parcela do prêmio. Este problema se estende além do xadrez e encontra relevância na matemática e, atualmente, na ciência dos dados: como ranquear entidades de forma justa e precisa?

Neste desafio, vamos explorar o campeonato Brasileirão: 
- investigar como diferentes métodos de ranqueamento, além do tradicional sistema de pontos acumulados, podem influenciar os resultados, alterando os vencedores e/ou rebaixados
- Vamos simular concluios entre times e avaliar quão robusto são os métodos para manter vencedores e rebaixados inaleterados
- Vamos fazer um shuffle e depois deletar X% das partidas e refazer a primeira análise

# Passos do Desafio:


    
## Data preparation
### Download dos dados

Baixe os dados do Campeonato Brasileirão dos últimos anos. Você pode encontrar estes dados em repositórios públicos ou sites especializados em estatísticas de futebol.

```python
# Construa seu código aqui usando esse site
```
### Data cleaning

Limpe e estruture os dados de forma que facilite a análise. Por exemplo, certifique-se de que os dados estejam completos, consistentes e no formato adequado.


### Construção do grafo

```python
# Você pode usar o networkx se prefereir ou o numpy
# o objetivo é ter uma representacao matricial ou de arestas do seu grafo

# Exemplo de código usando networkx
import networkx as nx

def build_graph(dados) -> nx.DiGraph
	# Criando um grafo direcionado
	G = nx.DiGraph()
	
	# Adicionando arestas ao grafo a partir dos dados das partidas
	for index, row in dados.iterrows():
	    G.add_edge(row['time_casa'], row['time_visitante'], weight=row['gols_casa'] - row['gols_visitante'])
	
	return G

```


# Métodos


## Ranqueamento


### Contagem de pontos

```python
# implemente uma função que receba seu grafo e retorne um score de ranqueamento para cada time
```

### Sua escolha

Exemplos de métodos:
- autovetor
- page-rank
- centralidade do vértice

```python
# implemente uma função que receba seu grafo e retorne um score de ranqueamento para cada time
```



## Mensurar e comparar ranqueamentos



### Plots

