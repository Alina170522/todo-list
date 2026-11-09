const pluralRules = new Intl.PluralRules('ru-RU')

/**
 * Склонение по числу: plural(5, { one: 'дело', few: 'дела', many: 'дел' }) → 'дел'
 */
export function plural(count, forms) {
  return forms[pluralRules.select(count)] ?? forms.many
}

export const TASK_FORMS = { one: 'дело', few: 'дела', many: 'дел', other: 'дела' }
