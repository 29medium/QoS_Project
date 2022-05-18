import speedtest

s = speedtest.Speedtest()
s.get_best_server()
s.download(threads=None)
s.upload(threads=None)
s.results.share()

results = s.results.dict()
print(results)