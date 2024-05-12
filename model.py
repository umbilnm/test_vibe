def get_label(features:dict) -> str:
    if not features['text']:
        return "Фото"
    if features['timestamp_count'] > 2:
        return "Скрин переписки"
    if features['dating']:
        return "Анкета"

    
    return "Не удалось определить"