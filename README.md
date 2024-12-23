# ucu_discrete_project
1. Вступ
Задача пошуку найкоротшого шляху є однією з ключових у галузях, пов’язаних із графовими структурами, зокрема в логістиці чи будівництві. У межах цього проекту ми розглядаємо задачу визначення найкоротшого шляху між двома заданими точками на прямокутній ділянці, яка представлена у вигляді матриці висот.
Основною метою проекту є розробка алгоритму, що знаходить шлях із мінімальною фізичною довжиною між двома точками з урахуванням рельєфу поверхні. Для цього використовуються математичні принципи обчислення відстаней у тривимірному просторі та алгоритм A* (A-star), який є одним із найефективніших методів для пошуку найкоротшого шляху на графах. Як евристичну функцію ми використовуємо Manhattan distance, оскільки вона ефективно враховує структуру прямокутної сітки, що описує ландшафт.
Ця задача є поширенно і її практичне застосування включає:
планування транспортних маршрутів у складних ландшафтах;
оптимізацію будівництва доріг або інженерних конструкцій;
географічний аналіз територій для визначення найзручніших шляхів.


3. Вхідні дані
Програма отримує вхідні дані, такі як:
Прямокутна матриця, що представлена у форматі CSV-файлу.
Кожен рядок у файлі відповідає рядку матриці.
Елементи в рядках розділені комами.
Значення кожної комірки — це висота відповідної точки.

Кінцева і Початкова точка.


Початкова точка (AA) та кінцева точка (BB) передаються як координати у форматі пар індексів (i,j)(i, j), де i — номер рядка, а j — номер стовпця.
Приклад: A=(0,1),B=(2,3)
Вимоги до даних
Значення висот у матриці повинні бути числовими (цілі або дійсні числа).
Початкова та кінцева точки повинні бути в межах розмірів матриці.
Ці вхідні дані дозволяють алгоритму створити граф прямокутної ділянки та виконати пошук найкоротшого шляху між заданими точками з урахуванням висот.

3 Алгоритм A*
Для розв'язання задачі було використано алгоритм A* (A-star) з евристикою Manhattan distance, який дозволяє ефективно знаходити найкоротший шлях між двома точками на прямокутній сітці, враховуючи висоти.
A* працює за принципом комбінування:
gg: фактична вартість шляху від початкової точки до поточної (відстань, яку вже подолано).
hh: евристична оцінка залишкової відстані до кінцевої точки (оцінка, скільки ще потрібно пройти).
Загальна оцінка для кожного вузла (клітинки) обчислюється як:
f=g+hf = g + h
де ff — це загальна оцінка, gg — фактична вартість шляху, а hh — евристика (наприклад, Manhattan distance).
gg: це просто відстань від початкової точки до поточної точки.
hh: це евристична оцінка відстані від поточної точки до кінцевої. У нашій реалізації використовується Manhattan distance, яка обчислюється як: h=∣xcurrent−xdest∣+∣ycurrent−ydest∣h = |x_{\text{current}} - x_{\text{dest}}| + |y_{\text{current}} - y_{\text{dest}}| Це означає, що евристика вимірює горизонтальні та вертикальні відстані, ігноруючи діагональні переміщення.
Ключові компоненти алгоритму
Черга з пріоритетами: Алгоритм використовує чергу з пріоритетами (черга heapq), щоб вибирати вузли з найменшою оцінкою ff. Це дозволяє швидко знаходити найбільш перспективні шляхи.


Перевірка всіх можливих рухів: Алгоритм перевіряє всі можливі сусідні клітинки (вліво, вправо, вгору, вниз), для кожної з яких обчислюється нова оцінка ff. Ось як це відбувається:


Для кожної сусідньої клітинки обчислюється вартість руху через зміну висоти між сусідніми точками (використовуючи функцію calculate_height_cost).
Якщо клітинка не була відвідана раніше, її додають до черги з пріоритетами.
Функція евристики: Функція calculate_h_value використовує Manhattan distance для обчислення евристики, яка визначає приблизну відстань до цільової точки.


Відновлення шляху: Як тільки алгоритм знаходить цільову точку, він використовує таблицю батьківських вузлів для відновлення шляху, йдучи від кінцевої точки до початкової. Це відбувається у функції trace_path.


Покроковий процес виконання
Алгоритм додає початкову точку в чергу з пріоритетами з оцінкою f=g+hf = g + h, де g=0g = 0 і hh обчислюється як Manhattan distance до кінцевої точки.
Далі алгоритм обробляє вузли по черзі, завжди вибираючи вузол з найменшим значенням ff.
Для кожного вузла перевіряються його сусіди, для кожного з яких обчислюється нова вартість руху та евристика.
Алгоритм продовжує обробку, поки не знайде цільову точку або не вичерпає всі варіанти.
Якщо шлях знайдений, алгоритм відновлює шлях, використовуючи таблицю батьків.
Завершення
Якщо шлях знайдений, він виводиться як послідовність координат. Якщо шлях неможливий (наприклад, через наявність перешкод), програма виводить повідомлення "No path found!".
Особливості обробки великих даних
3. Реалізація
Для реалізації алгоритму пошуку найкоротшого шляху між двома точками на прямокутній ділянці було використано мову програмування Python.

Використані бібліотеки
argparse:


Використовується для обробки аргументів командного рядка. Це дозволяє зручно передавати параметри при запуску програми (шлях до файлу та координати початкової і кінцевої точки).
heapq:


Бібліотека для роботи з чергами з пріоритетами, що використовується для зберігання та вибору вузлів з найменшим значенням f=g+hf = g + h. Це прискорює пошук шляху, оскільки алгоритм завжди обирає найбільш перспективний вузол для подальшої обробки.
math:


Бібліотека для математичних операцій, зокрема для обчислення відстані, якщо потрібно врахувати рух по діагоналі (наприклад, коригування вартості руху при діагональних переміщеннях).
Архітектура програми
Програма складається з кількох основних функцій, що взаємодіють між собою для виконання задачі пошуку найкоротшого шляху на прямокутній ділянці. Ось детальний опис того, як працюють основні частини коду:
Основна функція main()


Це точка входу в програму, яка забезпечує взаємодію з користувачем через командний рядок. Вона виконує наступні кроки:
Парсинг аргументів командного рядка за допомогою argparse:
Отримує шлях до файлу з матрицею висот.
Отримує координати початкової та кінцевої точок через параметри --src та --dest.
Зчитування даних з файлу:
Відкривається файл за переданим шляхом.
Кожен рядок з файлу перетворюється на список чисел (висот), який додається до загальної матриці grid.
Виклик алгоритму A*:
Після зчитування матриці та отримання координат початкової та кінцевої точок, викликається функція a_star.a_star_search_with_height(), яка реалізує основний пошук шляху.
Виведення результату:
Якщо шлях знайдено, програма виводить його.
Якщо шлях неможливий, виводиться повідомлення "No path found!".
Функції модуля a_star.py


Цей модуль містить основний алгоритм A* для пошуку найкоротшого шляху з урахуванням висот. Ось основні функції цього модуля:


is_in_grid(point, rows, cols)


Перевіряє, чи знаходиться точка в межах заданої матриці (сітки).
Як це працює: Перевіряє, чи координати точки (x,y)(x, y) знаходяться в межах дозволеного діапазону індексів для рядків і стовпців матриці.
Приклад використання: is_in_grid((2, 3), 5, 5) повертає True, якщо точка всередині матриці розміру 5×55 \times 5.
calculate_h_value(point, dest)


Обчислює евристичну оцінку відстані між поточною точкою і кінцевою за допомогою Manhattan distance.
Як це працює: Визначається різниця між координатами поточної точки та цільової точки по горизонталі та вертикалі і підсумовується.
Приклад використання: Для точок (0, 0) та (3, 4) ця функція повертає значення 7 (тобто ∣3−0∣+∣4−0∣=7|3-0| + |4-0| = 7).
calculate_height_cost(current_height, next_height)


Обчислює вартість переміщення між двома точками з урахуванням змін висоти.
Як це працює: Вартість переміщення визначається як абсолютна різниця між висотами двох точок. Це дозволяє алгоритму враховувати зміну рельєфу при виборі шляху.
Приклад використання: Якщо поточна висота 9, а наступна 10, функція повертає вартість руху 1.
trace_path(cell_details, dest)


Відновлює шлях з кінцевої точки до початкової, використовуючи таблицю батьківських вузлів.
Як це працює: Після знаходження цільової точки, ця функція відновлює шлях, йдучи від кінцевої точки через її батьківські вузли до початкової точки.
Приклад використання: Якщо таблиця батьківських вузлів виглядає так:
 cell_details = [[{'parent': None}, {'parent': (0, 0)}], [{'parent': (0, 0)}, {'parent': (1, 0)}]]
 Функція відновлює шлях: [(0, 0), (1, 0), (1, 1)].
a_star_search_with_height(grid, src, dest)


Основна функція алгоритму A*. Вона виконує пошук шляху з початкової точки до кінцевої.
Як це працює: Алгоритм використовує евристичну функцію для оцінки відстані до цілі, а також обчислює вартість кожного руху між точками з урахуванням зміни висоти.
Кожен вузол додається в чергу з пріоритетами на основі його оцінки ff. Алгоритм обирає вузли з мінімальним значенням ff для подальшої обробки.
Обробка файлів та зчитування даних


У функції main() відбувається зчитування файлу, що містить матрицю висот. Кожен рядок файлу перетворюється на список чисел, і ці списки додаються до загальної матриці grid. Якщо файл не знайдений або його не можна відкрити, виводиться повідомлення про помилку.
Модель та сайт
Основна функція main() для обробки терену:


main() — це точка входу в програму, де виконується обробка даних та їх експортування:
Згладжування сітки: За допомогою функції smooth_grid() ми обробляємо сітку висот, додаючи додаткові точки між сусідніми точками, щоб забезпечити плавніший перехід.
Експорт в формат GLB: Функція export_elevation_to_glb() відповідає за перетворення сітки висот у 3D-модель терену та її експорт у формат GLB, що є оптимальним форматом для 3D-моделей, які можна використовувати в різних додатках та на веб-сайтах.
Функція згладжування smooth_grid():


smooth_grid() згладжує дані сітки висот, додаючи нові точки між кожними двома сусідніми точками. Це дає змогу уникнути різких переходів та зробити рельєф більш плавним. Для цього функція використовує find_connecting_points() для обчислення нових точок.
Функція генерації кольорової карти терену create_terrain_colormap():


create_terrain_colormap() генерує кастомну кольорову карту, що відображає різні рівні висот, від темно-синього для води або низьких долин до білого для гірських вершин. Кольорова карта побудована за допомогою Matplotlib і використовує палітри кольорів, які відповідають природним характеристикам терену.
Функція створення 3D-терену elevation_grid_to_mesh():


elevation_grid_to_mesh() перетворює сітку висот у 3D-модель, застосовуючи Delaunay triangulation для створення тріангуляції, що дозволяє побудувати 3D-сітку терену.
Вершини цієї сітки отримують кольори на основі їх висоти за допомогою колірної карти, створеної в попередній функції. Це дає можливість візуалізувати рельєф у вигляді 3D-моделі з природними кольорами для різних висот.
Функція експорту GLB export_elevation_to_glb():


Ця функція виконує експорт обробленої сітки висот у 3D-модель у форматі GLB. Вона використовує Trimesh для створення 3D-об'єкта та зберігає його на диск у зазначеному місці. Також виводиться візуалізація кольорової карти для терену, яка зберігається як PNG зображення.
Веб-сервер на Flask:


Веб-сервер на основі Flask дозволяє обробляти запити від користувачів і надавати доступ до файлів, таких як HTML, CSS та JS, а також до 3D-моделей терену. Він використовується для створення простого інтерфейсу, через який користувач може взаємодіяти з програмою.


Маршрут / відповідає за відображення головної сторінки.


Маршрут /path/to/resource дозволяє отримувати доступ до статичних ресурсів, таких як стилі, скрипти або 3D-моделі терену, що зберігаються в папці www/root.

7. Розподіл роботи
Написання коду для виконання алгоритму А*:

Миколайчук Назар: функціЇ is_in_grid is_destination calculate_h_value calculate_height_cost

Яблуновська Анастасія: функція trace_path

Аланія Лілі та Коноваленко Станіслав: функція a_star_search_with_height

Main: Лілі та Настя

Модель та сайт: Коноваленко Станіслав, Миколайчук Назар, Тумак Олена

Звіт та презентація: Тумак Олена
