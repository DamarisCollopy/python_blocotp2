import psutil
import platform
import time
from matplotlib import pyplot as plt
import cpuinfo
from cpuinfo import get_cpu_info

# fiz um switch para gerenciar melhor os pedidos
def meu_switch():
    validacao = True
    x = 1
    while validacao:
        z = int(input("Menu : "
                      "\n 0 : Uso Memoria"
                      "\n 1 : Uso CPU "
                      "\n 2 : Uso Disco"
                      "\n 3 : Ip Maquina"
                      "\n 4 : Processador"
                      "\n 5 : Arquitetura de Rede"
                      "\n 6 : Informacao CPUs"
                      "\n 7 : Sair \n"))
        if z < x:
            uso_memoria()
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
            print("Programa encerrado")
            break
        else:
            print("opcao inválida")

#total: total de memória principal em bytes. Caso queira converter para GB, divida o valor por 1024x1024x1024.
def uso_memoria():
    mem = psutil.virtual_memory()
    total = round(mem.total / 1024 ** 3, 2)
    print(f" Memoria disponivel : {total} GB")
    plt.plot(mem)
    plt.show()


    #O programa acima irá produzir informação de uso de processamento a
    # cada segundo, 100 vezes. O comando time.sleep(1) serve para esperar 1 segundo até a próxima leitura.
    # plot mostra essa sequencia no grafico

def uso_cpu():
    lista_cpu_percent = []

    for i in range(0, 100):
        lista_cpu_percent.append(psutil.cpu_percent())
        time.sleep(1)

    plt.plot(lista_cpu_percent)
    plt.show()

#O comando de nome psutil.disk_usage indica o uso de um disco com o caminho de localização passado como parâmetro.
def uso_disco():
    print(time.ctime())
    disco = psutil.disk_usage('/')
    print(" Informacao detalhada do disco:")
    print(f"Total:{round(disco.used / 1024 ** 3, 2)} GB.")
    print(f"Em uso:{round(disco.total / 1024 ** 3, 2)} GB.")
    print(f"Livre:{round(disco.free / 1024 ** 3, 2)} GB.")
    print(f"Percentual:{round(disco.percent, 2)} %.")

    lista_uso_disco = [28.33, 30.45, 55.80, 0.5, 7.4, 10, 600]

    plt.plot(lista_uso_disco)
    plt.title = 'Uso do disco '
    plt.show()

# uname retorna uma tupla de strings (sistema,nome adm,  versão, máquina, processador)
# processor identifica o nome do processador .
#num_threads retorne os threads abertos pelo processo como uma lista de tuplas nomeadas,
# incluindo ID do thread e tempos de CPU do thread (usuário / sistema
# usei a documentacao como guia
# https://www.google.com/search?q=tradutot&oq=tradutot&aqs=chrome..69i57j0l7.3520j0j7&sourceid=chrome&ie=UTF-8
def processador() :
    print(platform.processor())
    print(platform.uname())
    p = psutil.Process()
    print("Numero de Threads" + "" + str(p.num_threads()))
    

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

def quantas_cpus() :

    for t in range(10) :
        print(psutil.cpu_percent(interval=0.1 , percpu = True))

#Exibe um grafico dos nucleos e threads
def exibir_percent_cpu_grafico(segundos) :
    num_cores = psutil.cpu_count()
    lista_uso_cores = []

    for i in range(num_cores) :
        lista_uso_cores.append([])

    for t in range(segundos) :
        percent = psutil.cpu_percent(interval=1, percpu=True)
        for i in range(num_cores):
            lista_uso_cores[i].append(percent[i])
    exibir_grafico(lista_uso_cores)


if __name__ == "__main__":
    print(meu_switch())