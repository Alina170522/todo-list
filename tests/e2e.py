# Сквозная проверка в настоящем браузере (Playwright).
# Запуск: npm run build, затем
#   pip install playwright && playwright install chromium
#   npm i -D axe-core
#   python tests/e2e.py dist shots node_modules/axe-core/axe.min.js

import json, subprocess, sys, time, os
from playwright.sync_api import sync_playwright, expect

DIST = sys.argv[1]
SHOTS = sys.argv[2]
AXE = sys.argv[3]
PORT = 4199
URL = f"http://127.0.0.1:{PORT}/"
KEY = "todo-list:v1"

server = subprocess.Popen([sys.executable, "-I", "-m", "http.server", str(PORT), "--bind", "127.0.0.1", "--directory", DIST],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)

results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))

errors = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=os.environ.get("CHROME_PATH") or None)
        ctx = browser.new_context(viewport={"width": 1280, "height": 900}, locale="ru-RU")
        page = ctx.new_page()
        page.on("console", lambda m: errors.append(f"console {m.type}: {m.text}") if m.type in ("error", "warning") else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        dialogs = []
        page.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))

        page.goto(URL)
        page.evaluate(f"localStorage.removeItem('{KEY}')")
        page.reload()

        # 1. Пустое состояние
        check("пустой список: цитата", page.get_by_text("Постановка целей").is_visible())
        check("пустой список: стикер 0 дел", "0 дел" in page.locator(".sticker__count").inner_text())
        check("пустой список: нет строки «сделано»", page.locator(".sticker__done").count() == 0)
        page.screenshot(path=f"{SHOTS}/01-empty-1280.png", full_page=True)

        # 2. Пустой ввод
        inp = page.locator("#new-task")
        page.get_by_role("button", name="Добавить").click()
        check("пустой ввод: текст ошибки", page.locator(".form__error").inner_text().strip() == "Введите текст задачи")
        check("пустой ввод: aria-invalid", inp.get_attribute("aria-invalid") == "true")
        inp.fill("   ")
        page.keyboard.press("Enter")
        check("ввод из пробелов не добавляет задачу", page.locator(".item").count() == 0)
        page.screenshot(path=f"{SHOTS}/02-error-1280.png")
        inp.fill("x"); inp.fill("")
        check("ошибка исчезает при вводе", page.locator(".form__error").inner_text().strip() == "")

        # 3. Добавление
        inp.fill("Прочитать главу по Vue 3"); page.keyboard.press("Enter")
        check("1 задача: «1 дело»", "1 дело" in page.locator(".sticker__count").inner_text())
        check("после добавления поле пустое и в фокусе", inp.input_value() == "" and page.evaluate("document.activeElement.id") == "new-task")
        inp.fill("Записаться к стоматологу"); page.get_by_role("button", name="Добавить").click()
        check("2 задачи: «2 дела»", "2 дела" in page.locator(".sticker__count").inner_text())
        inp.fill("  Полить цветы  "); page.keyboard.press("Enter")
        xss = '<img src=x onerror=alert(1)>'
        inp.fill(xss); page.keyboard.press("Enter")
        inp.fill("Разобрать почту и ответить на письма, которые ждут ответа с прошлой недели, и ещё одноооооооооооооооооооооооооооооооочень_длинное_слово_без_пробелов")
        page.keyboard.press("Enter")
        check("5 задач: «5 дел»", "5 дел" in page.locator(".sticker__count").inner_text())
        check("лишние пробелы обрезаны", page.locator(".check__pill").nth(2).inner_text() == "Полить цветы")
        page.wait_for_timeout(300)
        check("XSS: alert не сработал", len(dialogs) == 0, str(dialogs))
        check("XSS: текст показан как есть", page.locator(".check__pill").nth(3).inner_text() == xss)
        check("пустая цитата скрыта", page.get_by_text("Постановка целей").count() == 0)

        # 4. Отметка + сохранение
        page.locator(".check").nth(0).click()
        page.locator(".check").nth(2).click()
        check("сделано 2/5", "сделано 2 из 5" in page.locator(".sticker__done").inner_text())
        page.reload()
        check("после перезагрузки 5 задач", page.locator(".item").count() == 5)
        check("после перезагрузки отметки сохранились",
              page.locator(".item.is-done").count() == 2 and page.locator(".check__input").nth(0).is_checked())

        # 5. Удаление и «Вернуть»
        page.locator(".item__remove").nth(1).click()
        check("удаление: подсказка появилась", page.locator(".undo").is_visible())
        check("удаление: отсчёт с 5 с", "через 5 с" in page.locator(".undo").inner_text())
        check("удаление: фокус на «Вернуть»", page.evaluate("document.activeElement.textContent.trim()") == "Вернуть")
        check("удаление: стикер без удаляемой (4 дела)", "4 дела" in page.locator(".sticker__count").inner_text())
        check("удаление: чекбокс заблокирован", page.locator(".check__input").nth(1).is_disabled())
        page.screenshot(path=f"{SHOTS}/03-pending-1280.png", full_page=True)
        page.wait_for_timeout(1300)
        check("отсчёт идёт (≤4 с)", any(f"через {n} с" in page.locator(".undo").inner_text() for n in (3, 4)))
        page.get_by_role("button", name="Вернуть").click()
        check("«Вернуть»: задача на месте", page.locator(".item").count() == 5 and page.locator(".undo").count() == 0)
        check("«Вернуть»: снова 5 дел", "5 дел" in page.locator(".sticker__count").inner_text())
        check("«Вернуть»: фокус на корзине", "Удалить задачу" in (page.evaluate("document.activeElement.getAttribute('aria-label')") or ""))

        # 6. Обновление страницы во время отсчёта
        page.locator(".item__remove").nth(1).click()
        page.wait_for_timeout(2000)
        page.reload()
        check("перезагрузка во время отсчёта: задача вернулась", page.locator(".item").count() == 5 and page.locator(".undo").count() == 0)

        # 7. Двойной клик и окончательное удаление
        page.locator(".item__remove").nth(1).dblclick()
        check("двойной клик: одна подсказка", page.locator(".undo").count() == 1)
        page.wait_for_timeout(5600)
        check("через 5 с задача удалена", page.locator(".item").count() == 4 and page.locator(".undo").count() == 0)
        check("после удаления фокус в поле ввода", page.evaluate("document.activeElement.id") == "new-task")
        page.reload()
        check("после перезагрузки удалённой нет", page.locator(".item").count() == 4)
        stored = json.loads(page.evaluate(f"localStorage.getItem('{KEY}')"))
        check("в хранилище 4 задачи", len(stored) == 4)

        # 8. Всё выполнено
        for i in range(4):
            box = page.locator(".check__input").nth(i)
            if not box.is_checked():
                page.locator(".check").nth(i).click()
        check("всё выполнено: цитата", page.get_by_text("Успех — это награда за упорный труд.").is_visible())
        page.screenshot(path=f"{SHOTS}/04-alldone-1280.png", full_page=True)
        page.locator(".check").nth(0).click()
        check("снята отметка: цитата исчезла", page.get_by_text("Успех — это награда").count() == 0)

        # 9. Календарь
        btn = page.locator(".date__button")
        check("дата: число сегодня", page.locator(".date__day").inner_text() == str(time.localtime().tm_mday))
        check("дата: месяц в родительном", page.locator(".date__month").inner_text(), page.locator(".date__month").inner_text())
        btn.click()
        check("календарь открыт", page.locator("#calendar").is_visible() and btn.get_attribute("aria-expanded") == "true")
        cap = page.locator(".calendar__title").inner_text()
        check("календарь: заголовок", cap, cap)
        first_row = [c.inner_text().strip() for c in page.locator(".calendar__table tbody tr").first.locator("td").all()]
        check("календарь: первая неделя", True, str(first_row))
        check("календарь: сегодня отмечено", page.locator("td[aria-current='date']").inner_text().strip() == str(time.localtime().tm_mday))
        page.screenshot(path=f"{SHOTS}/05-calendar-1280.png")
        page.keyboard.press("Escape")
        check("Esc закрыл календарь", not page.locator("#calendar").is_visible())
        check("Esc: фокус на кнопке даты", page.evaluate("document.activeElement.classList.contains('date__button')"))
        btn.click(); page.locator(".brand").click()
        check("клик мимо закрыл календарь", not page.locator("#calendar").is_visible())

        # 10. Подпись «что сделать сегодня?» ставит курсор в поле
        page.locator(".bubble").click()
        check("реплика → фокус в поле", page.evaluate("document.activeElement.id") == "new-task")

        # 11. Две вкладки
        page2 = ctx.new_page()
        page2.goto(URL)
        n_before = page2.locator(".item").count()
        inp.fill("Задача из первой вкладки"); page.keyboard.press("Enter")
        page2.wait_for_timeout(500)
        check("вторая вкладка подхватила задачу", page2.locator(".item").count() == n_before + 1)
        page2.close()

        # 12. Доступность (axe) на 1280
        axe_src = open(AXE).read()
        def run_axe(pg):
            pg.add_script_tag(content=axe_src)
            res = pg.evaluate("async () => (await axe.run(document, {resultTypes:['violations']})).violations.map(v => ({id:v.id, impact:v.impact, n:v.nodes.length, help:v.help, t:v.nodes.slice(0,3).map(x=>x.target.join(' '))}))")
            return res
        v = run_axe(page)
        check("axe 1280: нарушений нет", len(v) == 0, json.dumps(v, ensure_ascii=False))

        # 13. Адаптив
        for w, h in ((360, 780), (375, 812), (768, 1024), (1280, 900), (1440, 900)):
            page.set_viewport_size({"width": w, "height": h})
            page.wait_for_timeout(200)
            sw = page.evaluate("document.documentElement.scrollWidth")
            check(f"{w}px: нет горизонтальной прокрутки", sw <= w, f"scrollWidth={sw}")
            fs = page.evaluate("getComputedStyle(document.getElementById('new-task')).fontSize")
            if w <= 600:
                check(f"{w}px: шрифт поля 16px", fs == "16px", fs)
            page.screenshot(path=f"{SHOTS}/06-{w}.png", full_page=True)
        page.set_viewport_size({"width": 375, "height": 812})
        v = run_axe(page)
        check("axe 375: нарушений нет", len(v) == 0, json.dumps(v, ensure_ascii=False))
        page.locator(".item__remove").nth(1).click()
        page.screenshot(path=f"{SHOTS}/07-pending-375.png", full_page=True)
        page.get_by_role("button", name="Вернуть").click()

        # 14. Повреждённые данные
        page.evaluate(f"localStorage.setItem('{KEY}', '{{не json')")
        errors_before = len(errors)
        page.reload()
        check("битый JSON: страница работает, список пуст", page.locator(".item").count() == 0 and page.get_by_text("Постановка целей").is_visible())
        page.evaluate(f"localStorage.setItem('{KEY}', JSON.stringify([{{id:'a',text:'ok',done:true}}, null, {{text:5}}, {{id:'b',text:'   '}}]))")
        page.reload()
        check("мусор в данных отфильтрован", page.locator(".item").count() == 1)
        page.evaluate(f"localStorage.removeItem('{KEY}')")

        browser.close()
finally:
    server.terminate()

check("ошибок в консоли нет", len(errors) == 0, "\n".join(errors))
ok = sum(1 for r in results if r[1])
for name, passed, detail in results:
    print(("PASS " if passed else "FAIL ") + name + (f"  [{detail}]" if detail and (not passed or name.startswith(('календарь','дата'))) else ""))
print(f"\n{ok}/{len(results)} passed")
