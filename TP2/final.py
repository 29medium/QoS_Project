from numpy import NaN
import speedtest
import logging
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates, rcParams

LOG_FILE = 'speedtest.log'

def setup_logging():
  logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)

def download_and_upload():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download(threads=None)
    s.upload(threads=None)

    r = s.results.dict()

    s2 = speedtest.Speedtest()
    s2.get_best_server()
    s2.download(threads=None)
    s2.upload(threads=None)

    r2 = s2.results.dict()

    return r['ping'],r['download']*0.000001,r['upload']*0.000001,abs(r['ping']-r2['ping']),r['server']['name'].replace(" ","-")+"-"+r['server']['country']

def download():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download(threads=None)

    s2 = speedtest.Speedtest()
    s2.get_best_server()
    s2.download(threads=None)

    r2 = s2.results.dict()

    r = s.results.dict()
    return r['ping'],r['download']*0.000001,None,abs(r['ping']-r2['ping']),r['server']['name'].replace(" ","-")+"-"+r['server']['country']

def upload():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.upload(threads=None)

    s2 = speedtest.Speedtest()
    s2.get_best_server()
    s2.upload(threads=None)

    r2 = s2.results.dict()

    r = s.results.dict()
    return r['ping'],None,r['upload']*0.000001,abs(r['ping']-r2['ping']),r['server']['name'].replace(" ","-")+"-"+r['server']['country']


def interpretador():
    opcoes = ['download','upload','tudo','exit','read']
    
    print("O que deseja testar:")
    for o in opcoes:
        print("\t"+o)
    while (i := input()) not in opcoes:
        print("O que deseja testar:")
        for o in opcoes:
            print("\t"+o)
    
    return i

def make_plot(df):   
    fig, axs = plt.subplots(4)
    fig.suptitle('Download, Upload, Ping and Jitter')


    axs[0].plot(df['download'], 'b-')
    axs[0].get_xaxis().set_visible(False)
    axs[1].plot(df['upload'], 'r-')
    axs[1].get_xaxis().set_visible(False)
    axs[2].plot(df['ping'], 'g-')
    axs[2].get_xaxis().set_visible(False)
    axs[3].plot(df['jitter'], 'y-')
    axs[3].get_xaxis().set_visible(False)

    plt.show()

def read_data():
    df = pd.io.parsers.read_csv(
        'speedtest.log',
        names='date time ping download upload jitter zone'.split(),
        header=None,
        sep=r'\s+',
        parse_dates={'timestamp':[0,1]},
        na_values=['TEST','FAILED'],
  )

    make_plot(df[-48:])

    return None, None, None, None, None

def do_it(opc):
    if opc == "download":
        return download()
    elif opc == "upload":
        return upload()
    elif opc == "tudo":
        return download_and_upload()
    elif opc == "read":
        return read_data()


if __name__ == "__main__":
    setup_logging()
    opcao = interpretador()
    while opcao != "exit":
    
        try:
            ping, down, up, jitter, zone = do_it(opcao)
        except ValueError as err:
            print(err)
        else:
            if opcao == "download":
                print(f"Ping: {ping} Download: {down} Jitter: {jitter} Localização:'{zone}'")
                logging.info("%5.1f %5.1f None %5.1f '%s'", ping, down, jitter, zone)
            elif opcao == "upload":
                print(f"Ping: {ping} Upload: {up} Jitter: {jitter} Localização:'{zone}'")                
                logging.info("%5.1f None %5.1f %5.1f '%s'", ping, up, jitter, zone)
            elif opcao == "tudo":
                print(f"Ping: {ping} Download: {down} Upload: {up} Jitter: {jitter} Localização:'{zone}'")
                logging.info("%5.1f %5.1f %5.1f %5.1f '%s'", ping, down, up, jitter, zone)
        opcao = interpretador()
