# Создание графов

## Граф 1.1, seed - 808, 10Mb

```shell
python3 util/graphgen.py -s 10M --seed 808 --topology chain -b 0.5 --min-step-pages 2 -o graph-rand.bin
```

```text
Файл записан: graph-rand.bin
  размер файла:        10485760 байт (запрошено: 10485760)
  число вершин:        436905
  размер записи:       24 байт
  fan_out:             1
  page_size:           4096
  min_step_nodes:      342 (~8208 байт)
  root_index:          248087  (offset=5954128)
  рёбер всего:         436904
  доля вперёд/назад:   0.499 / 0.501 (запрошено backprob=0.5)
  доля 'коротких' переходов (< min_step_nodes): 0.006

/* ------------------------------------------------------------------------
 * Автоматически сгенерировано graphgen.py для текущих параметров:
 *   size=10M  fanout=1  backprob=0.5
 *   page_size=4096  min_step_pages=2.0
 *   seed=808
 *
 *   node_count      = 436905
 *   record_size     = 24 байт
 *   min_step_nodes  = 342 (~8208 байт)
 *
 *   ВНИМАНИЕ: page_size/backprob/seed/min_step_nodes НЕ хранятся в самом
 *   файле (сознательно, чтобы читающая программа не могла подстроиться
 *   под гиперпараметры генерации) — они есть только здесь, в этом
 *   сгенерированном для СБОРКИ снипете, и в консольном выводе генератора.
 * ------------------------------------------------------------------------ */
#include <stdint.h>
#include <stddef.h>

#define GCACHEG_MAGIC        "GCACHEG1"   /* 8 байт, без завершающего нуля  */
#define GCACHEG_VERSION      1u
#define GCACHEG_FAN_OUT      1
#define GCACHEG_NODE_COUNT   436905ULL
#define GCACHEG_RECORD_SIZE  24u
#define GCACHEG_SENTINEL     0xFFFFFFFFFFFFFFFFULL  /* пустой слот children[] */

#pragma pack(push, 1)

/* Заголовок файла, ровно 40 байт, little-endian, без выравнивания.
 * Гиперпараметры генерации (page_size, backprob, seed, min_step_nodes)
 * в файл намеренно не пишутся. */
typedef struct {
    char     magic[8];             /* "GCACHEG1"                      */
    uint32_t version;
    uint64_t node_count;
    uint32_t record_size;          /* == sizeof(gcacheg_node_t)       */
    uint32_t fan_out;
    uint64_t root_index;           /* индекс стартовой вершины обхода */
    uint32_t flags;                /* bit0: 1 = граф ацикличен (DAG)  */
} gcacheg_header_t;

/* Запись одной вершины, 24 байт. */
typedef struct {
    int64_t  value;                    /* payload, можно менять при записи */
    uint32_t degree;                   /* фактическое число детей <= fan_out */
    uint32_t reserved;
    uint64_t children[GCACHEG_FAN_OUT]; /* индексы; неисп. слоты = SENTINEL  */
} gcacheg_node_t;

#pragma pack(pop)

_Static_assert(sizeof(gcacheg_header_t) == 40, "header size mismatch");
_Static_assert(sizeof(gcacheg_node_t) == GCACHEG_RECORD_SIZE, "record size mismatch");

/* offset(i) = header + i * record_size, O(1) доступ по индексу */
static inline uint64_t gcacheg_node_offset(uint64_t index) {
    return (uint64_t)sizeof(gcacheg_header_t) + index * (uint64_t)sizeof(gcacheg_node_t);
}
```

## Граф 1.2, seed - 808, 5Mb

```shell
python3 ../util/graphgen.py -s 5M --seed 427 --topology chain -b 0.5 --min-step-pages 2 -o graph-rand.bin
```

```text
Файл записан: graph-rand.bin
  размер файла:        5242864 байт (запрошено: 5242880)
  число вершин:        218451
  размер записи:       24 байт
  fan_out:             1
  page_size:           4096
  min_step_nodes:      342 (~8208 байт)
  root_index:          108587  (offset=2606128)
  рёбер всего:         218450
  доля вперёд/назад:   0.499 / 0.501 (запрошено backprob=0.5)
  доля 'коротких' переходов (< min_step_nodes): 0.010

/* ------------------------------------------------------------------------
 * Автоматически сгенерировано graphgen.py для текущих параметров:
 *   size=5M  fanout=1  backprob=0.5
 *   page_size=4096  min_step_pages=2.0
 *   seed=427
 *
 *   node_count      = 218451
 *   record_size     = 24 байт
 *   min_step_nodes  = 342 (~8208 байт)
 *
 *   ВНИМАНИЕ: page_size/backprob/seed/min_step_nodes НЕ хранятся в самом
 *   файле (сознательно, чтобы читающая программа не могла подстроиться
 *   под гиперпараметры генерации) — они есть только здесь, в этом
 *   сгенерированном для СБОРКИ снипете, и в консольном выводе генератора.
 * ------------------------------------------------------------------------ */
#include <stdint.h>
#include <stddef.h>

#define GCACHEG_MAGIC        "GCACHEG1"   /* 8 байт, без завершающего нуля  */
#define GCACHEG_VERSION      1u
#define GCACHEG_FAN_OUT      1
#define GCACHEG_NODE_COUNT   218451ULL
#define GCACHEG_RECORD_SIZE  24u
#define GCACHEG_SENTINEL     0xFFFFFFFFFFFFFFFFULL  /* пустой слот children[] */

#pragma pack(push, 1)

/* Заголовок файла, ровно 40 байт, little-endian, без выравнивания.
 * Гиперпараметры генерации (page_size, backprob, seed, min_step_nodes)
 * в файл намеренно не пишутся. */
typedef struct {
    char     magic[8];             /* "GCACHEG1"                      */
    uint32_t version;
    uint64_t node_count;
    uint32_t record_size;          /* == sizeof(gcacheg_node_t)       */
    uint32_t fan_out;
    uint64_t root_index;           /* индекс стартовой вершины обхода */
    uint32_t flags;                /* bit0: 1 = граф ацикличен (DAG)  */
} gcacheg_header_t;

/* Запись одной вершины, 24 байт. */
typedef struct {
    int64_t  value;                    /* payload, можно менять при записи */
    uint32_t degree;                   /* фактическое число детей <= fan_out */
    uint32_t reserved;
    uint64_t children[GCACHEG_FAN_OUT]; /* индексы; неисп. слоты = SENTINEL  */
} gcacheg_node_t;

#pragma pack(pop)

_Static_assert(sizeof(gcacheg_header_t) == 40, "header size mismatch");
_Static_assert(sizeof(gcacheg_node_t) == GCACHEG_RECORD_SIZE, "record size mismatch");

/* offset(i) = header + i * record_size, O(1) доступ по индексу */
static inline uint64_t gcacheg_node_offset(uint64_t index) {
    return (uint64_t)sizeof(gcacheg_header_t) + index * (uint64_t)sizeof(gcacheg_node_t);
}
```

## Граф 2.1, seed - 808, 10Mb

```shell
python3 util/graphgen.py -s 10M --seed 808 --topology sequential -o graph-seq.bin
```

```text
Файл записан: graph-seq.bin
  размер файла:        10485760 байт (запрошено: 10485760)
  число вершин:        436905
  размер записи:       24 байт
  fan_out:             1
  page_size:           4096
  min_step_nodes:      342 (~8208 байт)
  root_index:          0  (offset=40)
  рёбер всего:         436904
  доля вперёд/назад:   1.000 / 0.000 (запрошено backprob=0.5)
  доля 'коротких' переходов (< min_step_nodes): 0.000

/* ------------------------------------------------------------------------
 * Автоматически сгенерировано graphgen.py для текущих параметров:
 *   size=10M  fanout=1  backprob=0.5
 *   page_size=4096  min_step_pages=2.0
 *   seed=808
 *
 *   node_count      = 436905
 *   record_size     = 24 байт
 *   min_step_nodes  = 342 (~8208 байт)
 *
 *   ВНИМАНИЕ: page_size/backprob/seed/min_step_nodes НЕ хранятся в самом
 *   файле (сознательно, чтобы читающая программа не могла подстроиться
 *   под гиперпараметры генерации) — они есть только здесь, в этом
 *   сгенерированном для СБОРКИ снипете, и в консольном выводе генератора.
 * ------------------------------------------------------------------------ */
#include <stdint.h>
#include <stddef.h>

#define GCACHEG_MAGIC        "GCACHEG1"   /* 8 байт, без завершающего нуля  */
#define GCACHEG_VERSION      1u
#define GCACHEG_FAN_OUT      1
#define GCACHEG_NODE_COUNT   436905ULL
#define GCACHEG_RECORD_SIZE  24u
#define GCACHEG_SENTINEL     0xFFFFFFFFFFFFFFFFULL  /* пустой слот children[] */

#pragma pack(push, 1)

/* Заголовок файла, ровно 40 байт, little-endian, без выравнивания.
 * Гиперпараметры генерации (page_size, backprob, seed, min_step_nodes)
 * в файл намеренно не пишутся. */
typedef struct {
    char     magic[8];             /* "GCACHEG1"                      */
    uint32_t version;
    uint64_t node_count;
    uint32_t record_size;          /* == sizeof(gcacheg_node_t)       */
    uint32_t fan_out;
    uint64_t root_index;           /* индекс стартовой вершины обхода */
    uint32_t flags;                /* bit0: 1 = граф ацикличен (DAG)  */
} gcacheg_header_t;

/* Запись одной вершины, 24 байт. */
typedef struct {
    int64_t  value;                    /* payload, можно менять при записи */
    uint32_t degree;                   /* фактическое число детей <= fan_out */
    uint32_t reserved;
    uint64_t children[GCACHEG_FAN_OUT]; /* индексы; неисп. слоты = SENTINEL  */
} gcacheg_node_t;

#pragma pack(pop)

_Static_assert(sizeof(gcacheg_header_t) == 40, "header size mismatch");
_Static_assert(sizeof(gcacheg_node_t) == GCACHEG_RECORD_SIZE, "record size mismatch");

/* offset(i) = header + i * record_size, O(1) доступ по индексу */
static inline uint64_t gcacheg_node_offset(uint64_t index) {
    return (uint64_t)sizeof(gcacheg_header_t) + index * (uint64_t)sizeof(gcacheg_node_t);
}
```

## Граф 2.2, seed - 808, 5Mb

```shell
python3 ../util/graphgen.py -s 5M --seed 427 --topology sequential -o graph-seq.bin
```

```text
Файл записан: graph-seq.bin
  размер файла:        5242864 байт (запрошено: 5242880)
  число вершин:        218451
  размер записи:       24 байт
  fan_out:             1
  page_size:           4096
  min_step_nodes:      342 (~8208 байт)
  root_index:          0  (offset=40)
  рёбер всего:         218450
  доля вперёд/назад:   1.000 / 0.000 (запрошено backprob=0.5)
  доля 'коротких' переходов (< min_step_nodes): 0.000

/* ------------------------------------------------------------------------
 * Автоматически сгенерировано graphgen.py для текущих параметров:
 *   size=5M  fanout=1  backprob=0.5
 *   page_size=4096  min_step_pages=2.0
 *   seed=427
 *
 *   node_count      = 218451
 *   record_size     = 24 байт
 *   min_step_nodes  = 342 (~8208 байт)
 *
 *   ВНИМАНИЕ: page_size/backprob/seed/min_step_nodes НЕ хранятся в самом
 *   файле (сознательно, чтобы читающая программа не могла подстроиться
 *   под гиперпараметры генерации) — они есть только здесь, в этом
 *   сгенерированном для СБОРКИ снипете, и в консольном выводе генератора.
 * ------------------------------------------------------------------------ */
#include <stdint.h>
#include <stddef.h>

#define GCACHEG_MAGIC        "GCACHEG1"   /* 8 байт, без завершающего нуля  */
#define GCACHEG_VERSION      1u
#define GCACHEG_FAN_OUT      1
#define GCACHEG_NODE_COUNT   218451ULL
#define GCACHEG_RECORD_SIZE  24u
#define GCACHEG_SENTINEL     0xFFFFFFFFFFFFFFFFULL  /* пустой слот children[] */

#pragma pack(push, 1)

/* Заголовок файла, ровно 40 байт, little-endian, без выравнивания.
 * Гиперпараметры генерации (page_size, backprob, seed, min_step_nodes)
 * в файл намеренно не пишутся. */
typedef struct {
    char     magic[8];             /* "GCACHEG1"                      */
    uint32_t version;
    uint64_t node_count;
    uint32_t record_size;          /* == sizeof(gcacheg_node_t)       */
    uint32_t fan_out;
    uint64_t root_index;           /* индекс стартовой вершины обхода */
    uint32_t flags;                /* bit0: 1 = граф ацикличен (DAG)  */
} gcacheg_header_t;

/* Запись одной вершины, 24 байт. */
typedef struct {
    int64_t  value;                    /* payload, можно менять при записи */
    uint32_t degree;                   /* фактическое число детей <= fan_out */
    uint32_t reserved;
    uint64_t children[GCACHEG_FAN_OUT]; /* индексы; неисп. слоты = SENTINEL  */
} gcacheg_node_t;

#pragma pack(pop)

_Static_assert(sizeof(gcacheg_header_t) == 40, "header size mismatch");
_Static_assert(sizeof(gcacheg_node_t) == GCACHEG_RECORD_SIZE, "record size mismatch");

/* offset(i) = header + i * record_size, O(1) доступ по индексу */
static inline uint64_t gcacheg_node_offset(uint64_t index) {
    return (uint64_t)sizeof(gcacheg_header_t) + index * (uint64_t)sizeof(gcacheg_node_t);
}
```