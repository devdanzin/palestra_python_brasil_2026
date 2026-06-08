# Caçando bugs em Python: do olho humano à IA

## Introdução

### Olá

Saudações a todas e a todos! Meu nome é Daniel Diniz e esta é a palestra "Caçando bugs em Python: do olho humano à IA".

Primeiro, gostaria de agradecer a vocês por participar da palestra. Segundo, gostaria de me apresentar.

### Quem sou

Minhas qualificações, em ordem de importância:

- Sou pai do Pedro, que tem 12 anos e está aqui conosco
- Sou biólogo e exerço a profissão
- Sou Programador Amador de Python há mais de 20 anos, nunca atuei profissionalmente na área de tecnologia
- Faço parte do Python Triage Team, grupo oficial que faz triagem de bugs no GitHub do CPython, a principal implementação do Python
- Faço parte do Python Fuzzing Team, grupo oficial voltado ao fuzzing do CPython, a gente vai ver o que é fuzzing daqui a pouco
- Sou um caçador de bugs, interessado em ajudar projetos a serem mais robustos encontrando falhas neles

Estou envolvido na análise de projetos escritos em Python há pouco menos de 20 anos e gostaria de trazer para vocês algumas coisas que aprendi, desenvolvi e descobri ao longo desse tempo.

## Um breve paralelo

Como já citei, sou biólogo. Minha área de atuação é fauna: os animaizinhos desse mundão. E também sou programador, e minha área é a caça a bugs, defeitos e problemas de software em geral. Vejo muitas semelhanças entre essas duas atividades. Por isso, convido vocês a passearem por um paralelo entre biologia e programação.

Imagine que você está na natureza, numa mata desconhecida, nunca estudada. Você sabe que existem animais ali, só não sabe quais, nem onde estão. Com bugs é a mesma coisa: é certo que eles existem, mas quais são? Em que partes do software eles estão?

Existem diversas formas de descobrir quais animais estão presentes, mas ocultos, naquele lugar. Você pode fazer uma simples observação: está lá esperando o que vai aparecer e, do nada, PÁ, CAPIVARA. Você pode procurar por indícios e pistas, como pegadas, tocas ou ninhos. Ou você pode, por exemplo, colocar câmeras automáticas com diversos tipos de isca para registrar animais que forem lá comer.

Com os bugs, a simples observação é o que chamamos de revisão manual do código: procuramos os bugs ativamente, mas sem técnicas ou ferramentas específicas para ajudar. Procurar por indícios corresponde à análise estática, uma técnica que tenta encontrar partes do código que estejam seguindo padrões que geralmente resultam em bugs. E tentar atrair animais com iscas diferentes parece com o fuzzing, técnica na qual alimentamos programas com inputs de diversos tipos, tentando que algum deles faça um bug oculto se mostrar.

Agora imagine uma equipe onde cada pessoa bióloga é especialista em uma classe de animal: uma em mamíferos, outra em aves, outra em répteis, e todas varrem o mesmo trecho de mata simultaneamente, cada uma com seu próprio método, procurando os animais que vivem ali. É assim que os agentes de IA trabalham: cada um caça uma classe específica de bug, como vazamento de referência, falha de NULL, problema de GIL, utilizando as técnicas citadas em paralelo no mesmo código.

## Spoilers

Bom, para adiantar o que um esforço de caça aos bugs pode encontrar, eu gostaria de dar spoilers sobre uma campanha recente de caça aos bugs baseada em IA, focando tanto no CPython quanto no ecossistema de extensões Python em C e C++.

Essa campanha começou em março deste ano, e nela eu utilizei ferramentas que serão detalhadas em breve.
Nesse período, foram encontrados mais de 300 bugs no código C do CPython.
Além disso, foram analisadas cerca de 90 extensões Python em C, correspondendo a cerca de 2 milhões de linhas de código. Nessas extensões, foram encontrados por volta de 2000 bugs. Desses bugs, cerca de 300 possuem exemplos de reprodução: um pequeno script que demonstra o crash ou o comportamento inesperado do código.

Antes da virada para ferramentas baseadas em IA, uma campanha de fuzzing tradicional do CPython em 2024-2025 já tinha rendido 52 issues, incluindo release blockers, que são bugs tão severos que uma nova versão do Python só pode ser lançada depois de consertá-los. Um fuzzer mais recente, focado no JIT experimental do Python, encontrou XX crashes.

Espero que esses resultados tenham despertado curiosidade sobre como encontrar esses bugs, porque é isso que veremos agora.

## Técnicas

Falaremos de três técnicas básicas, ou famílias de técnicas, que são as mais importantes que conheço para encontrar bugs em projetos Python, e depois de uma quarta abordagem, híbrida, que combina aspectos das três: a análise baseada em IA.

Primeiro, abordaremos a revisão manual de código, aquela que a gente faz meio que automaticamente lendo o código quando está escrevendo ou fazendo revisão de código. Em seguida, a análise estática, que é uma técnica que analisa o código sem executá-lo, utilizando ferramentas. Depois disso, o fuzzing, que é automatizado e pode encontrar bugs que as outras técnicas não conseguem. Por fim, examinaremos a análise baseada em IA, que é híbrida, porque apresenta características de todas as outras técnicas.

### Revisão Manual de Código

Pois bem. Começando pela revisão manual de código, frequentemente empregada pelas pessoas mantenedoras nos seus projetos, ou por quem tem que resolver problemas encontrados na execução do software.

Essa técnica corresponde à observação simples na busca por animais. Você está lá olhando o código e PÁ, CAPIVARA.

Eu gosto de chamar de Desenvolvimento Guiado por Uai, porque o que acontece é que você olha pro código e pensa "UAI! o código tá errado aqui!". Pode ser guiado por UÉ, por É O QUÊ??, por ÔXI, varia.

Nessa técnica, as regras geralmente ficam armazenadas nas cabeças das pessoas desenvolvedoras e sua aplicação depende de olhar afiado para encontrar problemas. Isso requer experiência e faro. Talvez seja a técnica mais precisa e profunda para encontrar bugs em softwares, mas também é a mais demorada e não é escalável. Ou seja, não é uma boa técnica para cobrir grandes quantidades de código rapidamente.

[...]

### Análise Estática

Tem esse nome porque analisa o código sem executá-lo, utilizando ferramentas que procuram padrões de código que indicam possíveis bugs.

Esta técnica corresponde à procura por indícios da presença de animais. Você está buscando as pegadas dos bugs.

Cada ferramenta tem uma forma de consumir e analisar o código. Pode fazer um parse, usar expressões regulares, etc. e tenta identificar trechos do código que correspondem a regras pré-definidas. Estas regras em geral são configuráveis e muitas vezes podem ser acrescidas de regras personalizadas pela pessoa usuária. Então, em vez de depender da memória e do olhar da pessoa desenvolvedora para encontrar possíveis bugs, a análise estática baseia-se em padrões de código que são identificados automaticamente pelas ferramentas, podendo ser executada em grande escala.

Por isso, ela é menos precisa e profunda, mas mais rápida e escalável do que a revisão manual. Mas ainda depende de olhar afiado para filtrar os falsos positivos que as ferramentas tendem a gerar. Ou seja, é capaz de lidar com grandes quantidades de código rapidamente, mas sem o detalhamento e confiabilidade da revisão manual.

[...]

### Fuzzing

Fuzzing é uma técnica baseada em fornecer inputs problemáticos ou inválidos, frequentemente de forma aleatória e guiada, para testar a robustez do software. Como o software é executado com esses inputs, é uma forma de análise dinâmica.

Esta técnica corresponde às câmeras com iscas diferentes para atrair animais. Você oferece inputs e vê atraem algum bug.

No fuzzing, em vez de regras pré-definidas, os inputs são gerados aleatoriamente e frequentemente de forma guiada por um mecanismo de feedback. A parte de ser aleatório, que significa gerar inputs de forma imprevisível e "criativa", permite que o fuzzer explore uma ampla gama de inputs, enquanto a parte de ser guiada pelo feedback, que significa levar em conta o efeito dos inputs anteriores na hora de construir novos, ajuda a identificar inputs com maior probabilidade de encontrar bugs.

Com o fuzzing, é possível encontrar bugs que outras técnicas não alcançam, em larga escala e, em geral, confirmados, pois a detecção é de estados inválidos do programa que podem ser reproduzidos. Por isso, ele é mais preciso e confiável do que a análise estática, mas menos abrangente e geralmente requer bastante tempo de CPU para ter bons resultados. Também é comum que gere scripts enormes, que por vezes precisam ser minimizados antes que o problema fique claro.

[...]

### Análise Baseada em IA (Híbrida)

É uma técnica recente, na qual instruímos um LLM a procurar os bugs no código. Podemos fazer isso de forma direta, solicitando ao modelo que procure de forma livre. Mas aqui vamos falar sobre uma forma mais estruturada, na qual delegamos a diversos agentes que procurem tipos de bugs específicos. Usada dessa maneira, a IA permite uma abordagem híbrida, com características de revisão manual, análise estática e fuzzing.

Esta técnica corresponde à equipe de pessoas biólogas especialistas trabalhando em conjunto.

Os diferentes agentes de IA são instruídos a partir de prompts específicos, cada um descrevendo o tipo de análise que devem realizar e exemplos de problemas que devem procurar. Cada agente pode ter acesso a recursos especiais, como ferramentas de análise estática e ambientes preparados para a execução de código, para aumentar sua eficácia.

Alguns dos agentes realizam uma leitura direta do código, interpretando o fluxo de execução e percebendo diretamente inconsistências e problemas como fazemos na revisão manual.

Também existem agentes voltados à procura de padrões de código que geralmente são problemáticos, como na análise estática. Esses agentes podem inclusive rodar ferramentas de análise estática e fazer o trabalho de identificar problemas reais, descartando falsos positivos.

Outros agentes podem focar no que acontece quando inputs inválidos são passados ao programa, podendo escrever scripts que chamam o programa com esses inputs e observar o comportamento quando executados, se assemelhando ao fuzzing.

E é possível ter agentes utilizando técnicas que só são possíveis com IA, como a análise do histórico de correções de bugs num projeto, que permite identificar correções imprecisas ou incompletas, nas quais código semelhante ainda apresenta o mesmo bug. É quando você corrige um bug numa função e não percebe que o mesmo bug está presente em outra função parecida.

Além do trabalho individual de cada agente, eles também podem corroborar ou desmentir os resultados uns dos outros, às vezes utilizando estes resultados como base da sua própria análise. Por exemplo, um agente que identifica erros de lógica pode ser guiado por um agente que identifica trechos de código mais complexos, mais propensos a abrigar bugs.

Como cada agente tem uma missão específica, geralmente precisamos de um passo de unificação dos seus relatórios. Esse passo remove duplicatas, analisa e prioriza os problemas encontrados, e gera um relatório que pode ser encaminhado às pessoas mantenedoras do código para que possam resolver, ou pelos menos tomar ciência, os bugs.

A interação com as pessoas mantenedoras é um tópico que merece uma palestra por si só, pois passa por incredulidade, sobrecarga, resistências diversas, respeito ao tempo e energia de pessoas mantenedoras, formas adequadas de comunicação, etc.

[...]

## Ferramentas

Agora faremos um breve passeio por ferramentas que nos ajudam a aplicar as técnicas descritas, com certa ênfase nas ferramentas de IA que desenvolvi.

### Para Revisão Manual de Código

Como vimos, este método não utiliza ferramentas específicas. Mas pode se valer de processos como discutir os achados com outras pessoas, criar programas ou scripts para reproduzir o problema, etc. Vamos usar nossos olhos como ferramenta e observar o código abaixo para ver se encontramos um "Uai". É um código mal escrito e confuso, mas isso é só para atrapalhar a análise de vocês.

```python
def max_pow(a, b):
    """Encontra o maior número possível na exponenciação de um par de números."""
    if a > b:
        result = b ** a
        if b < 0 and a % 2 == 0:
            result = abs(result)
        print(result)
        return result
    result = a ** b
    if a < 0 and b % 2 == 0:
        result = abs(result)
    print(result)
```

O Uai que eu vejo é que falta um `return` ao final do segundo bloco: o código vai printar o resultado, mas vai retornar `None`. Talvez você encontre outro Uai na matemática ou na lógica, mas deu para entender o princípio.

### Para Análise Estática

Acredito que seja a técnica com mais ferramentas disponíveis, você acha alguma para quase qualquer linguagem de programação.

Em Python, são famosos os linters e os checadores de tipagem. É comum que essas ferramentas venham como parte do IDE, como é o caso do PyCharm e do Zed, seja nativamente, seja na forma de LSPs. Elas encontram erros como variáveis não definidas, problemas de estilo, código com potencial de falhar por fluxos incompletos, tipos incorretos, mas não analisam a lógica mais profunda do código.

Exemplos bem conhecidos são ruff e pylint e os checadores de tipagem, como mypy e pyright.

Vamos dar uma rápida olhada em como algumas dessas ferramentas são utilizadas e os resultados delas:

[...]

### Para Fuzzing

AFL, fuzzers específicos do CPython no OSSFuzz, fusil e lafleur.

Como executam o código, acabam analisando a lógica profunda.

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

Essas ferramentas formam um família que compartilha métodos, código e filosofia, sendo cada uma adaptada de forma específica para o fim a que se destina. Alguns agentes e scripts são compartilhados e adaptados, outros são exclusivos de uma ferramenta.

Vamos ver como é a organização geral desses plugins.

Vamos ver exemplos dos tipos de erro que uma dessas ferramentas encontra:

[...]

## Resultados e Conclusões

Como foi citado lá no início, essas minhas ferramentas de fuzzing e IA que discutimos não são teóricas, com aplicação potencial. Elas foram utilizadas em algumas campanhas voltadas ao ecossistema Python e trouxeram resultados significativos.

### Sobre as Campanhas

Descrição das campanhas (período, quem se envolveu, posts dos resultados, etc.).

[...]

### Resultados Alcançados

Descrição detalhada dos resultados das campanhas.

[...]

### Importância das Campanhas

Esse tipo de esforço sistemático é importante em diferentes níveis. No mais básico, reportamos problemas e às vezes soluções para bugs específicos. Também fomentamos que as pessoas mantenedoras procurem mais falhas e problemas, além dos que identificamos, por si mesmas, às vezes até utilizando as mesmas ferramentas. Isso pode mudar um pouco a cultura do projeto. O fato de ser um esforço amplo permite que identifiquemos problemas recorrentes em diferentes contextos, podendo dar origem a soluções nas APIs que frequentemente são utilizadas de maneira incorreta. Por fim, a discussão que esse tipo de campanha gera contribui para que projetos procurem por ajuda para analisar seu código de diversas formas e adotem práticas defensivas preventivas. Tudo isso tem impactos positivos na comunidade Python, pois, desde que feita com responsabilidade e respeito a pessoas mantenedoras, uma campanha dessas mobiliza energia para aumentar a robustez e confiabilidade do software que usamos.

### Importância das Ferramentas

As ferramentas permitem que até mesmo pessoas com pouca familiaridade com o código de um projeto rodem análises capazes de ajudar a tornar o software mais robusto. Também deixam as pessoas especialistas num projeto avaliarem o código de formas totalmente diferentes das que estão acostumadas.

Além de possibilitarem as campanhas e análises individuais de bases de código, as ferramentas ensinam pessoas desenvolvedoras a pensar como caçadoras de bugs: uma abordagem adversarial na qual pensamos "como isso pode dar errado?" por diversas perspectivas.

### Futuro

Perspectivas com modelos mais potentes, aprimoramentos das ferramentas e mais pessoas caçando bugs.

[...]

## Fechamento

Bom, basicamente é isso que eu tinha para compartilhar com vocês. Chegamos à parte final da palestra, espero que estejamos todas e todos bem, quem cochilou pode acordar agora.

Vocês lembram da metáfora do levantamento de fauna no início? Quando você desenvolve um arsenal de técnicas que funciona num local desconhecido, permitindo encontrar diversos tipos de animais, esse arsenal também serve para descobertas semelhantes em outros locais. As ferramentas que vocês viram hoje encontraram bugs no CPython, no Pillow, no PyPy, no Cython, no bottleneck e agora elas estão à disposição para encontrar bugs no código de vocês.

### Um Convite

Se você é pessoa mantenedora de um pacote ou extensão Python, ou se é pessoa usuária de algum projeto específico com o qual gostaria de contribuir, ou apenas ficou com curiosidade sobre o que foi mencionado, fica aqui o convite para que a gente analise esse código em conjunto utilizando as ferramentas que foram apresentadas. Se essas ferramentas fizerem sentido para o código de vocês, estou à disposição para ensinar e fazer junto.

### Agradecimento e Contato

Agradeço a presença de todas e todos e a sua atenção. Espero que tenham aproveitado a palestra e tenham saído com mais conhecimento e interesse pela caça aos bugs. Aqui estão meus dados para contato. Se quiser tirar uma dúvida, solicitar uma análise ou só bater papo, fique a vontade para mandar mensagens. Obrigado! PÁ, CAPIVARA!
