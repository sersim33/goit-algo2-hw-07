# goit-algo2-hw-07



Порівняльний аналіз ефективності двох підходів до обчислення чисел Фібоначчі: із використанням LRU-кешу та з використанням Splay Tree. 
Результати вимірювань часу виконання представлені у вигляді таблиці.

## Результати

| n   | LRU Cache Time (s)       | Splay Tree Time (s)       |
|-----|--------------------------|---------------------------|
| 0   | 5.536000571737531e-07    | 4.907000402454287e-07     |
| 50  | 2.962500002468005e-06    | 9.49969999055611e-06      |
| 100 | 1.5925000298011583e-06   | 2.8899799963255647e-05    |
| 150 | 1.6044999938458203e-06   | 3.1980699986888794e-05    |
| 200 | 1.8319999981031288e-06   | 3.515100006552529e-05     |
| 250 | 1.840699951571878e-06    | 6.021449999025208e-05     |

##
- **LRU Cache**: Підхід із використанням LRU-кешу показав значно кращу продуктивність для великих значень n. Час виконання залишався стабільно низьким (на графіку це видно).
- **Splay Tree**: Підхід із використанням Splay Tree мав більший час виконання, особливо для великих значень n. Це пов'язано з додатковими витратами на операції з деревом.

На основі отриманих результатів можна зробити висновок, що використання LRU-кешу є більш ефективним для обчислення чисел Фібоначчі порівняно з Splay Tree.

## Графік порівняння часу виконання

![Графік порівняння часу виконання](graph.png)

