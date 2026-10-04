# Caçando bugs em Python: do olho humano à IA

## Introdução

### Olá

Boa tarde a todas e a todos! Meu nome é Daniel e esta é a palestra "Caçando bugs em Python: do olho humano à IA".

Gostaria de agradecer a vocês por participarem da palestra. E também gostaria de me apresentar.

### Quem sou

Minhas qualificações, em ordem de importância:

- Sou pai do **Pedro**, que tem 12 anos e está aqui conosco
- Sou **biólogo** e exerço a profissão
- Sou Programador **Amador** de Python há mais de 20 anos, nunca atuei profissionalmente na área de tecnologia
- Faço parte de dois times **oficiais** do Python: **Triage Team** que faz triagem de bugs no GitHub do CPython
- E **Fuzzing Team**, grupo voltado ao fuzzing do CPython, a gente vai ver o que é fuzzing daqui a pouco
- Sou um **caçador de bugs**, interessado em ajudar projetos a serem mais robustos encontrando falhas neles

Há quase 20 anos eu procuro problemas em projetos Python. Hoje quero mostrar algumas coisas que aprendi fazendo isso.

## Um breve paralelo

E existe uma coincidência curiosa entre essas duas partes da minha vida. Na biologia eu trabalho com fauna. Na programação, eu caço bugs. E as duas atividades se parecem mais do que a gente imagina. Por isso, convido vocês a passearem por um **paralelo** entre biologia e programação.

Imagine que você está na natureza, numa mata desconhecida, nunca estudada. Você sabe que existem animais ali. Só não sabe quais. Nem onde. Com bugs é a mesma coisa: eles existem. A pergunta é: quais? E onde?

Existem diversas formas de descobrir quais animais estão presentes, mas ocultos, naquele lugar.

Você pode fazer uma **simples observação**: está lá esperando o que vai aparecer e, do nada, **PÁ, CAPIVARA**.

Você pode **procurar por indícios e pistas**, como pegadas, tocas ou ninhos.

Ou você pode, por exemplo, colocar **câmeras automáticas** com diversos tipos de isca para registrar animais que forem lá comer.

Com os bugs, a simples observação é o que chamamos de **revisão manual do código**: procuramos os bugs ativamente, mas sem técnicas ou ferramentas específicas para ajudar.

Procurar por indícios corresponde à **análise estática**, uma técnica que tenta encontrar partes do código que estejam seguindo padrões que geralmente resultam em bugs.

E tentar atrair animais com iscas diferentes parece com o **fuzzing**, técnica na qual alimentamos programas com inputs de diversos tipos, tentando que algum deles faça um bug oculto se mostrar.

Agora imagine **uma equipe** de pessoas biólogas. Uma procura mamíferos. Outra, aves. Outra, répteis. Todas investigam a mesma mata, ao mesmo t empo, mas cada uma procurando **coisas diferentes**.

É assim que os agentes de IA trabalham: cada um caça uma classe específica de bug. Um procura problemas de memória. Outro, de concorrência. Outro, de erros de API.

## Spoilers

Bom, para adiantar o que um esforço de caça aos bugs pode encontrar, eu gostaria de dar spoilers sobre uma campanha recente de caça aos bugs baseada em IA, focando tanto no CPython quanto no ecossistema de extensões Python em C e C++.

Essa campanha começou em março deste ano, e nela eu utilizei ferramentas que serão detalhadas em breve.
Nesse período, foram encontrados 55 bugs distintos no código do CPython.
Além disso, foram analisadas 50 extensões Python em C e C++. Nelas, foram apontados cerca de 690 problemas em nível de correção, dos quais mais de 215 possuem exemplos de reprodução: um pequeno script que demonstra o crash ou o comportamento inesperado do código. Depois de deduplicar, confirmar e reportar, esses achados viraram 138 bugs distintos registrados nos projetos. Uma análise específica de free threading, cobrindo 18 extensões, ainda mapeou mais de 4.500 corridas de dados potenciais e mais de 30 crashes reproduzíveis.

Antes da virada para ferramentas baseadas em IA, uma campanha de fuzzing tradicional do CPython em 2024-2025 já tinha rendido 52 issues, incluindo release blockers, que são bugs tão severos que uma nova versão do Python só pode ser lançada depois de consertá-los. Um fuzzer mais recente, focado no JIT experimental do Python, já encontrou 28 bugs distintos.

Espero que esses resultados tenham despertado curiosidade sobre como encontrar esses bugs, porque é isso que veremos agora.

## Técnicas

Vamos ver quatro abordagens.

Primeiro, o olho humano: revisão manual.

Depois, ferramentas que procuram padrões: análise estática.

Depois, programas que provocam o software: fuzzing.

E finalmente IA, que mistura características das três anteriores.

### Revisão Manual de Código

Pois bem. Começando pela revisão manual de código, frequentemente empregada pelas pessoas mantenedoras nos seus projetos, ou por quem tem que resolver problemas encontrados na execução do software.

Essa técnica corresponde à observação simples na busca por animais. Você está lá olhando o código e PÁ, CAPIVARA.

Eu gosto de chamar de Desenvolvimento Guiado por Uai, porque o que acontece é que você olha pro código e pensa "UAI! o código tá errado aqui!". Pode ser guiado por UÉ, por É O QUÊ??, por ÔXI, varia.

Nessa técnica, as regras geralmente ficam armazenadas nas cabeças das pessoas desenvolvedoras e sua aplicação depende de olhar afiado para encontrar problemas.

Isso requer experiência e faro.

Quando feita por alguém que conhece bem o domínio, talvez seja a técnica capaz da análise mais profunda. Mas, até por isso, também é a mais demorada e não é escalável. Ou seja, não é uma boa técnica para cobrir grandes quantidades de código rapidamente.

### Análise Estática

Tem esse nome porque analisa o código sem executá-lo, utilizando ferramentas que procuram padrões de código que indicam possíveis bugs.

Esta técnica corresponde à procura por indícios da presença de animais. Você está buscando as pegadas dos bugs.

Cada ferramenta tem uma forma de consumir e analisar o código. Pode fazer um parse, usar expressões regulares, etc. e tenta identificar trechos do código que correspondem a regras pré-definidas. Estas regras em geral são configuráveis e muitas vezes podem ser acrescidas de regras personalizadas pela pessoa usuária. Então, em vez de depender da memória e do olhar da pessoa desenvolvedora para encontrar possíveis bugs, a análise estática baseia-se em padrões de código que são identificados automaticamente pelas ferramentas, podendo ser executada em grande escala.

Ela troca parte da profundidade da revisão manual por escala: consegue varrer muito código rapidamente, mas produz resultados que ainda precisam do olhar humano, especialmente para separar falsos positivos. Ou seja, é capaz de lidar com grandes quantidades de código rapidamente, mas sem o detalhamento e confiabilidade da revisão manual.

### Fuzzing

Fuzzing é uma técnica baseada em gerar e fornecer grandes quantidades de inputs, inclusive inesperados, extremos ou inválidos, e observar como o software reage.

Como o software é executado com esses inputs, é uma forma de análise dinâmica.

Esta técnica corresponde às câmeras com diferentes iscas para atrair animais. Você oferece inputs e vê se atraem algum bug.

No fuzzing, em vez de procurar diretamente por padrões de código problemáticos, o fuzzer gera ou modifica inputs, muitas vezes com uma parte aleatória e com um mecanismo de feedback.

Há duas ideias importantes aí: aleatoriedade e feedback.

A aleatoriedade ajuda o fuzzer a experimentar coisas que nós talvez não imaginaríamos.

O feedback mostra quais dessas tentativas parecem interessantes, por exemplo, porque alcançaram uma parte nova do código, e ajuda a escolher as próximas.

Com o fuzzing, é possível encontrar em larga escala bugs que outras técnicas não alcançam. 

Uma vantagem é que muitos achados já vêm acompanhados de uma evidência executável: um crash, uma exceção inesperada ou outro comportamento que podemos reproduzir.

Entre as desvantagens, geralmente requer bastante tempo de CPU para ter bons resultados. 

E o fuzzing tem dificuldade para encontrar problemas de lógica quando não existe um sintoma observável que permita detectar que algo deu errado.

Também é comum que gere scripts enormes, que por vezes precisam ser minimizados antes que o problema fique claro.

### Análise Baseada em IA (Híbrida)

É uma abordagem recente, na qual instruímos um LLM a procurar os bugs no código. Podemos fazer isso de forma direta, solicitando à IA que procure de forma livre.

Mas aqui vamos falar sobre uma forma mais estruturada: vários agentes, e cada um recebe uma especialidade. Aqui, quando eu falo em agente, pense basicamente numa instância do modelo com uma missão, instruções e ferramentas específicas.

Esta técnica corresponde à equipe de pessoas biólogas especialistas trabalhando em conjunto.

Cada agente tem seus alvos e métodos específicos. Alguns leem. Outros procuram padrões. Outros executam.

Ou seja, alguns fazem uma leitura direta do código, interpretando o fluxo de execução e percebendo diretamente inconsistências e problemas. Como fazemos na revisão manual.

Outros procuram padrões de código que ostumam indicar problemas. Como na análise estática. Esses agentes podem inclusive rodar ferramentas de análise estática e fazer o trabalho de identificar problemas reais, descartando falsos positivos.

Outros experimentam inputs problemáticos ou inesperados e observam o comportamento do programa. Como no fuzzing.

E a IA também torna práticas, em grande escala, análises que seriam muito trabalhosas manualmente.

Por exemplo, examinar o histórico de correções de um projeto e procurar lugares semelhantes em que o mesmo bug talvez tenha ficado para trás.

É quando você corrige um bug numa função e não percebe que o mesmo bug está presente em outra função parecida.

Além disso, os agentes podem usar os resultados uns dos outros. Um agente pode identificar os trechos mais complexos do código, e outro usar essa informação para concentrar ali a procura por erros de lógica.

Mas encontrar alguma coisa não é o fim do processo. Outros agentes podem tentar verificar o achado, comparar resultados, eliminar duplicatas e consolidar tudo.

Só então produzimos um relatório que possa ser levado às pessoas mantenedoras, para que possam resolver os bugs, ou pelo menos tomar ciência deles.

E aí começa outro problema: como levar esses resultados às pessoas mantenedoras sem gerar sobrecarga ou ruído. Isso, por si só, daria outra palestra.

## Ferramentas

Agora faremos um breve passeio por ferramentas que nos ajudam a aplicar as técnicas descritas, com certa ênfase nas ferramentas de IA que desenvolvi.

### Para Revisão Manual de Código

Como vimos, este método não utiliza ferramentas específicas. Mas pode se valer de processos como discutir os achados com outras pessoas, criar programas ou scripts para reproduzir o problema, etc. Vamos usar nossos olhos como ferramenta e observar o código abaixo para ver se encontramos um "Uai". É um código mal escrito e confuso, mas isso é só para atrapalhar a análise de vocês.

```python
def max_power(a, b):
    """Encontra o maior número possível na exponenciação de um par."""
    if a > b:
        result = b ** a
        if b < 0 and a % 2 == 0:
            result = abs(result)
        return result
    else:
        result = a ** b
        if a < 0 and b % 2 == 0:
            result = abs(result)
```

O Uai que eu vejo é que falta um `return` ao final do bloco do `else`: o código calcula tudo direitinho, guarda em `result` e... esquece de retornar. Quem chamar a função por esse caminho recebe `None`. Talvez você encontre outro Uai na matemática ou na lógica, mas deu para entender o princípio.

### Para Análise Estática

Acredito que seja a técnica com mais ferramentas disponíveis, e você acha alguma para quase qualquer linguagem de programação.

Em Python, são famosos os linters e os checadores de tipagem. É comum que essas ferramentas venham como parte do IDE, como é o caso do PyCharm e do Zed, seja nativamente, seja na forma de LSPs. Elas encontram erros como variáveis não definidas, problemas de estilo, código com potencial de falhar por fluxos incompletos, tipos incorretos, mas não analisam a lógica mais profunda do código.

Exemplos bem conhecidos são ruff e pylint e os checadores de tipagem, como mypy e pyright. Temos outros, por exemplo o bandit, que é um linter para encontrar vulnerabilidades em código Python.

Vamos dar uma rápida olhada em como algumas dessas ferramentas são utilizadas e os resultados delas:

Primeiro, o ruff. Ele é um linter que analisa o código Python e encontra problemas de estilo, variáveis não definidas, fluxos incompletos, entre outros. Ele é rápido e eficiente, e pode ser configurado para encontrar problemas específicos. Por exemplo, ele não encontra o nosso UAI do código anterior nas configurações padrão. Mas, se ativamos as regras de fluxo de retorno, o grupo RET, ele encontra o UAI na hora, apontando que falta um `return` explícito no fim de uma função que pode retornar valores.

Já o mypy, o checador de tipagem mais tradicional do Python, tem um comportamento curioso: nas configurações padrão, ele nem analisa o corpo de funções sem anotações de tipo, então o nosso `max_power` passa ileso. O modo estrito reclama, mas apenas da falta das anotações. A mágica acontece quando atendemos ao pedido: no momento em que declaramos que `max_power` recebe e retorna `int`, o mypy encontra o UAI imediatamente, mesmo sem modo estrito: `Missing return statement`, falta um `return`. A anotação de tipo é a gente mostrando à ferramenta qual pegada procurar: dizemos o que a função deveria retornar, e ela flagra o caminho que não retorna nada.

### Para Fuzzing

AFL, fuzzers específicos do CPython no OSSFuzz, fusil e lafleur.

Como vimos, elas executam o código e acabam analisando a lógica profunda, desde que tenha efeitos visíveis.

Vamos ver brevemente como uma dessas ferramentas, lafleur, funciona e que tipo de resultados ela traz:

[...]

### Para Análise Baseada em IA (Híbrida)

Temos uma ampla gama de projetos nessa categoria: pr-review-toolkit, xxx, yyy. Mas geralmente são focados ou em análise de PRs ou de segurança do código. Além disso, são multi-linguagem.

No ecossistema Python, as principais ferramentas de análise baseada em IA são criações minhas. São alguns plugins para Claude Code, cada um focando em um aspecto específico:

- code-review-toolkit, que analisa código Python puro.
- cext-review-toolkit, que analisa extensões em C e C++ para Python.
- ft-review-toolkit, que analisa suporte e problemas de extensões em C relacionados ao Free Threading.
- cpython-review-toolkit, que analisa o código do próprio CPython.
- rust-ext-review-toolkit (junto com Charlie Lin), que analisa extensões em Rust para Python.

Essas ferramentas formam uma família que compartilha métodos, código e filosofia, sendo cada uma adaptada de forma específica para o fim a que se destina. Alguns agentes e scripts são compartilhados e adaptados, outros são exclusivos de uma ferramenta.

Vamos ver como é a organização geral desses plugins.

Vamos ver exemplos dos tipos de erro que uma dessas ferramentas encontra:

[...]

## Resultados e Conclusões

Como foi citado lá no início, essas ferramentas de fuzzing e IA que discutimos não são teóricas, com aplicação potencial. Elas foram utilizadas em algumas campanhas voltadas ao ecossistema Python e trouxeram resultados significativos.

### Sobre as Campanhas

As campanhas aconteceram em ondas, e a ordem delas conta a própria história do título da palestra. Tudo começou com o olho humano: meus primeiros bugs reportados são de 2008, no velho bugs.python.org, achados na base do Uai. Entre 2024 e 2025 veio a onda de fuzzing, primeiro ressuscitando e modernizando o fusil, depois criando o lafleur para caçar bugs no JIT experimental. E em março de 2026 começou a onda de IA: a família review-toolkit varrendo o CPython, dezenas de extensões C e C++ e o suporte a free threading.

Nada disso foi um esforço solitário: as issues e as correções envolveram dezenas de pessoas, incluindo core developers do CPython e pessoas mantenedoras dos projetos analisados. Os resultados foram publicados ao longo do caminho em issues, PRs, gists e posts [PREENCHER: posts/links dos resultados], e organizei tudo num catálogo de bugs: cada número que vou mostrar a seguir vem de lá e é auditável.

[...]

### Resultados Alcançados

Começando pela onda de fuzzing.

O fusil, considerando seus diferentes modos e plugins, já é responsável por 146 bugs distintos. O lafleur, focado no JIT experimental do CPython, encontrou outros 28.

Depois veio a onda de IA.

O cext-review-toolkit analisou 50 extensões e produziu centenas de achados. Depois de reprodução, deduplicação e triagem, isso virou 138 bugs reportados.

O cpython-review-toolkit encontrou 55 bugs no próprio CPython.

E a análise de free threading, além dos bugs já reportados, mapeou mais de 4.500 corridas de dados potenciais em 18 extensões — aqui estamos falando de pontos que ainda precisam de investigação, e não de 4.500 bugs confirmados.

Somando todas as ondas — olho humano, fuzzing e IA — o catálogo registra hoje 464 bugs distintos.

Em 2008 foram nove, encontrados basicamente no olho.

Em 2026, foram 250 com fuzzing e IA.

Os números acabam contando a mesma história do título desta palestra.

### Importância das Campanhas

Mas uma campanha dessas não serve apenas para aumentar um contador de bugs.

O primeiro efeito é o mais óbvio: encontramos problemas concretos e, em muitos casos, eles são corrigidos.

O segundo aparece quando começamos a ver o mesmo tipo de problema em lugares diferentes. A repetição pode revelar uma API fácil de usar errado, uma prática perigosa ou uma classe inteira de bugs que merece uma solução mais geral.

E existe um terceiro efeito: a própria campanha pode mudar a maneira como um projeto procura bugs. Pessoas mantenedoras começam a buscar casos semelhantes, usar as mesmas ferramentas e adotar práticas mais defensivas.

Isso só funciona, é claro, quando a campanha é feita com responsabilidade e respeito pelo tempo das pessoas mantenedoras.

E temos um sinal de que isso pode funcionar: parte dos bugs foi reportada diretamente por mim, mas muitos outros foram registrados pelas próprias pessoas dos projetos depois de receberem os relatórios.

Um bom relatório vira insumo útil para o projeto, não ruído.

### Importância das Ferramentas

As ferramentas também diminuem a barreira de entrada.

Elas permitem que alguém que ainda não conhece profundamente uma base de código faça análises úteis, e permitem que quem conhece muito bem aquele projeto enxergue o código por perspectivas diferentes das habituais.

Mas talvez exista um efeito ainda mais interessante.

Essas ferramentas ensinam uma maneira de pensar.

Você começa a olhar para o código e perguntar:

“Como isso pode dar errado?”

E depois faz a mesma pergunta de várias perspectivas diferentes.

Isso é pensar como uma pessoa caçadora de bugs.

### Futuro

E o que vem por aí?

Eu vejo três frentes.

A primeira são os modelos. Modelos mais capazes podem tornar os mesmos agentes mais eficientes e, em alguns casos, fazer aparecer problemas que antes escapavam.

A segunda são as ferramentas: novos tipos de agente, verificação automática mais rigorosa antes que qualquer achado vire relatório e menos trabalho para aplicar tudo isso a um projeto novo.

E a terceira, para mim a mais importante, é ter mais gente caçando.

As ferramentas existem. Funcionam. Estão disponíveis.

O próximo passo é colocar mais gente para usá-las.

## Fechamento

Bom, era isso que eu queria compartilhar com vocês.

Se alguém cochilou, essa é uma boa hora para acordar.

Vocês lembram do levantamento de fauna lá do começo?

Quando desenvolvemos um conjunto de técnicas capaz de encontrar diferentes animais numa mata desconhecida, podemos levar essas mesmas técnicas para outras matas.

É exatamente o que aconteceu aqui.

Essas ferramentas já encontraram bugs no CPython, no Pillow, no Cython, no PyPy e em dezenas de outros projetos.

E agora elas também podem procurar bugs no código de vocês.

### Um Convite

Então fica o convite.

Se você mantém um projeto Python, usa um projeto no qual gostaria de contribuir ou simplesmente ficou curioso, venha conversar comigo.

Se alguma dessas ferramentas fizer sentido para o projeto, eu posso ensinar como usá-la e podemos fazer a análise juntos.

PÁ, CAPIVARA!

### Agradecimento e Contato

Agradeço a presença de todas e todos e a sua atenção. Espero que tenham aproveitado a palestra e tenham saído com mais conhecimento e interesse pela caça aos bugs. Aqui estão meus dados para contato. Se quiser tirar uma dúvida, solicitar uma análise ou só bater papo, fique à vontade para mandar mensagens. Obrigado!
