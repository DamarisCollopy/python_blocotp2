import psutil
import time
from matplotlib import pyplot as plt


def meu_switch():
    validacao = True
    x = 1
    while validacao:
        z = int(input("Menu : "
                      "\n 0 : Uso Memoria"
                      "\n 1 : Uso CPU "
                      "\n 2 : Uso Disco"
                      "\n 3 : Ip Maquina"
                      "\n 4 : Sair \n"))
        if z < x:
            uso_memoria()
        elif z == x:
            uso_cpu()
        elif z == 2:
            uso_disco()
        elif z == 3:
            ip_maquina()
        elif z == 4:
            print("Programa encerrado")
            break
        else:
            print("opcao inválida")


def uso_memoria():
    mem = psutil.virtual_memory()
    total = round(mem.total / 1024 ** 3, 2)
    print(f" Memoria disponivel : {total} GB")
    plt.plot(mem)
    plt.show()


def uso_cpu():
    lista_cpu_percent = []

    for i in range(0, 1200):
        lista_cpu_percent.append(psutil.cpu_percent())
        time.sleep(0.1)

    plt.plot(lista_cpu_percent)
    plt.show()


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


def ip_maquina():
    dic_interfaces = psutil.net_if_addrs()
    print(dic_interfaces)


if __name__ == "__main__":
    print(meu_switch())