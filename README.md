# Trabalho Seguranca
Repositório parra o Trabalho Prática da Disciplina de Segurança em Sistemas de Computação

## Grupo 04
* Nome: Mariana Siano Pinto
* Matricula: 202465182A

## Como rodar o código

#### Primeiramente, para rodar os códigos, o Free5GC tem que está rodando ativamente para os mesmos rodarem!!

* Clonar o repositório

* Para descobrir quais são as vulnerabilidades, vai para a pasta OWASP com o comando: <br> 
`cd OWASP`.

* Apóis isso, digite o seguinte comando: <br>
`python3 Axx_ + tab` <br>

* Sendo `xx` o número o OWASP (de 01 até 10) e o `tab` para completar, para não precisar digitar o nome todo do arquivo.

* Após achar as vulnerabilidades do OWASP, volta uma pasta com o comando: <br>
`cd ..`

* E testa a vulnerabilidade do arquivo `EXTRA_Falhas-Segmentacao-Rede` com o comando: <br>
`python3 EXTRA_Falhas-Segmentacao-Rede.py`

* Com isso feito, faça o seguinte comando: <br>
`python3 explorador_free5gc.py`

* E, com isso, vão explorar um pouco as vulnerabilidades encontradas no `A02_Cryptographic-Failures` e no `EXTRA_Falhas-Segmentacao-Rede`, criando, também, um gráfico com as vulnerabiidades.