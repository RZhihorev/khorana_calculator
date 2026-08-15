def khorana_report(
    cancer_site,
    platelets,
    hemoglobin,
    epoetin,
    leukocytes,
    bmi
):

    """
    Рассчитывает балл Khorana для оценки риска ВТЭО
    у амбулаторных пациентов, получающих системную терапию.

    Источник:
    Khorana AA, Kuderer NM, Culakova E, Lyman GH, Francis CW.
    Development and validation of a predictive model for
    chemotherapy-associated thrombosis.
    Blood. 2008;111(10):4902–4907.
    doi:10.1182/blood-2007-10-116327
    """

    total_score = 0
    report = (
        'ШКАЛА KHORANA для оценки риска ВТЭО у пациентов, '
        'получающих химиотерапию\n'
    )

    report += '1. Локализация опухоли: '
    if cancer_site == 'Желудок, поджелудочная железа':
        report += (
            'очень высокий риск (желудок, поджелудочная железа)'
            ' (2 балла);\n'
        )
        total_score += 2
    elif cancer_site == (
            'Лёгкое, лимфома, женская репродуктивная система,'
            ' мочевой пузырь, яичко'):
        report += (
            'высокий риск (лёгкое, лимфома, женская репродуктивная система, '
            'мочевой пузырь, яичко) (1 балл);\n'
        )
        total_score += 1
    else:
        report += 'прочее (0 баллов);\n'

    report += (
        f'2. Количество тромбоцитов до химиотерапии: '
        f'{platelets:.1f} x 10^9/л '
    )
    if platelets < 350:
        report += '(менее 350 x 10^9/л, 0 баллов);\n'
    else:
        report += '(350 x 10^9/л и более, 1 балл);\n'
        total_score += 1

    report += '3. Концентрация гемоглобина и применение эритропоэтина: '
    report += f'{hemoglobin:.1f} г/л, '
    if hemoglobin < 100:
        report += '(менее 100 г/л), '
    else:
        report += '(100 г/л и более), '
    if epoetin:
        report += 'эритропоэтин получает '
    else:
        report += 'эритропоэтин не получает '
    if hemoglobin < 100 or epoetin:
        report += '(1 балл);\n'
        total_score += 1
    else:
        report += '(0 баллов);\n'

    report += (
        '4. Количество лейкоцитов до химиотерапии: '
        f'{leukocytes:.2f} x 10^9/л '
    )
    if leukocytes > 11:
        report += '(более 11 x 10^9/л, 1 балл);\n'
        total_score += 1
    else:
        report += '(11 x 10^9/л и менее, 0 баллов);\n'

    report += f'5. Индекс массы тела: {bmi:.2f} кг/м.кв. '
    if bmi < 35:
        report += '(менее 35 кг/м.кв., 0 баллов);\n'
    else:
        report += '(35 кг/м.кв. и более, 1 балл);\n'
        total_score += 1

    report += f'ВЕРОЯТНОСТЬ РАЗВИТИЯ ТГВ И ТЭЛА: сумма баллов {total_score}'
    if total_score > 2:
        report += (
            ' (высокий риск,'
            ' риск развития ВТЭО за 2-5 месяцев составляет от 6,7% до 7,1%).'
        )
    elif total_score > 0:
        report += (
            ' (умеренный риск,'
            ' риск развития ВТЭО за 2-5 месяцев составляет от 1,8% до 2,0%).'
        )
    else:
        report += (
            ' (низкий риск,'
            ' риск развития ВТЭО за 2-5 месяцев составляет от 0,3% до 0,8%).'
        )
    return report
