# Предварительный план Triage

Полный маршрут standard; риск medium, уверенность high. Это заготовка для Architect, не согласованный план исполнения.

- AC1: attempt — int >= 0 без bool; base_delay/max_delay/remaining — конечные int/float без bool, base_delay и max_delay > 0, remaining >= 0; любые некорректные аргументы дают ValueError.
- AC2: Задержка min(max_delay, base_delay * 2**attempt) возвращается при delay <= remaining; при remaining == 0 или delay > remaining возвращается None.
- AC3: attempt=10**9 быстро возвращает ограниченный результат без огромной степени, переполнения и зависания; функция чистая, без внешних зависимостей, ожиданий, сети, часов и случайности.
- AC4: Адресные unittest покрывают нормальные случаи, границы, точный и исчерпанный бюджет, bool, отрицательные/нечисловые/NaN/inf аргументы и огромный attempt; README описывает контракт.
- AC5: Существующая constant_delay и поведение вне задачи сохранены относительно base 067c6b554b31cd8929bc58bd4402ab3fcd5d9aae; продуктовые изменения только retry_policy.py, tests/test_retry_policy.py, README.md.

1. Planner подготовит PLAN.json для AC1–AC5 в пределах трёх продуктовых файлов. Opponent проверит границы чисел и сложность; владелец независимо согласует план в Telegram.
2. Builder в Work/Docker реализует функцию, адресные тесты и README после согласования. Быстрая проверка: scripts/agent-check --phase quick; адресная: python3 -m unittest discover -s tests -p test_retry_policy.py -v.
3. Контроллер отдельно выполнит Verify (python3 -m unittest discover -s tests -v), затем Review по сохранённым проверкам и Security; приёмка владельца в Telegram предшествует PR/CI/merge контроллером.

Не менять AGENTS.md, CI, scripts/, .agent/project.json, skills, модели и правила контроллера. Не запускать полный suite в роли агента. Бюджет: одна техническая и пять ролевых native-сессий; без новых сессий, делегирования, Fix, автоматических повторов/fallback/напоминаний. Назначения моделей из BRIEF отражены в TEAM; request.role не содержит их названий, подтверждать соответствие должен контроллер.

Входы: request.context.artifacts.BRIEF.md и role; журнал решений: request.recovery, owner_decisions пуст. Triage завершает только оценку и документы; следующий шаг — Spec контроллером.
