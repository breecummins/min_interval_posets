import tests.test_poset_distance as tpd
import time

start = time.time()
tpd.benchmark(20,1,10,0.5)
print(time.time()-start)
