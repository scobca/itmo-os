# Логи запуска

## Запуск на чистую

### 1. Base, random graph

```shell
scobca@scobca-MS-7816:~/os-course/lab/intro-exp$ time ./out/graph_traverse 1 graph-rand.bin
Iteration 1/1 (read): traversing graph-rand.bin ... OK (218451 nodes processed)

real    0m0,253s
user    0m0,131s
sys     0m0,121s
```

### 2. Base, sequential graph

```shell
scobca@scobca-MS-7816:~/os-course/lab/intro-exp$ time ./out/graph_traverse 1 graph-seq.bin
Iteration 1/1 (read): traversing graph-seq.bin ... OK (218451 nodes processed)

real    0m0,242s
user    0m0,145s
sys     0m0,097s
```

### 3. --no-cache, random graph

```shell
scobca@scobca-MS-7816:~/os-course/lab/intro-exp$ time ./out/graph_traverse --no-cache 1 graph-rand.bin
Iteration 1/1 (read): traversing graph-rand.bin ... OK (218451 nodes processed)

real    0m12,487s
user    0m0,204s
sys     0m1,192s
```

### 4. --no-cache, sequential graph

```shell
scobca@scobca-MS-7816:~/os-course/lab/intro-exp$ time ./out/graph_traverse --no-cache 1 graph-seq.bin
Iteration 1/1 (read): traversing graph-seq.bin ... OK (218451 nodes processed)

real    0m12,415s
user    0m0,224s
sys     0m1,187s
```

### 5. --write, random graph

```shell
scobca@scobca-MS-7816:~/os-course/lab/intro-exp$ time ./out/graph_traverse --write 1 graph-rand.bin
Iteration 1/1 (write): traversing graph-rand.bin ... OK (218451 nodes processed)

real    0m0,524s
user    0m0,266s
sys     0m0,258s
```

### 6. --write, sequential graph

```shell
scobca@scobca-MS-7816:~/os-course/lab/intro-exp$ time ./out/graph_traverse --write 1 graph-seq.bin
Iteration 1/1 (write): traversing graph-seq.bin ... OK (218451 nodes processed)

real    0m0,516s
user    0m0,272s
sys     0m0,244s
```

### 7. --no-cache + --write, random graph

```shell
scobca@scobca-MS-7816:~/os-course/lab/intro-exp$ time ./out/graph_traverse --write --no-cache 1 graph-rand.bin
Iteration 1/1 (write): traversing graph-rand.bin ... OK (218451 nodes processed)

real    0m43,118s
user    0m0,641s
sys     0m3,705s
```

### 8. --no-cache + --write, sequential graph

```shell
scobca@scobca-MS-7816:~/os-course/lab/intro-exp$ time ./out/graph_traverse --write --no-cache 1 graph-seq.bin
Iteration 1/1 (write): traversing graph-seq.bin ... OK (218451 nodes processed)

real    0m39,312s
user    0m0,635s
sys     0m3,782s
```
