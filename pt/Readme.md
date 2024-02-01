# Encontrar uma rota viável utilizando o Vizinho Mais Próximo, o Recozimento Simulado e algumas heurísticas para competições FLL.

### Este projeto é realizado com a assistência da equipe Delta de São João Nepomuceno.

## O algoritmo tenta otimizar 3 variáveis alvo

- Complexidade de uma execução (à medida que o número de missões em uma execução aumenta, a complexidade da construção das ferramentas para essa execução também cresce)
- Tempo de uma execução
- Pontuação de uma execução

## Vizinho Mais Próximo

A rota inicial (ponto de partida para otimização SA) é gerada usando a heurística do vizinho mais próximo, que consiste em selecionar a missão mais próxima com base na posição atual.

## Recozimento Simulado

O Recozimento Simulado é um algoritmo de otimização probabilístico inspirado no processo de recozimento na metalurgia. O processo de recozimento envolve o aquecimento de um material a uma alta temperatura e, em seguida, resfriamento gradual para remover defeitos e otimizar sua estrutura. Da mesma forma, o recozimento simulado é usado para encontrar uma solução aproximada para um problema de otimização, explorando o espaço de soluções e aceitando movimentos ocasionalmente subótimos para escapar de mínimos locais.

- Inicialização: Comece com uma solução inicial para o problema de otimização. Isso pode ser gerado aleatoriamente ou por meio de alguma heurística.

- Controle de Temperatura: O recozimento simulado mantém um parâmetro de temperatura que controla a probabilidade de aceitar soluções piores. A temperatura é inicialmente definida alta e é gradualmente reduzida ao longo do tempo. Em temperaturas mais altas, o algoritmo é mais propenso a aceitar soluções piores, permitindo a exploração do espaço de soluções.

- Busca de Vizinhança: Em cada iteração, uma solução vizinha é gerada. A vizinhança pode ser definida de várias maneiras, dependendo do problema. Pode envolver pequenas alterações ou perturbações na solução atual.

- Avaliação: A qualidade da nova solução é avaliada usando uma função objetiva. Se a nova solução for melhor do que a atual, ela é aceita. Se for pior, o algoritmo ainda pode aceitá-la com uma certa probabilidade determinada pela temperatura e pela extensão da degradação na qualidade da solução.

- Recozimento da Temperatura: A temperatura é reduzida gradualmente de acordo com uma programação predefinida. À medida que a temperatura diminui, o algoritmo se torna menos tolerante a soluções piores, concentrando-se mais na exploração do que na exploração.

- Término: O processo continua até que um critério de término seja atendido, como atingir uma temperatura alvo ou um número máximo de iterações.

Planejo aprimorar o projeto no futuro, aprimorando as heurísticas e otimizando o desempenho/qualidade do código ao longo das temporadas. Vale ressaltar que o código está protegido pela GPL (Licença Pública Geral GNU), e os termos podem ser encontrados em [GPL](https://www.gnu.org/licenses/gpl-3.0.en.html).
