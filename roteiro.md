# Caçando bugs em Python: do olho humano à IA

## Introdução

### Olá

Boa tarde a todas e a todos! Meu nome é Daniel e esta é a palestra "Caçando bugs em Python: do olho humano à IA".

Agradeço a vocês por participarem da palestra. E gostaria de me apresentar.

Primeiro, minha auto-descrição. Sou um homem negro de pele clara, cabelos cacheados na altura dos ombros, de pretos a grisalhos. Estou usando uma calça preta e uma camiseta preta com uma imagem de capivara com um arco-íris. Tenho cara de panaca.

### Quem sou

Essas são minhas qualificações, em ordem de importância:

- Sou pai do **Pedro**, que tem 12 anos e está aqui conosco
- Sou **biólogo** e trabalho na área
- Sou Programador **Amador** de Python há mais de 20 anos, nunca trabalhei na área de tecnologia
- Faço parte de dois times **oficiais** do Python: **Triage Team**, que faz triagem de bugs no GitHub do CPython
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

Agora imagine **uma equipe** de pessoas biólogas. Uma procura mamíferos. Outra, aves. Outra, répteis. Todas investigam a mesma mata, ao mesmo tempo, mas cada uma procurando **coisas diferentes**.

É assim que os agentes de IA trabalham: cada um caça uma classe específica de bug. Um procura problemas de memória. Outro, de concorrência. Outro, de erros de API.

## Spoilers

Só para vocês saberem que isso não é uma discussão hipotética: as campanhas que vou mostrar encontraram dezenas de bugs no próprio CPython e mais de uma centena em extensões do ecossistema Python. No final eu mostro os números. Agora quero mostrar como chegamos até eles.

## Técnicas

Vamos ver quatro abordagens.

Primeiro, o olho humano: revisão manual.

Depois, ferramentas que procuram padrões: análise estática.

Depois, programas que provocam o software: fuzzing.

E finalmente IA, que mistura características das três anteriores.

### Revisão Manual de Código

Começando pela revisão manual de código, frequentemente empregada pelas pessoas mantenedoras nos seus projetos, ou por quem tem que resolver problemas encontrados na execução de um software.

Essa técnica corresponde à observação simples na busca por animais.

Nessa técnica, as regras geralmente ficam armazenadas nas cabeças das pessoas desenvolvedoras e sua aplicação depende de olhar afiado para encontrar problemas.

Isso requer experiência e faro.

Quando feita por alguém que conhece bem o domínio, talvez seja a técnica capaz da análise mais profunda. Mas, até por isso, também é a mais demorada e não é escalável. Ou seja, não é uma boa técnica para cobrir grandes quantidades de código rapidamente.

Eu gosto de chamar de Desenvolvimento Guiado por Uai, porque o que acontece é que você olha pro código e pensa "UAI! o código tá errado aqui!" ou "Ué, isso vai dar crash...".

Em resumo: você está lá olhando o código e PÁ, CAPIVARA.

### Análise Estática

Seguindo para a próxima técnica. É chamada análise estática porque examina o código sem executá-lo. Utiliza ferramentas que procuram padrões de código que indicam possíveis bugs.

Esta técnica corresponde à procura por indícios da presença de animais. Você está buscando as pegadas dos bugs.

Cada ferramenta tem uma forma de consumir e analisar o código. Pode fazer um parse, usar expressões regulares, etc. e tenta identificar trechos do código que correspondem a regras pré-definidas. Estas regras em geral são configuráveis e muitas vezes podem ser acrescidas de regras personalizadas pela pessoa usuária. Então, em vez de depender da memória e do olhar da pessoa desenvolvedora para encontrar possíveis bugs, a análise estática baseia-se em padrões de código que são identificados automaticamente pelas ferramentas, podendo ser executada em grande escala.

```slide
Ilustrar o processo de dar match em regra
```

Ela troca parte da profundidade da revisão manual por escala: consegue varrer muito código rapidamente, mas produz resultados que ainda precisam do olhar humano, especialmente para separar falsos positivos.

### Fuzzing

Fuzzing é uma técnica baseada em gerar e fornecer grandes quantidades de inputs, inclusive inesperados, extremos ou inválidos, e observar como o software reage.

Como o software é executado com esses inputs, é uma forma de análise dinâmica.

Esta técnica corresponde às câmeras com diferentes iscas para atrair animais. Você oferece inputs e vê se atraem algum bug.

No fuzzing, em vez de procurar diretamente por padrões de código problemáticos, o fuzzer gera ou modifica inputs, muitas vezes com uma parte aleatória e com um mecanismo de feedback.

Há duas ideias importantes aí: aleatoriedade e feedback.

```slide
Aleatoriedade e feedback
```

A aleatoriedade ajuda o fuzzer a experimentar coisas que nós talvez não imaginaríamos.

O feedback mostra quais dessas tentativas parecem interessantes, por exemplo, porque alcançaram uma parte nova do código, e ajuda a escolher as próximas tentativas.

Com o fuzzing, é possível encontrar em larga escala bugs que outras técnicas não alcançam. 

Uma vantagem é que muitos achados já vêm acompanhados de uma evidência executável: um crash, uma exceção inesperada ou outro comportamento que podemos reproduzir.

Entre as desvantagens, geralmente requer bastante tempo de CPU para ter bons resultados. 

E o fuzzing tem dificuldade para encontrar problemas de lógica quando não existe um sintoma observável que permita detectar que algo deu errado.

Às vezes o fuzzer produz programas enormes. Eu já vi um com 25 mil linhas.

Depois de reduzir o programa, sobraram nove linhas. E eram suficientes para reproduzir o bug.

### Análise Baseada em IA (Híbrida)

A análise baseada em IA é uma abordagem recente, na qual instruímos um LLM a procurar os bugs no código. Podemos fazer isso de forma direta, solicitando a uma IA que procure de forma livre.

Mas vamos falar sobre uma forma mais estruturada: vários agentes, e cada um recebe uma especialidade. Aqui, quando eu falo em agente, pense basicamente numa instância do modelo com uma missão, instruções e ferramentas específicas.

Esta técnica corresponde à equipe de pessoas biólogas especialistas trabalhando em conjunto.

Cada agente tem seus alvos e métodos específicos. Alguns leem. Outros procuram padrões. Outros executam.

Ou seja, alguns fazem uma leitura direta do código, interpretando o fluxo de execução e percebendo diretamente inconsistências e problemas. Como fazemos na revisão manual.

Outros procuram padrões de código que costumam indicar problemas. Como na análise estática. Esses agentes podem inclusive rodar ferramentas de análise estática e fazer o trabalho de identificar problemas reais, descartando falsos positivos.

Outros experimentam inputs problemáticos ou inesperados e observam o comportamento do programa. Como no fuzzing.

E a IA também torna práticas, em grande escala, análises que seriam muito trabalhosas manualmente.

Por exemplo, examinar o histórico de correções de um projeto e procurar lugares semelhantes em que o mesmo bug talvez tenha ficado para trás.

É quando você corrige um bug numa função e não percebe que o mesmo bug está presente em outra função parecida.

```slide
Mesmo bug não foi corrigido em código semelhante.
```

Como citei, os agentes são especializados.

Além disso, os agentes podem usar os resultados uns dos outros. Um agente pode identificar os trechos mais complexos do código, e outro usar essa informação para concentrar ali a procura por erros de lógica.

Mas encontrar alguma coisa não é o fim do processo. Outros agentes podem tentar verificar o achado, comparar resultados, eliminar duplicatas e consolidar tudo.

Só então produzimos um relatório que possa ser levado às pessoas mantenedoras, para que possam resolver os bugs, ou pelo menos tomar ciência deles.

E aí começa outro problema: como levar esses resultados às pessoas mantenedoras sem gerar sobrecarga ou ruído. Isso, por si só, daria outra palestra.

## Ferramentas

Agora faremos um breve passeio por ferramentas que nos ajudam a aplicar as técnicas descritas, com certa ênfase nas ferramentas que desenvolvi.

### Para Revisão Manual de Código

Como vimos, este método não utiliza ferramentas específicas. Mas pode se valer de processos como discutir os achados com outras pessoas, criar programas ou scripts para reproduzir o problema, etc.

Vamos usar nossos olhos como ferramenta e observar o código abaixo para ver se encontramos um "Uai". É um código mal escrito e confuso, mas isso é só para atrapalhar a análise de vocês.

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

Acharam um Uai? Pode levantar a mão ou arriscar uma resposta.

O Uai que eu vejo é que falta um `return` ao final do bloco do `else`: o código calcula tudo direitinho, guarda em `result` e... esquece de retornar. Quem chamar a função por esse caminho recebe `None`. Talvez você encontre outro Uai na matemática ou na lógica, mas deu para entender o princípio.

### Para Análise Estática

```slide
Introduzindo Análise Estática, já que o slide de ferramentas foi deslocado.
```

Acredito que seja a técnica com mais ferramentas disponíveis, e você acha alguma para quase qualquer linguagem de programação.

Em Python, são famosos os linters e os checadores de tipagem. É comum que essas ferramentas venham como parte do IDE, como é o caso do PyCharm e do Zed, seja nativamente, seja na forma de LSPs.

Essas ferramentas mais comuns encontram variáveis não definidas, problemas de estilo, tipos incorretos e fluxos incompletos, mas cada ferramenta trabalha com uma abstração e uma profundidade diferentes.

Exemplos bem conhecidos são ruff e pylint e os checadores de tipagem, como mypy e pyright. Temos outros, por exemplo o bandit, que é um linter para encontrar vulnerabilidades em código Python.

Vamos dar uma rápida olhada em como algumas dessas ferramentas são utilizadas e os resultados delas:

Primeiro, o ruff. Ele é um linter que analisa o código Python e encontra problemas de estilo, variáveis não definidas, fluxos incompletos, entre outros.

Ele é rápido e eficiente, e pode ser configurado para encontrar problemas específicos. Por exemplo, ele não encontra o nosso UAI do código anterior nas configurações padrão.

Mas, se ativamos as regras de fluxo de retorno, o grupo RET, ele encontra o UAI na hora, apontando que falta um `return` explícito no fim de uma função que pode retornar valores.

Já o mypy, o checador de tipagem mais tradicional do Python, tem um comportamento curioso: nas configurações padrão, ele nem analisa o corpo de funções sem anotações de tipo, então o nosso `max_power` passa ileso.

O modo estrito reclama, mas apenas da falta das anotações.

A mágica acontece quando atendemos ao pedido: no momento em que declaramos que `max_power` recebe e retorna `int`, o mypy encontra o UAI imediatamente, mesmo sem modo estrito: `Missing return statement`, falta um `return`.

A anotação de tipo é a gente mostrando à ferramenta qual pegada procurar: dizemos o que a função deveria retornar, e ela encontra o caminho que não retorna nada.

Ruff e mypy são só duas espécies dessa família. Algumas ferramentas vão bem mais fundo.

Semgrep procura padrões estruturais; Pysa e CodeQL conseguem acompanhar fluxos de dados entre funções; CrossHair procura entradas que violem contratos. Então análise estática não é uma técnica com uma profundidade só: ferramentas diferentes procuram pegadas diferentes.

### Para Fuzzing

No mundo Python temos ferramentas com papéis diferentes. Atheris faz fuzzing guiado por cobertura. Hypothesis trabalha com propriedades e geração de casos; HypoFuzz acrescenta fuzzing contínuo guiado por cobertura. OSS-Fuzz fornece infraestrutura para campanhas contínuas.

E fusil e lafleur são fuzzers mais especializados, focados no Python, que eu desenvolvo e usei nas campanhas que vou mostrar.

Como vimos, elas executam o código e acabam analisando a lógica profunda, desde que tenha efeitos visíveis.

Então vamos sair da teoria. Este foi um programa produzido a partir de uma campanha do fusil.

```python
class Silly:
    def __iter__(self):
        raise RuntimeError("ninguém espera a Inquisição Espanhola")

def generator():
    yield from Silly()

next(generator())  # deveria propagar RuntimeError; ocorria crash
```

Esse código é estranho? É. Mas tem alguma coisa inválida aqui? Não. O __iter__ é perfeitamente autorizado a levantar uma exceção. O que deveria acontecer? RuntimeError. O que aconteceu? Crash.

PÁ, CAPIVARA.

```slide
capivara
```

O problema estava no tratamento de erros dentro do interpretador. Quando o __iter__ falhava, uma operação interna tentava utilizar o resultado da chamada antes de verificar que ela tinha falhado. O resultado foi um acesso inválido à memória.

A correção foi verificar a falha antes de continuar. E o caso virou um teste de regressão.

### Para Análise Baseada em IA (Híbrida)

Hoje existem muitas ferramentas de IA que suportam Python. Algumas revisam mudanças em PRs. Outras colocam IA sobre resultados de análise estática. E outras trabalham em nível de repositório inteiro.

A família que desenvolvi está principalmente nesse terceiro grupo, com uma especialização adicional: Python, o próprio CPython e a fronteira com código nativo.

```slide
- code-review-toolkit: código Python puro.
- cext-review-toolkit: extensões em C e C++.
- ft-review-toolkit: Free Threading.
- cpython-review-toolkit: código do próprio CPython.
- pypy-review-toolkit: PyPy, criado por Bhuvansh Kataria.
- rust-ext-review-toolkit: extensões em Rust, criado por Charlie Lin.
```

E essa família já começou a crescer com a colaboração de outras pessoas. Bhuvansh Kataria desenvolveu uma ferramenta para analisar o PyPy, e Charlie Lin, outra voltada a extensões Python em Rust.

Vamos ver um exemplo do tipo de erro que uma dessas ferramentas encontra:

O alvo da análise era o código por trás do `groupby`, uma ferramenta do módulo `itertools` do Python. Uma correção anterior protegeu referências em `groupby_next` antes de chamar código Python reentrante, por exemplo um dunder eq que avança o iterador.

O `cpython-review-toolkit` examinou o histórico e encontrou a mesma operação desprotegida na função irmã `_grouper_next`. Um `__eq__` malicioso podia reentrar no iterador, substituir e liberar uma chave ainda em uso, produzindo use-after-free e causando crash.

O código no slide, que é bastante avançado, fazia o CPython ter uma falha de segmentação.

```python
import itertools

class Key:
    __hash__ = None
    counter = 0

    def __eq__(self, other):
        if not self.counter:
            self.counter += 1
            try: next(grouper_iter)
            except StopIteration: pass
            return NotImplemented
        return True

g = itertools.groupby(range(4), lambda x: Key())
key, grouper_iter = next(g)
items = list(grouper_iter)
```

Não precisa entender esse código inteiro. Olhem só para isto: durante o __eq__, ele avança o próprio iterador. Usando essa classe como no código à direita, temos um crash.

Você corrige um bug numa função e esquece outra função parecida. Lembram quando eu falei nisso? Aconteceu de verdade.

Quando reportei o bug, inicialmente acharam que era uma duplicata. Foi preciso revalidar o reproducer para demonstrar que se tratava de outro problema. Depois ele foi corrigido e ganhou um teste de regressão.

## Resultados e Conclusões

Como foi citado lá no início, essas ferramentas de fuzzing e IA que discutimos não são teóricas, com aplicação potencial. Elas foram utilizadas em algumas campanhas voltadas ao ecossistema Python e trouxeram resultados significativos.

Mas encontrar um código suspeito é só o começo. Para isso virar uma contribuição, há todo um outro caminho.

Além de encontrar um possível bug, o que chamamos de achado, temos que produzir um script que reproduza esse bug, o que chamamos de reproducer.

Quando temos o reproducer, precisamos checar se aquele já é um problema conhecido: repetir um report anterior desperdiça tempo e energia da pessoa mantenedora.

Com a confirmação de que é um bug desconhecido, precisamos entrar em contato com as pessoas mantenedoras e validar o bug, até mesmo para saber se elas têm interesse em corrigi-lo. 

```slide
Respeito às pessoas mantenedoras!

encontrar → reproduzir → deduplicar → comunicar e validar → corrigir
```

Esse contato com pessoas mantenedoras é algo importante e delicado. Temos que pensar no custo-benefício do nosso trabalho. Um relatório com 50 achados pode significar 50 horas de trabalho para alguém que não pediu por ele e até mesmo que não considera esses bugs relevantes. E se boa parte desses achados forem falsos positivos, a situação fica ainda pior.

```slide
Manadas de capivaras, com a legenda "Capivárias".
```

A última coisa que você quer é descarregar uma avalanche de achados sobre uma pessoa mantenedora que provavelmente já está sobrecarregada com tarefas relativas ao seu projeto.

Como falei, daria para fazer uma palestra inteira só sobre essa parte humana do processo.

### Sobre as Campanhas

As campanhas aconteceram em ondas, e a ordem delas conta a própria história do título da palestra.

Tudo começou com o olho humano: meus primeiros bugs reportados são de 2008, no velho bugs.python.org, achados na base do Uai.

Entre 2024 e 2025 veio a onda de fuzzing, primeiro ressuscitando e modernizando o fusil, depois criando o lafleur para caçar bugs no JIT experimental.

E em 2026 começou a onda de IA: a família review-toolkit varrendo o CPython, dezenas de extensões C e C++ e o suporte a free threading.

Nada disso foi um esforço solitário: as issues e as correções envolveram dezenas de pessoas, incluindo core developers do CPython e pessoas mantenedoras dos projetos analisados. Os resultados foram publicados ao longo do caminho em issues, PRs, gists e posts. 

Deu até em dissertação de mestrado de um colega e uma matéria jornalística.

```slides
Imagem Tese Hameed
Imagem matéria LWN.net
```

Uma pergunta interessante que recebi na prévia dessa palestra foi: e os recursos para fazer tudo isso? CPU, tokens, infraestrutura? Você paga do próprio bolso?

Em parte, sim.

Uso máquinas virtuais gratuitas na nuvem, mas também investi em máquinas próprias para executar fuzzers.

Para a IA, uso uma assinatura básica do Claude. Também recebi um patrocínio da Anthropic, com acesso por 12 meses a um plano mais avançado, que viabilizou boa parte das campanhas recentes. Fica aqui meu agradecimento.

Mas talvez o maior investimento seja o tempo. Analisar os achados, reproduzir os bugs, investigar, melhorar as ferramentas e conversar com as pessoas mantenedoras exige bastante trabalho humano.

Ou seja, não ganho dinheiro com isso: eu gasto.

```slide
| Recurso | Como obtenho |
|---|---|
| CPU | Máquinas próprias e nuvem |
| IA | Assinatura e apoio recebido |
| Tempo | Trabalho voluntário |
```

### Resultados Alcançados

Em 2008 foram nove bugs, encontrados basicamente no olho.

Em 2026, já foram 250 bugs com fuzzing e IA.

Os números acabam contando a mesma história do título desta palestra.

Quando falamos de achados e bugs, há um funil de evidência, por exemplo:

```slide
Achado não é bug
~690 achados
↓ 
revisão + reprodução
↓
215+ reproduzidos
↓ 
deduplicação + comunicação
↓
138 bugs distintos
```

Então, quando eu digo 690 achados, eu não estou dizendo 690 bugs.

Depois de revisão, reprodução, deduplicação e comunicação, chegaram a 138 bugs distintos.

É justamente por isso que eu faço distinção entre achado, reproducer e bug. Esses números não são intercambiáveis e se afunilam a partir da verificação e colaboração.

Somando todas as ondas — olho humano, fuzzing e IA — o catálogo registra hoje 464 bugs distintos.

### Importância das Campanhas

Mas uma campanha dessas não serve apenas para aumentar um contador de bugs.

O primeiro efeito é o mais óbvio: encontramos problemas concretos e, em muitos casos, eles são corrigidos.

O segundo aparece quando começamos a ver o mesmo tipo de problema em lugares diferentes. A repetição pode revelar uma API fácil de usar errado, uma prática perigosa ou uma classe inteira de bugs que merece uma solução mais geral. Só com campanhas em larga escala conseguimos construir essa visão macro do ecossistem.

E existe um terceiro efeito: a própria campanha pode mudar a maneira como um projeto procura bugs. Pessoas mantenedoras começam a buscar casos semelhantes, usar as mesmas ferramentas e adotar práticas mais defensivas. Isso já encontrou diversos bugs que eu não tinha achado.

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

E a terceira frente, para mim a mais importante, é ter mais gente caçando.

Mas não cada pessoa por conta própria.

Eu gostaria de ver pessoas colaborando, coordenando campanhas, melhorando ferramentas juntas e trabalhando de forma organizada com quem mantém os projetos.

Mais gente caçando, mas também mais gente trabalhando em equipe.

É algo que eu gostaria muito de ajudar a construir.

```slide
Imagem para consolidar a ideia de cooperação entre caçadores de bugs?
```

As ferramentas existem. Funcionam. Estão disponíveis.

O próximo passo é colocar mais gente para usá-las, de forma responsável.

## Fechamento

```slide
overview para callback da mata
```

Vocês lembram do levantamento de fauna lá do começo?

Quando desenvolvemos um conjunto de técnicas capaz de encontrar diferentes animais numa mata desconhecida, podemos levar essas mesmas técnicas para outras matas.

É exatamente o que aconteceu aqui.

Essas ferramentas já encontraram bugs no CPython, no Pillow, no Cython, no PyPy e em dezenas de outros projetos.

E agora elas também podem procurar bugs no código de vocês.

### Contato

Muito obrigado pela atenção. Aqui estão meus contatos, caso queiram conversar depois.

Mas falta uma coisa. A mais importante.

Vocês não precisam apenas assistir a outras pessoas encontrando bugs...

### Um Convite

Então fica o convite.

Se você mantém um projeto Python, usa um projeto no qual gostaria de contribuir ou simplesmente ficou curioso, venha conversar comigo.

Se alguma dessas ferramentas fizer sentido para o projeto, eu posso ensinar como usá-la e podemos fazer a análise juntos.

PÁ, CAPIVARA!
