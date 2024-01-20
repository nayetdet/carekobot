# CarekoBot
O CarekoBot é um bot Discord desenvolvido em Python, utilizando a biblioteca discord.py, com recursos avançados de Text-to-Speech (TTS) para reproduzir mensagens nos canais de voz em que o usuário está presente.<br />

# Comandos
<br />

> ![commands](https://user-images.githubusercontent.com/41995706/211715227-889813d5-24cf-4ea2-a96a-3d9a1efd2b29.png)
> * O prefixo padrão utilizado para invocar os comandos é "=".<br />
> * Optei por não oferecer suporte aos comandos de barra porque simplesmente não gosto deles.<br />

# Comando: SAY
Reproduz uma mensagem TTS no canal de voz do usuário.<br />

### Formas de Utilizar
```
=say Oi
```
> Modo padrão de utilizar o comando.<br />

<br />

```
= Oi
```
> Alternativa mais conveniente para usar o comando.<br />

### Features Extras
O comando também pode alterar o sotaque e traduzir mensagens conforme as linguagens disponíveis.<br />
```
= [en] Oi
```
> O bot vai falar "Oi", mas com sotaque estadunidense.<br />

<br />

```
= [t/en] Oi
```
> A palavra é traduzida para seu equivalente em inglês e pronunciada com sotaque estadunidense.<br />

# Diferentes formas de invocar comandos
- default: lang, d<br />
- stop: s<br />
- join: j<br />
- clear: c<br />
- leave: l<br />

# Utilidade Extra
O bot oferece um recurso adicional de log de informações do servidor, exibindo dados úteis quando o usuário menciona o bot.
> ![Captura de tela 2023-01-11 024313](https://user-images.githubusercontent.com/41995706/211726783-0baf3369-c946-4776-b18f-8b2457bb243b.png)<br />
> Um adendo importante é que esse comando funciona mesmo em canais que estão lockado, assim, pode servir como referência caso o usuário em questão não se lembre quais canais ele havia lockado anteriormente. <br />

# Linguagens Suportadas
Africanêr, Alemão, Árabe, Bengali, Búlgaro, Canarês, Catalão, Cingalês, Coreano, Dinamarquês, Eslovaco, Espanhol, Estoniano, Filipino, Finlandês, Francês, Grego, Guzerate, Hindi, Holandês, Húngaro, Indonésio, Inglês, Islandês, Italiano, Japonês, Malaiala, Mandarim, Marati, Nepali, Norueguês, Polonês, Português, Quemer, Romeno, Russo, Sérvio, Sueco, Sundanês, Tâmil, Theco, Telugo, Ucraniano, Urdu, Vietnamita.<br />
