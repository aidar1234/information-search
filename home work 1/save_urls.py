from bs4 import BeautifulSoup

# Страница, с которой был взят HTML: https://ilibrary.ru/author/chekhov/form.8/l.all/index.html
html_code = """
<html>
<div class="list" style="margin: 0.5em 1em;"><p><a href="/text/1367/p.1/index.html">Агафья</a></p><p><a
    href="/text/452/p.1/index.html">Анна на шее</a></p><p><a href="/text/1137/p.1/index.html">Анюта</a></p><p><a
    href="/text/1190/p.1/index.html">Ариадна</a></p><p><a href="/text/1185/p.1/index.html">Архиерей</a></p><p><a
    href="/text/1541/p.1/index.html">Бабы</a></p><p><a href="/text/86/p.1/index.html">Барыня</a></p><p><a
    href="/text/1145/p.1/index.html">Беглец</a></p><p><a href="/text/1368/p.1/index.html">Беда</a> ⟨1886⟩</p><p><a
    href="/text/1546/p.1/index.html">Беда</a> ⟨1887⟩</p><p><a href="/text/1048/p.1/index.html">Беззащитное существо</a>
</p><p><a href="/text/1143/p.1/index.html">Белолобый</a></p><p><a href="/text/1138/p.1/index.html">Беседа пьяного с
    трезвым чёртом</a></p><p><a href="/text/1351/p.1/index.html">Брак по расчету</a> <i><span class="t10pt">(Роман в 2-х частях)</span></i>
</p><p><a href="/text/1353/p.1/index.html">Брожение умов</a> <i><span
    class="t10pt">(Из летописи одного города)</span></i></p><p><a href="/text/46/p.1/index.html">В вагоне</a></p><p><a
    href="/text/1104/p.1/index.html">В потемках</a></p><p><a href="/text/1563/p.1/index.html">В ссылке</a></p><p><a
    href="/text/983/p.1/index.html">Ванька</a></p><p><a href="/text/1371/p.1/index.html">Ведьма</a></p><p><a
    href="/text/1361/p.1/index.html">Верочка</a></p><p><a href="/text/1354/p.1/index.html">Винт</a></p><p><a
    href="/text/1129/p.1/index.html">Водевиль</a></p><p><a href="/text/1370/p.1/index.html">Восклицательный знак</a> <i><span
    class="t10pt">(Святочный рассказ)</span></i></p><p><a href="/text/1102/p.1/index.html">Враги</a></p><p><a
    href="/text/1357/p.1/index.html">Выигрышный билет</a></p><p><a href="/text/1133/p.1/index.html">Горе</a></p><p><a
    href="/text/52/p.1/index.html">Грешник из Толедо</a> <i><span class="t10pt">(Перевод с испанского)</span></i></p><p>
    <a href="/text/1139/p.1/index.html">Гриша</a></p><p><a href="/text/976/p.1/index.html">Дама с собачкой</a></p><p><a
    href="/text/1372/p.1/index.html">Дачники</a></p><p><a href="/text/104/p.1/index.html">Два скандала</a></p><p><a
    href="/text/82/p.1/index.html">Двадцать девятое июня</a> <i><span class="t10pt">(Рассказ охотника, никогда в цель не попадающего)</span></i>
</p><p><a href="/text/1136/p.1/index.html">Детвора</a></p><p><a href="/text/99/p.1/index.html">Добрый знакомый</a></p>
    <p><a href="/text/1050/p.1/index.html">Дом с мезонином</a> <i><span class="t10pt">(Рассказ художника)</span></i></p>
    <p><a href="/text/1360/p.1/index.html">Дома</a></p><p><a href="/text/1134/p.1/index.html">Дорогая собака</a></p><p>
        <a href="/text/1549/p.1/index.html">Дорогие уроки</a></p><p><a href="/text/1182/p.1/index.html">Дочь
        Альбиона</a></p><p><a href="/text/1181/p.1/index.html">Драма</a> ⟨1887⟩</p><p><a
        href="/text/995/p.1/index.html">Душечка</a></p><p><a href="/text/1374/p.1/index.html">Егерь</a></p><p><a
        href="/text/42/p.1/index.html">Жены артистов</a> <i><span class="t10pt">(Перевод... с португальского)</span></i>
    </p><p><a href="/text/87/p.1/index.html">Живой товар</a></p><p><a href="/text/34/p.1/index.html">За двумя зайцами
        погонишься, ни одного не поймаешь</a></p><p><a href="/text/39/p.1/index.html">За яблочки</a></p><p><a
        href="/text/57/p.1/index.html">Забыл!!</a></p><p><a href="/text/1342/p.1/index.html">Загадочная натура</a></p>
    <p><a href="/text/72/p.1/index.html">Зеленая коса</a> <i><span class="t10pt">(Маленький роман)</span></i></p><p><a
        href="/text/1362/p.1/index.html">Зиночка</a></p><p><a href="/text/1073/p.1/index.html">Злой мальчик</a></p><p><a
        href="/text/992/p.1/index.html">Злоумышленник</a></p><p><a href="/text/100/p.1/index.html">Идиллия — увы и
        ах!</a></p><p><a href="/text/437/p.1/index.html">Ионыч</a></p><p><a href="/text/59/p.1/index.html">Исповедь, или
        Оля, Женя, Зоя</a> <i><span class="t10pt">(Письмо)</span></i></p><p><a href="/text/1560/p.1/index.html">История
        одного торгового предприятия</a></p><p><a href="/text/1132/p.1/index.html">Канитель</a></p><p><a
        href="/text/1146/p.1/index.html">Каштанка</a></p><p><a href="/text/74/p.1/index.html">Корреспондент</a></p><p><a
        href="/text/1343/p.1/index.html">Кот</a></p><p><a href="/text/83/p.1/index.html">Который из трех?</a> <i><span
        class="t10pt">(Старая, но вечно новая история)</span></i></p><p><a href="/text/460/p.1/index.html">Крыжовник</a>
    </p><p><a href="/text/1100/p.1/index.html">Кухарка женится</a></p><p><a href="/text/80/p.1/index.html">Летающие
        острова</a> <i><span class="t10pt">Соч. Жюля Верна</span></i></p><p><a href="/text/988/p.1/index.html">Лошадиная
        фамилия</a></p><p><a href="/text/1047/p.1/index.html">Мальчики</a></p><p><a
        href="/text/1130/p.1/index.html">Маска</a></p><p><a href="/text/1074/p.1/index.html">Мелюзга</a></p><p><a
        href="/text/98/p.1/index.html">Месть</a></p><p><a href="/text/1347/p.1/index.html">На гвозде</a></p><p><a
        href="/text/1141/p.1/index.html">На мельнице</a></p><p><a href="/text/1349/p.1/index.html">На охоте</a></p><p><a
        href="/text/1365/p.1/index.html">На пути</a></p><p><a href="/text/1045/p.1/index.html">Налим</a></p><p><a
        href="/text/92/p.1/index.html">Нарвался</a></p><p><a href="/text/1356/p.1/index.html">Не в духе</a></p><p><a
        href="/text/1184/p.1/index.html">Невеста</a></p><p><a href="/text/1547/p.1/index.html">Ненастье</a></p><p><a
        href="/text/88/p.1/index.html">Ненужная победа</a> <i><span class="t10pt">(Рассказ)</span></i></p><p><a
        href="/text/93/p.1/index.html">Неудачный визит</a></p><p><a href="/text/1144/p.1/index.html">Нищий</a></p><p><a
        href="/text/1348/p.1/index.html">О женщины, женщины!..</a></p><p><a href="/text/461/p.1/index.html">О любви</a>
    </p><p><a href="/text/84/p.1/index.html">Он и она</a></p><p><a href="/text/1341/p.1/index.html">Орден</a></p><p><a
        href="/text/36/p.1/index.html">Папаша</a></p><p><a href="/text/1540/p.1/index.html">Пари</a></p><p><a
        href="/text/40/p.1/index.html">Перед свадьбой</a></p><p><a href="/text/97/p.1/index.html">Пережитое</a> <i><span
        class="t10pt">(Психологический этюд)</span></i></p><p><a href="/text/1373/p.1/index.html">Переполох</a></p><p><a
        href="/text/1044/p.1/index.html">Пересолил</a></p><p><a href="/text/43/p.1/index.html">Петров день</a></p><p><a
        href="/text/706/p.1/index.html">Попрыгунья</a></p><p><a href="/text/1558/p.1/index.html">После театра</a></p><p>
        <a href="/text/1189/p.1/index.html">Припадок</a></p><p><a href="/text/79/p.1/index.html">Пропащее дело</a>
        <i><span class="t10pt">(Водевильное происшествие)</span></i></p><p><a
        href="/text/1049/p.1/index.html">Радость</a></p><p><a href="/text/984/p.1/index.html">Размазня</a></p><p><a
        href="/text/1103/p.1/index.html">Репетитор</a></p><p><a href="/text/91/p.1/index.html">Речь и ремешок</a></p><p>
        <a href="/text/1366/p.1/index.html">Розовый чулок</a></p><p><a href="/text/1142/p.1/index.html">Роман с
        контрабасом</a></p><p><a href="/text/977/p.1/index.html">Рыбья любовь</a></p><p><a
        href="/text/1358/p.1/index.html">Свадьба</a></p><p><a href="/text/73/p.1/index.html">«Свидание хотя и
        состоялось, но...»</a></p><p><a href="/text/1548/p.1/index.html">Свирель</a></p><p><a
        href="/text/1363/p.1/index.html">Святою ночью</a></p><p><a href="/text/75/p.1/index.html">Сельские эскулапы</a>
    </p><p><a href="/text/1187/p.1/index.html">Сирена</a></p><p><a href="/text/81/p.1/index.html">Скверная история</a>
        <i><span class="t10pt">Нечто романообразное</span></i></p><p><a href="/text/978/p.1/index.html">Скрипка
        Ротшильда</a></p><p><a href="/text/462/p.1/index.html">Случай из практики</a></p><p><a
        href="/text/987/p.1/index.html">Смерть чиновника</a></p><p><a href="/text/1369/p.1/index.html">Событие</a></p>
    <p><a href="/text/1564/p.1/index.html">Соседи</a></p><p><a href="/text/683/p.1/index.html">Спать хочется</a></p><p>
        <a href="/text/1350/p.1/index.html">Справка</a></p><p><a href="/text/1562/p.1/index.html">Страх</a> <i><span
        class="t10pt">(Рассказ моего приятеля) </span></i></p><p><a href="/text/979/p.1/index.html">Студент</a></p><p><a
        href="/text/48/p.1/index.html">Суд</a></p><p><a href="/text/1071/p.1/index.html">Супруга</a></p><p><a
        href="/text/1359/p.1/index.html">Счастье</a></p><p><a href="/text/464/p.1/index.html">Толстый и тонкий</a></p>
    <p><a href="/text/981/p.1/index.html">Тоска</a></p><p><a href="/text/1135/p.1/index.html">Тряпка</a> <i><span
        class="t10pt">(Сценка)</span></i></p><p><a href="/text/38/p.1/index.html">Тысяча одна страсть или страшная
        ночь</a> <i><span class="t10pt">(Роман в одной части с эпилогом)</span></i></p><p><a
        href="/text/1046/p.1/index.html">Унтер Пришибеев</a></p><p><a href="/text/1355/p.1/index.html">Устрицы</a></p>
    <p><a href="/text/1188/p.1/index.html">Учитель</a></p><p><a href="/text/1159/p.1/index.html">Учитель словесности</a>
    </p><p><a href="/text/463/p.1/index.html">Хамелеон</a></p><p><a href="/text/982/p.1/index.html">Хирургия</a></p><p>
        <a href="/text/1101/p.1/index.html">Хористка</a></p><p><a href="/text/1364/p.1/index.html">Хорошие люди</a></p>
    <p><a href="/text/90/p.1/index.html">Цветы запоздалые</a></p><p><a href="/text/438/p.1/index.html">Человек в
        футляре</a></p><p><a href="/text/1051/p.1/index.html">Шуточка</a></p><p><a href="/text/1131/p.1/index.html">Экзамен
        на чин</a></p>
</div>
</html>
"""

base_url = "https://ilibrary.ru"

soup = BeautifulSoup(html_code, 'html.parser')

links = [base_url + a['href'] for a in soup.find_all('a', href=True)]

urls = links[:100]

with open("urls.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(urls))

print("Извлеченные URL:")
print("\n".join(urls))
