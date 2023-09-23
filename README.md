# sign_PDF_CAdESCOM

Модуль реализации подписания PDF-файла.
PDF-файл подписывается ЭЦП (Электронной цифровой подписью) по ГОСТу криптопровайдером КриптоПро.
Доступно расподписание файла и верификация на предмет того, был ли файл подписан именно необходимым сертификатом КриптоПро.
CAdESCOM - (https://docs.cryptopro.ru/cades/reference/cadescom)|КриптоПро.

Вызов объектов интерфейса COM. Библиотека pywin32 (win32com.client in Python) 


## Распаковка проекта
- Установите и активируйте виртуальное окружение:
```
python -m venv venv
```
``` 
source venv/Scripts/activate
``` 
- Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
pip install pywin32

## Технологии

Python 3.11.0, FastAPI 0.95.2, КриптоПро


## В разработке
- Переделка модуля core.py под CAdESCOM через pywin32
- Подпись внутри PDF.


