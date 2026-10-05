# Паспорт системы

## ОС

| Параметр | Значение                                      | Получено из                               |
|----------|-----------------------------------------------|-------------------------------------------|
| Система  | Ubuntu GNU/Linux, x86_64                      | [`uname.txt`](../logs/passport/uname.txt) |
| Ядро     | Linux 6.11.0-29-generic, SMP, PREEMPT_DYNAMIC | [`uname.txt`](../logs/passport/uname.txt) |

## Процессор

| Параметр            | Значение                                         | Получено из                                                                                        |
|---------------------|--------------------------------------------------|----------------------------------------------------------------------------------------------------|
| Модель              | Intel Core i7-4770 @ 3.40 GHz                    | [`lscpu.txt`](../logs/passport/lscpu.txt)                                                          |
| Топология           | 1 сокет, 4 физических ядра, 2 потока на ядро     | [`lscpu.txt`](../logs/passport/lscpu.txt)                                                          |
| Логические CPU      | 8, все доступны и находятся в NUMA-узле 0        | [`lscpu.txt`](../logs/passport/lscpu.txt), [`nproc.txt`](../logs/passport/nproc.txt)               |
| Частоты             | 800–3400 MHz                                     | [`lscpu.txt`](../logs/passport/lscpu.txt)                                                          |
| Кэши                | L1d: 128 KiB; L1i: 128 KiB; L2: 1 MiB; L3: 8 MiB | [`lscpu.txt`](../logs/passport/lscpu.txt), [`proc-cpuinfo.txt`](../logs/passport/proc-cpuinfo.txt) |
| Основные расширения | SSE–SSE4.2, AVX, AVX2, FMA, AES, BMI1/2, VT-x    | [`lscpu.txt`](../logs/passport/lscpu.txt)                                                          |

Пары SMT-потоков одного физического ядра: `0/4`, `1/5`, `2/6`, `3/7` ([`lscpue.txt`](../logs/passport/lscpue.txt)).

## Память и NUMA

| Параметр                      | Значение                                                                 | Получено из                                   |
|-------------------------------|--------------------------------------------------------------------------|-----------------------------------------------|
| Оперативная память            | 16 GiB DDR3-1600: 2 × 8 GiB                                              | [`lshw.txt`](../logs/passport/lshw.txt)       |
| Состояние при снятии паспорта | занято 1,4 GiB; свободно 8,9 GiB; buffers/cache 5,0 GiB; доступно 13 GiB | [`free.txt`](../logs/passport/free.txt)       |
| Swap                          | 15 GiB, занято 305 MiB                                                   | [`free.txt`](../logs/passport/free.txt)       |
| NUMA                          | 1 узел; 15 404 MiB, свободно 9 065 MiB; CPU 0–7                          | [`numactl.txt`](../logs/passport/numactl.txt) |

## Накопитель

| Параметр         | Значение                                                 | Получено из                                                                              |
|------------------|----------------------------------------------------------|------------------------------------------------------------------------------------------|
| Устройство       | `/dev/sda`                                               | [`lshw.txt`](../logs/passport/lshw.txt)                                                  |
| Модель и ёмкость | WDC WD10SPZX-22Z10T1, 1,00 TB                            | [`lshw.txt`](../logs/passport/lshw.txt), [`smartctl.txt`](../logs/passport/smartctl.txt) |
| Тип              | HDD, SMR, 2,5 дюйма, 5400 об/мин                         | [`smartctl.txt`](../logs/passport/smartctl.txt)                                          |
| Интерфейс        | SATA 3.1, 6,0 Гбит/с; секторы 512 Б лог. / 4096 Б физ.   | [`smartctl.txt`](../logs/passport/smartctl.txt)                                          |
| SMART            | Поддерживается и включён; итоговая самопроверка не снята | [`smartctl.txt`](../logs/passport/smartctl.txt)                                          |
