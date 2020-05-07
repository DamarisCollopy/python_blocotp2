import psutil
import platform
import time
from matplotlib import pyplot as plt
import cpuinfo
import os
import stat
import sched
from pprint import pprint as pp
import subprocess


scheduler = sched.scheduler(time.time,time.sleep)
memoria_lista = []
min = []
mem_livre = []
numero_clock = []

#Inclui os TPs 2 e 3
# fiz um switch para gerenciar melhor os pedidos
def meu_switch():
    validacao = True
    x = 1
    while validacao:
        z = int(input("Menu : "
                      "\n 0 : Uso Memoria Virtual"# Questao TP5 escalonamento
                      "\n 1 : Uso CPU "
                      "\n 2 : Uso Disco"
                      "\n 3 : Ip Maquina"
                      "\n 4 : Exibir Processos Ativos"
                      "\n 5 : Arquitetura de Rede"
                      "\n 6 : Informacao CPUs"
                      "\n 7 : Sistema Operacional e Processos"
                      "\n 8 : Diretorios" #questao TP4 e TP5
                      "\n 9 : Numero de Clocks" # questao TP5
                      "\n 10 :Informação sobre sub rede de IP especifico " # questao TP6
                      "\n 11 : Sair \n"))
        if z < x:
            uso_memoria()
            imprimindo_algumas_vezes(uso_memoria)
        elif z == x:
            uso_cpu()
        elif z == 2:
            uso_disco()
        elif z == 3:
            detalhes_rede()
        elif z == 4:
            processador()
        elif z == 5:
            arquitetura_info()
        elif z == 6:
            quantas_cpus()
            exibir_percent_cpu_grafico(10)
        elif z == 7:
            exibir_processamento()
        elif z == 8:
            exibir_diretorio()
            imprimindo_algumas_vezes(exibir_diretorio)
        elif z == 9:
            numero_clocks()
        elif z == 10:
            chamadas_para_ip()
        elif z == 11:
            print("Programa encerrado")
            break
        else:
            print("opcao inválida")


def imprime_evento():

    print('Inicio do evento:', time.ctime(), memoria_lista)
    print('Inicio do evento:', time.ctime(),min)
    # x vai ser os minutos
    x = min
    #y vai ser o resultado da lista
    y = memoria_lista
    # z lista memoria livre
    z = mem_livre
    #listas inseridas na plotagem

    plt.plot(x,y)
    plt.plot(x,z)
    # grafico legenda
    plt.xlabel("Tempo", fontsize=16)
    plt.ylabel("GB", fontsize=16)
    # legenda
    plt.plot(y, label="Memoria Usada")
    plt.plot(z, label="Memoria Livre")
    plt.legend()
    #titulo
    plt.title('Memoria Virtual')
    plt.tight_layout()

    plt.show()

#total: total de memória principal em bytes. Caso queira converter para GB, divida o valor por 1024x1024x1024.
def uso_memoria():
    mem = psutil.virtual_memory()
    total = round(mem.total / 1024 ** 3, 2)
    print(f" Memoria Total : {total} GB")

    for i in range(0,5):
        mem = psutil.virtual_memory()
        # Formatacao para gb e da hora
        total = round(mem.used / 1024 ** 3, 2)
        livre = round(mem.free / 1024 ** 3, 2)
        current_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
        # Salvo na lista para poder usar na plotagem
        memoria_lista.append(total)
        mem_livre.append(livre)
        min.append(current_time)
        # Uso no TP5 para caputurar os dados dos clocks na hora da execucao desse metodo
        clock = time.process_time()
        numero_clock.append(clock)
        #Tempo de espera
        time.sleep(10)
    imprime_evento()

    # O programa acima irá produzir informação de uso da memoria virtual, mostra o uso e a memoria livre alem do total
    # plot um grafico com essas informacoes usando o time sleep ele coleta dados em 10seg e lanca no grafico essas informaoes

def uso_cpu():
    lista_cpu_percent = []
    x = ['0','1','2','3','4','5','6','7','8','9']
    # cpu_percent representa a utilização atual da CPU em todo o sistema como uma porcentagem.
    for i in range(0, 10):
        cpu = psutil.cpu_percent()
        lista_cpu_percent.append(cpu)
        time.sleep(1)

    plt.title('CPU em funcionamento')
    y = lista_cpu_percent
    # grafico legenda
    plt.ylabel("CPU em funcinonamento %", fontsize=16)
    plt.xlabel("Segundos", fontsize=16)
    plt.plot(x,y)
    plt.show()

    # O programa acima irá produzir informação de uso de processamento a
    # cada segundo, 100 vezes. O comando time.sleep(1) serve para esperar 1 segundo até a próxima leitura.
    # plot mostra essa sequencia no grafico

#O comando de nome psutil.disk_usage indica o uso de um disco com o caminho de localização passado como parâmetro.
def uso_disco():
    print("Inicio",time.ctime())
    disco = psutil.disk_usage('/')
    print(" Informacao detalhada do disco:")
    print(f"Em uso:{round(disco.used / 1024 ** 3, 2)} GB.")
    print(f"Total:{round(disco.total / 1024 ** 3, 2)} GB.")
    print(f"Livre:{round(disco.free / 1024 ** 3, 2)} GB.")
    print(f"Percentual:{round(disco.percent, 2)} %.")


    # uname retorna uma tupla de strings (sistema,nome adm,  versão, máquina, processador)
    # processor identifica o nome do processador .
    #num_threads retorne os threads abertos pelo processo como uma lista de tuplas nomeadas,
    # incluindo ID do thread e tempos de CPU do thread (usuário / sistema
    # usei a documentacao como guia
    # https://www.google.com/search?q=tradutot&oq=tradutot&aqs=chrome..69i57j0l7.3520j0j7&sourceid=chrome&ie=UTF-8

def processador() :
    print(platform.processor())
    #Processo avaliado python e numero de threads
    p = psutil.Process()
    pid = os.getpid()
    print("Nome do processo ", psutil.Process(pid).name(), "Numero de Threads:", str(p.num_threads()))
    # processo que esta acontecendo no momento, apresentado PID,nome e status

    # from pprint import pprint as pp
    pp([(procurar.pid, procurar.info) for procurar in psutil.process_iter(['name', 'status']) if
        procurar.info['status'] == psutil.STATUS_RUNNING])


def detalhes_rede() :
    detalhes_rede = psutil.net_if_addrs()
    num_interfaces = len(detalhes_rede)
    for i in range(num_interfaces):
        print(detalhes_rede['Ethernet'][i][1])

#Informação de arquitetura
def arquitetura_info() :

    cpu = cpuinfo.get_cpu_info()
    print(cpu['arch'])
    print(cpu['brand'])
    print(cpu['bits'])
    print(cpu['count'])
    print(cpu['hz_actual'])

def exibir_grafico(valores) :
    for lista in valores :
        plt.plot(lista)
        plt.title('Cpu Processamento %')
        plt.xlabel("Tempo", fontsize=16)
        plt.ylabel("%", fontsize=16)
        plt.show()

def quantas_cpus() :
    porcentagem_cpu = psutil.cpu_percent()*100
    nucleos_processamento = psutil.cpu_count()
    threads_analise = psutil.Process().num_threads()
    threads = []
    lista_perc = []
    nucleos = []
    segundos = []

    for t in range(10) :
        lista_perc.append(porcentagem_cpu)
        nucleos.append(nucleos_processamento)
        threads.append(threads_analise)
        current_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
        segundos.append(current_time)
        time.sleep(10)

    text = ''
    for n, a in zip(lista_perc, nucleos):
        text += '\n Processador {} %  Numero de Nucleos {}'.format(n, a)
    textM = ''
    for n, a in zip(segundos, threads):
        textM += '\n Tempo {}  Threads {}'.format(n, a)
    print(textM,  text)

#Exibe um grafico dos nucleos
def exibir_percent_cpu_grafico(segundos) :
    #Retorne o número de CPUs lógicas no sistema retorne o número de CPUs lógicas no sistema, se não for determinado. núcleos lógicos significa o número de núcleos
    # físicos multiplicados pelo número de threads que podem ser executados em cada núcleo
    num_cores = psutil.cpu_count()
    lista_uso_cores = []

    for i in range(num_cores) :
        lista_uso_cores.append([])

    for t in range(segundos) :
    #cpu_percent representa a utilização atual da CPU em todo o sistema como uma porcentagem.
        percent = psutil.cpu_percent(interval=1, percpu=True)
        for i in range(num_cores):
            lista_uso_cores[i].append(percent[i])
    exibir_grafico(lista_uso_cores)

def exibir_processamento() :
    # devolve o sistema operacional
    plataforma = platform.system()
    print("Sistema Operacional: ", plataforma)
    # Achar PID
    pid = os.getpid()
    print("Nome do processo ", psutil.Process(pid).name(), "PID", pid)

    # Memoria
    # rss ou [0] usado para encontrar a memoria dentro da lista Sistema Operacional Windows
    processo = psutil.Process(os.getpid())
    # processo que esta acontecendo no momento
    # for proc in psutil.process_iter():
    # print(proc.name)

    # conversao em MB
    memoria = processo.memory_info()[0] >> 20
    print("Memoria usada processamento: ", memoria, "MB")

    memoria_porcentagem = processo.memory_percent("rss")
    print("Memoria em porcentagem processo: ", memoria_porcentagem * 100, "%")
    # conversao bytes para MB
    memoria_virtual = psutil.virtual_memory()
    print("Memoria Usada Windows :", memoria_virtual[3] >> 20, "MB")


def exibir_diretorio():
    caminho_path = r"C:\Users\Damaris-PC"
    # esse r junto do caminho é uma formatacao para tornar visivel indeferente como o caminho esta inscrito para a bibloteca, pq na hora da leitura a biblioteca pode nao conseguir visualizar o nome

    print("Nome : %s" % caminho_path)

    # print o diretorio que estou usando no momento, no caso o do programa
    # print(os.getcwd())

    # Mostra o conteudo dentro daquele diretorio
    conteudo = os.listdir(caminho_path)
    print(conteudo)

    nome = os.stat(caminho_path)
    formatar_hora = time.ctime(nome[stat.ST_MTIME])
    formatar_criacao = time.ctime(nome[stat.ST_CTIME])

    # O "ctime", conforme relatado pelo sistema operacional. Em alguns sistemas (como Unix), é a hora da última alteração de metadados e,
    # em outros (como Windows), é a hora de criação (consulte a documentação da plataforma para obter detalhes).
    print("Data da Criação:", formatar_criacao)
    # biblioteca os stat.St_MTIME funcao que mostra a ultima modificacao, usando a biblioteca time eu consigo formatar o numero apresentado em hora,dia,ano,dia da semana e mes por isso chamei de formatar a hora
    print("Data da modificação :", (formatar_hora))
    # ST_SIZE Tamanho em bytes de um arquivo simples
    tamanho = nome.st_size
    print("Tamanho da pasta :", tamanho, "Bytes")

# Questao TP5
def imprimindo_algumas_vezes(variavel):
    print("Inicio Evento:", time.ctime())
    scheduler.enter(5, 1, variavel,())
    scheduler.enter(10, 1, variavel, ())
    scheduler.run()
    print("Fim do Evento:", time.ctime())

def numero_clocks():
    #TimeSleep 10 segundos
    uso_memoria()
    imprimindo_algumas_vezes(uso_memoria)
    text = ''
    for n, a in zip(min, numero_clock):
        text += '\nO Inicio do Evento {} Numero de Clocks {}'.format(n, a)
    print(text)
    print("Inicio do Evento:",time.ctime(), "Clocks em funcionamento no momento:",time.process_time())
    rtc_time = time.ctime()
    print(rtc_time)

# TP6 projeto de bloco
# Ping IP
def ping(hostname):
    # Criar uma ou mais funções que retornem ou apresentem informações sobre as máquinas pertencentes à sub-rede do IP específico
    plataforma = platform.system()
    args = []
    if plataforma == "Windows":
        args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]

    else:
        args = ['ping', '-c', '1', '-W', '1', hostname]

    ret_cod = subprocess.call(args,
                              stdout=open(os.devnull, 'w'),
                              stderr=open(os.devnull, 'w'))
    return ret_cod

def verifica_hosts(base_ip):
    """Verifica todos os host com a base_ip entre 1 e 255 retorna uma lista com todos os host que tiveram resposta 0 (ativo)"""
    print("Mapeando\r")
    host_validos = []
    return_codes = dict()
    for i in range(1, 255):

        return_codes[base_ip + '{0}'.format(i)] = ping(base_ip + '{0}'.format(i))
        if i % 20 == 0:
            print(".", end="")
        if return_codes[base_ip + '{0}'.format(i)] == 0:
            host_validos.append(base_ip + '{0}'.format(i))
    print("\nMapping ready...")

    return host_validos

# TP 6
#11 Questao Criar uma ou mais funções que retornem ou apresentem informações sobre as máquinas pertencentes à sub-rede do IP específico
def chamadas_para_ip():
    # Chamadas
    ip_string = input("Entre com o ip alvo: ")
    ip_lista = ip_string.split('.')
    base_ip = ".".join(ip_lista[0:3]) + '.'
    # 2 Questao Usar a função em seu programa para mostrar o resultado. O resultado pode ser em texto formatado impresso na tela ou gráfico, usando o módulo ‘pygame’.
    print("O teste será feito na sub rede: ", base_ip)
    # 3 Questao Criar uma ou mais funções que retornem ou apresentem informações sobre as portas dos diferentes IPs obtidos nessa sub rede
    # 4 Questao Usar a função em seu programa para mostrar o resultado. O resultado pode ser em texto formatado impresso na tela ou gráfico, usando o ‘pygame’.
    print("Os host válidos são: ", verifica_hosts(base_ip))

def conversao_bytes(n):

    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

if __name__ == "__main__":
    print(meu_switch())