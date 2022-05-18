import speedtest
import logging
import pandas as pd

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
    print(r)
    return r['ping'],r['download'],r['upload'],r['server']['name']+"-"+r['server']['country']

def download():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download(threads=None)

    r = s.results.dict()
    return r['ping'],r['download'],None,r['server']['name']+"-"+r['server']['country']

def upload():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.upload(threads=None)


    r = s.results.dict()
    return r['ping'],None,r['upload'],r['server']['name']+"-"+r['server']['country']


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
def read_data():
    df = pd.io.parsers.read_csv(
        'speedtest.log',
        names='date time ping download upload zone'.split(),
        header=None,
        sep=r'\s+',
        parse_dates={'timestamp':[0,1]},
        na_values=['TEST','FAILED'],
  )

    print(df[-48:]) # return last 48 rows of data (i.e., 24 hours)
    return None,None,None
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
            ping, down, up, zone = do_it(opcao)
        except ValueError as err:
            print(err)
        else:
            if opcao == "download":
                logging.info("%5.1f %5.1f None %s", ping, down,zone)
            elif opcao == "upload":
                logging.info("%5.1f None %5.1f %s", ping, up, zone)
            elif opcao == "tudo":
                logging.info("%5.1f %5.1f %5.1f %s", ping, down, up, zone)
        opcao = interpretador()
