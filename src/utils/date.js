const LOCALE = 'ru-RU'

const dayMonthFormat = new Intl.DateTimeFormat(LOCALE, { day: 'numeric', month: 'long' })
const weekdayFormat = new Intl.DateTimeFormat(LOCALE, { weekday: 'long' })
const monthFormat = new Intl.DateTimeFormat(LOCALE, { month: 'long' })

/** «ноября» — месяц в родительном падеже, как в «9 ноября» */
export function monthGenitive(date) {
  return dayMonthFormat.formatToParts(date).find((part) => part.type === 'month')?.value ?? ''
}

/** «понедельник» */
export function weekdayName(date) {
  return weekdayFormat.format(date)
}

/** «Ноябрь 2026» — заголовок календаря */
export function monthTitle(date) {
  const month = monthFormat.format(date)
  return `${month.charAt(0).toUpperCase()}${month.slice(1)} ${date.getFullYear()}`
}

export const WEEKDAYS_SHORT = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']

/**
 * Сетка месяца по неделям, неделя начинается с понедельника.
 * Пустые ячейки до первого и после последнего числа — null.
 */
export function monthGrid(date) {
  const year = date.getFullYear()
  const month = date.getMonth()
  // getDay(): 0 — воскресенье. Сдвигаем так, чтобы 0 был понедельником.
  const offset = (new Date(year, month, 1).getDay() + 6) % 7
  const daysInMonth = new Date(year, month + 1, 0).getDate()

  const cells = Array(offset).fill(null)
  for (let day = 1; day <= daysInMonth; day += 1) cells.push(day)
  while (cells.length % 7 !== 0) cells.push(null)

  const weeks = []
  for (let i = 0; i < cells.length; i += 7) weeks.push(cells.slice(i, i + 7))
  return weeks
}

export function isSameDay(a, b) {
  return (
    a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate()
  )
}
