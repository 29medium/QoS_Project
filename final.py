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
    return r['ping'],r['download'],r['upload']

def download():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download(threads=None)

    r = s.results.dict()
    return r['ping'],r['download'],r['upload']

def upload():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.upload(threads=None)


    r = s.results.dict()
    return r['ping'],r['download'],r['upload']


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
    names='date time ping download upload'.split(),
    header=None,
    sep=r'\s+',
    parse_dates={'timestamp':[0,1]},
    na_values=['TEST','FAILED'],
  )

  print(df[-48:]) # return last 48 rows of data (i.e., 24 hours)

def do_it(opc):
    switch={
        "download":download(),
        "upload":upload(),
        "tudo":download_and_upload(),
        "read":read_data()
    }
    return switch.get(opc,'Invalid input')



if __name__ == "__main__":
    setup_logging()
    opcao = interpretador()
    if opcao == 'exit':
        exit()
    try:
        ping, down, up, timestamp = do_it(opcao)
    except ValueError as err:
        logging.info(err)
    else:
        logging.info("%5.1f %5.1f %5.1f", ping, down, up)

