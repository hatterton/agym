# Agym

Agym - набор инструментов и платформа-песочница для экспериментов в создании искусственного интеллекта в компьютерных играх. Задумывался как аналог [openai/gym](https://github.com/openai/gym).

Ниже приведена демонстрация геймплея.

<img src="././static/gifs/gameplay.gif" width=400>

## Презентация реализованного

В процессе разработки я сталкивался с классическими проблемами и задачами программирования и разработки игр в частности. Ниже приведены показавшиеся мне наиболее интересными пункты, на которых хотелось бы заострить внимание:

- [Геометрические примитивы](#geom-primitives)
- [Обнаружение и обработка столкновений](#geom-collisions)
- [KD-Дерево](#geom-kd-tree)
- [Работа с кодом](#quality-of-code)


<h3 id="geom-primitives"> Геометрические примитивы </h3>

#### Низкоуровневые примитивы

Для решения задачи обнаружения и обработки столкновений был реализован набор низкоуровневых геометрических примитивов таких как:
- Двумерный вектор, она же точка на плоскости, [ссылка на код](./src/geometry/geometry/basic/point.py#L8)
- Прямая на плоскости, [ссылка на код](./src/geometry/geometry/basic/line.py)
- Отрезок на плоскости, [ссылка на код](./src/geometry/geometry/basic/segment.py)

В целях удобства использования у многих примитивов были перегружены математические бинарные и унарные операции: сложения, умножения на скаляр, унарный минус, скалярное произведение и прочее, что позволяет писать более интуитивно понятный код при реализации математических формул для геометрических задач.

Вот так, на пример, выглядит [код](./src/envs/envs/breakout/collisions/precise.py#L7) нахождения момента времени и точки столкновения двух шаров, где все переменные кроме `radius` и `t` являются двумерными векторами:

```python
    radius = ball1.radius
    s1, f1 = ball1.fake_update(dt)
    s2, f2 = ball2.fake_update(dt)

    v1 = f1 - s1
    v2 = f2 - s2
    a = s1 - s2
    b = v1 - v2

    t = -a.scalar(b)
    t = max(0, min(t, b.norm2()))

    shift = a * b.norm2() + b * t

    if shift.norm2() < ((2 * radius - EPS) * b.norm2()) ** 2:
        point = (f1 + f2) / 2
```

#### Геометрические фигуры

Поверх низкоуровневых примитивов был реализован набор геометрических фигур:
- Окружность, [ссылка на код](./src/geometry/geometry/shapes/circle.py)
- Треугольник, [ссылка на код](./src/geometry/geometry/shapes/triangle.py)
- Прямоугольник с параллельными осям сторонами, [ссылка на код](./src/geometry/geometry/shapes/rectangle.py)

#### Нахождения точки пересечения

На базе геометрических фигур же была реализована полиморфная функция для нахождения точки пересечения этих базовых геометрических фигур друг с другом. [Её](./src/geometry/geometry/intersecting.py#L19) сигнатура:

```python
IntersectionStrict = Point
Intersection = Optional[IntersectionStrict]

def get_intersection(a: Shape, b: Shape) -> Intersection:
    ...
```

<h3 id="geom-collisions"> Обнаружение и обработка столкновений </h3>

Для игры breakout хотелось добиться реалистичности поведения шара при столкновении с объектами, в том числе при взаимном столкновении шаров, поэтому "наивная" реализация с "отражением" одной из компонент вектора скорости выглядела недостаточной.

Подходы в обработке столкновений подразделяют на несколько типов:

- A prior (априорная) - обнаружение и обработка столкновения "до" фактического столкновения
- A posterior (апостериорная) - обнаружение и обработка столкновения уже "после" фактического столкновения

Инвариант "в любом момент времени ничего ни с чем не пересекается" показался довольно изящным, и в первом подходе казалось проще его поддерживать. Для его реализации необходимо не допускать таких обновлений положений объектов, которые приводят к пересечению, а каким-либо образом обрабатывать такие ситуации заранее.

#### Непрерывность

Обнаружения столкновений, а также обновление состояния сцены происходит через фиксированные промежутки времени, которые далее будут называться "тиками".

Таким образом в одном тике объекты не пересекаются, а в следующем за ним тике уже может появиться пересечение, которое должно быть обработано.
При высокой скорости объектов относительно друг друга или большой длительности тика, расстояние между ними может быть настолько большим, что правдоподобная обработка такого "столкновения" может оказаться затруднительной даже в теории.

Кроме этого, появляется вероятность возникновения эффекта, при котором идентичные начальные сцены при разной частоте обработки (frame rate) перейдут в разные состояние после некоторой цепочки обработок.

Чтобы всего этого избежать был реализован механизм нахождения точного времени столкновения объектов с заданной погрешностью с последующей обработкой (далее именуемый как "шаг") и обработки тика в некоторое количество обозначенных шагов.

Точное время столкновения [вычисляется](./src/envs/envs/breakout/collisions/detector.py#L39) бинарным поиском. Зная его, сцена обновляется в состояние "за миг до" столкновения. После этого вычисляются столкновения происходящие через "миг", обрабатываются и на этом шаг [заканчивается](./src/envs/envs/breakout/env.py#L121).

Такой механизм позволяется значительно увеличить реалистичность и правдоподобность поведения объектов при столкновении. Ниже приведена небольшая видео-демонстрация с в десятки раз превосходящей игровую скоростью шаров.

<!-- Ниже видео-демонстрация идентичность поведения объектов одной и той же сцены при разном фреймрейте и разном степени замедления видео: -->
<!-- - <гифка сцены при fps 100 и playback 1> -->
<!-- - <гифка сцены при fps 100 и playback 0.1> -->
<!-- - <гифка сцены при fps 20 и playback 0.1> -->
<!-- - <гифка сцены при fps 4 и playback 0.1> -->

<img src="./static/gifs/high_speed.gif" width=300>


<h3 id="geom-kd-tree"> KD-Дерево </h3>

Следующая проблема, о которой я подумал, была проблема производительности. Ведь если предположить, что каждый объект сцены может столкнуться с каждым другом объектом, то "наивная" реализация алгоритма нахождения всех пересечений будет работать за $O(n^2)$, где $n$ - кол-во объектов на сцене.

Есть разные способы чтобы справится с этой проблемой, но из-за претензии на универсальность мной был выбран подход с k-мерным пространственным деревом.

В ходе его работы:

1. Все объекты сцены представляются в виде набора геометрических фигур
2. По набору геометрических фигур рекурсивно строится kd-дерево с некоторое эвристикой выбора разделяющей прямой
3. Опираясь на построенное дерево находятся пары фигур, которые теоретически могут пересекаться и тогда уже проверяются на пресечение полноценно.

Такой подход позволяет вычислить столкновения за условное время $O(n \cdot d + k)$, где $n$ - кол-во объектов, $d$ - глубина дерева $\sim log(n)$, k - кол-во фактических столкновений, что в теории ограничено $O(n^2)$.


Ниже демонстрация разбиение дерева при большом количестве объектов.

<img src="./static/gifs/kdtree.gif" width=400>

А ещё ниже представлена сравнительная видео-демонстрация производительности обоих подходов при увеличении количества объектов.

| Кол-во объектов | "Наивных" подход | KD-деревянный подход |
|-|-|-|
| 5 |  <img src="./static/gifs/naive_5.gif" width=300> | <img src="./static/gifs/kdtree_5.gif" width=300>
| 10 |  <img src="./static/gifs/naive_10.gif" width=300> | <img src="./static/gifs/kdtree_10.gif" width=300>
| 20 |  <img src="./static/gifs/naive_20.gif" width=300> | <img src="./static/gifs/kdtree_20.gif" width=300>

Искушённого читателя может смутить, что падение количества кадров в секунду при увеличении количества объектов не соответствует заявленному в формулах выше. Так происходить из-за того, что формулы выше описывают сложность вычисления пересечений одной сцены, а не тика.
На деле же, в одном тике может быть множество шагов, а в одном шаге несколько сцен. Кроме этого, чем дольше вычисляется текущий тик, тем больше будет длительность следующего тика так как обновлений сцены привязывается ко времени. А также кол-во фактических столкновений линейно влияет на время обсчёта одного тика так как для каждого столкновения нужно вычислить точно время и соответственно сделать шаг.

То есть, чем дольше вычисляется текущий тик, тем больше объём работ будет у следующего тика. Поэтому формулы зависимости количества кадров в секунду от количества объектов будут выглядеть несколько сложнее.

<h3 id="quality-of-code"> Работа с кодом </h3>

Хочется отметить, что качество кода было не последним приоритетом при разработке. Программный продукт разделён на слои, где преимущественно каждый слой работает с 1-2 находящимися ниже слоями, а программирование происходит на уровне [интерфейсов](./src/agym/protocols). Помимо этого для структуризации кода были использованы множество шаблонов проектирования. Упрощённая структура слоёв выглядит так:

1. Слой геометрических примитивов
3. Слой полиморфной функции пересечения фигур. Использует слой 1
4. Слой kd-дерева. Использует слой 1
5. Слой двигателя поиска пересечений фигур сцены. Использует слои 2 и 3
6. Слой поиска пересечений фигур сцены. Использует слой 4 с помощью шаблона проектирования Strategy
8. Слой объектов игры. Использует слои 1
9. Слой логики игры. Использует слои 5 и 6
10. Слой абстракции над фреймворком ввода-вывода. Использует pygame с помощью шаблона проектирования Adapter
11. Слой компонент игры. Использует слои 7 и 8
13. Слой обработки событий. Использует слои 7, 8 и 9 с помощью шаблона проектирования Chain of Responsibility

Также следует отметить, что создание фреймворка ввода-вывода и компонент игры происходит при помощи шаблона проектирования Abstact Factory.

Описанное выше позволяет иметь возможность контроля из [файла конфигурации](./src/agym/settings.py) таких параметров запуска как:

- Фреймворк ввода-вывода
- Тип запускаемой игры и её параметры инициализации
- Тип двигателя поиска пересечения фигур сцены


### Резюме

На этом примечательные пункты достойные внимания пока заканчиваются. Спасибо за внимание.


## Требования

- Python (3.8.1)
- Poetry
- Make

Узнать больше информации об используемых пакетах вы можете найти [здесь](https://github.com/hatterton/agym/blob/develop/src/pyproject.toml).

## Установка

```bash
git lfs install
git lfs pull
make init-env
```

## Запуск

```bash
make run
```

