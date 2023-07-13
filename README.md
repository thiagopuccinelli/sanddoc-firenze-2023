# Repositório do Projeto de Doutorado Sanduíche "EFEITOS DA MATRIZ EXTRACELULAR NA ATIVIDADE ENZIMÁTICA: UM MODELO COMPUTACIONAL" realizado em Firenze, Itália em 2023.

Neste repositório, encontram-se todos os script utilizados para desenvolver o Projeto de Doutorado Sanduíche financiado pela CAPES no ano de 2023. Os códigos utilizados para desenvolvimento dos scripts estão em FORTRAN90, Python e LAMMPS. Este é uma linguagem específica do pacote de simulações LAMMPS [1]. Tal pacote é distribuído gratuitamente pelos laboratórios Sandia, através do link (https://www.lammps.org/). O LAMMPS é um código clássico de dinâmica molecular (MD) que modela conjuntos de partículas num estado líquido, sólido ou gasoso. Pode modelar sistemas atómicos, poliméricos, biológicos, de estado sólido (metais, cerâmicas, óxidos), granulares, de granulação grossa ou macroscópicos, utilizando uma variedade de potenciais interatómicos (campos de força) e condições de fronteira. Pode modelar sistemas 2d ou 3d com tamanhos que vão desde apenas algumas partículas até milhares de milhões.

No sentido mais geral, o LAMMPS integra as equações de movimento de Newton para um conjunto de partículas em interação. Uma partícula pode ser um átomo, uma molécula ou um eletron, um aglomerado de átomos de "coarse-grained", ou um aglomerado de material mesoscópico ou macroscópico. Os modelos de interação que o LAMMPS inclui são, na sua maioria, de curto alcance; estão também incluídos alguns modelos de longo alcance.

O LAMMPS usa listas de vizinhos para manter o registo das partículas próximas. As listas são optimizadas para sistemas com partículas que são repulsivas a curtas distâncias, de modo a que a densidade local de partículas nunca se torne demasiado grande. Isto contrasta com os métodos utilizados para modelar plasma ou corpos gravitacionais (como a formação de galáxias).

Em máquinas paralelas, o LAMMPS usa técnicas de decomposição espacial com paralelização MPI para particionar o domínio de simulação em subdomínios de igual custo computacional, um dos quais é atribuído a cada processador. Os processadores comunicam e armazenam informações de átomos "fantasmas" para átomos que fazem fronteira com o seu subdomínio. A paralelização multi-threading e a aceleração GPU com decomposição de partículas podem ser utilizadas adicionalmente.

Referências: 
[1] Steve Plimpton. Fast parallel algorithms for short-range molecular dynamics. Journal of
computational physics, 117(1):1–19, 1995.

