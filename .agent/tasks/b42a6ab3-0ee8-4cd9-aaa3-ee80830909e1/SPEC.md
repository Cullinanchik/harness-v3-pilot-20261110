# Предварительная спецификация Triage

Цель: добавить чистый расчёт экспоненциальной задержки с ограничением и бюджетом.

- AC1: attempt — int >= 0 без bool; base_delay/max_delay/remaining — конечные int/float без bool, base_delay и max_delay > 0, remaining >= 0; любые некорректные аргументы дают ValueError.
- AC2: Задержка min(max_delay, base_delay * 2**attempt) возвращается при delay <= remaining; при remaining == 0 или delay > remaining возвращается None.
- AC3: attempt=10**9 быстро возвращает ограниченный результат без огромной степени, переполнения и зависания; функция чистая, без внешних зависимостей, ожиданий, сети, часов и случайности.
- AC4: Адресные unittest покрывают нормальные случаи, границы, точный и исчерпанный бюджет, bool, отрицательные/нечисловые/NaN/inf аргументы и огромный attempt; README описывает контракт.
- AC5: Существующая constant_delay и поведение вне задачи сохранены относительно base 067c6b554b31cd8929bc58bd4402ab3fcd5d9aae; продуктовые изменения только retry_policy.py, tests/test_retry_policy.py, README.md.

Область: retry_policy.py, tests/test_retry_policy.py, README.md и обязательные документы задачи. Исходное значение constant_delay() == 1 — наблюдение baseline, а не новый отдельный продуктовый контракт. Действует требование сохранить существующую функцию. UI, UAT и миграции не нужны.
