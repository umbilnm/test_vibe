### VIBE TEST TASK

Streamlit-сервис, классифицирующий скрины на 3 класса:
1) Фото
2) Скрин переписки
3) Анкета с сайта знакомств 

## Подход
Первая идея:
Обращение к API yandex_ocr -> регулярка, которая достает строки вида "hh:mm" с картинки -> отсекаем по трешхолду(пробовал один или два)
+ отдельная регулярка на ДВ вида ", \w+, \d{2}), " (вряд ли кто то будет число из двух цифр выделять запятыми в переписке)
+ регулярка на твинби чтоб вытаскивать строки [Имя, возраст... км], "Полная информация", "Совместимость"
Проблема: на некоторых сайтах знакомств на экране с анкетой у пользователя может быть время последнего появления в сети, что добавляет ложные срабатывания. Если же брать >2 то обрезанные скрины с двумя сообщениями не будут отлавливаться.

Итоговая идея: 
Наскринил переписок, анкет, зафайнтюнил резнет:) \n
*можно добавить регулярку на ДВ ", \w+, \d{2}), ", так как сейчас не будет его ловить, но тут speed/accuracy tradeoff, вызов API у меня занимал ~0.35с 
