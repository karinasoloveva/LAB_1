import tkinter as tk
from tkinter import ttk
import requests

# Функция для получения курса валют с API ПриватБанка
def get_exchange_rate():
    url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"  # API ПриватБанка
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            # Поиск курса USD и EUR
            usd_rate = None
            eur_rate = None
            for rate in data:
                if rate['ccy'] == 'USD':
                    usd_rate = float(rate['sale'])
                elif rate['ccy'] == 'EUR':
                    eur_rate = float(rate['sale'])
            
            if usd_rate and eur_rate:
                return usd_rate, eur_rate
            else:
                print("Ошибка: не удалось получить курсы валют.")
                return None, None
        else:
            print(f"Ошибка: статус {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Ошибка при подключении: {e}")
        return None, None

# Функция для конвертации валюты
def convert_currency():
    try:
        amount = float(grnInput.get())
        usd_rate, eur_rate = get_exchange_rate()
        if not usd_rate or not eur_rate:
            result_label.config(text="Ошибка: не удалось получить курс")
            return
        if currency_var.get() == 'USD':
            result_label.config(text=f"Результат: {amount / usd_rate:.2f} USD")
        elif currency_var.get() == 'EUR':
            result_label.config(text=f"Результат: {amount / eur_rate:.2f} EUR")
        else:
            result_label.config(text="Выберите валюту")
    except ValueError:
        result_label.config(text="Введите корректное значение!")

# Функция для очистки полей
def clear_fields():
    grnInput.delete(0, tk.END)
    result_label.config(text="Результат: ")
    currency_menu.set('Выберите валюту')

# Автоматическое обновление курса каждые 60 секунд
def update_rates():
    usd_rate, eur_rate = get_exchange_rate()
    if usd_rate and eur_rate:
        status_label.config(text=f"Курс обновлен: USD: {usd_rate:.2f}, EUR: {eur_rate:.2f}")
    else:
        status_label.config(text="Ошибка при обновлении курса")
    root.after(60000, update_rates) 

if __name__ == '__main__':
    # Инициализация главного окна
    root = tk.Tk()
    root.title('Конвертер валют')  # заголовок
    root.geometry('600x400')  # увеличенные размеры окна
    root.resizable(width=False, height=False)  # отключение изменения размера

    # Рамка для размещения компонентов
    frame = tk.Frame(root, bg='#e1f0e8')  # рамка для компонентов
    frame.place(relwidth=1, relheight=1)

    # Заголовок
    title = tk.Label(frame, text="Конвертер валют (UAH -> USD/EUR)", font=("Arial", 18, "bold"), bg='#e1f0e8', fg='#333')
    title.pack(pady=20)

    # Поле для ввода суммы
    grn_label = tk.Label(frame, text="Введите сумму в гривнах:", font=("Arial", 16), bg='#e1f0e8')
    grn_label.pack(pady=5)
    
    grnInput = tk.Entry(frame, font=("Arial", 16), bg='white', width=25)  
    grnInput.pack(pady=5)

    # Выпадающий список для выбора валюты
    currency_var = tk.StringVar()
    currency_menu = ttk.Combobox(frame, textvariable=currency_var, font=("Arial", 16), values=['USD', 'EUR'], state='readonly', width=22, height=3)
    currency_menu.set('Выберите валюту')
    currency_menu.pack(pady=10)

    # Кнопка конвертации
    btn_a = tk.Button(frame, text='Конвертировать', font=("Arial", 16), bg='#007ACC', fg='black', width=15, height=2) 
    btn_a.config(command=convert_currency)
    btn_a.pack(pady=5)

    # Кнопка для очистки полей
    btn_b = tk.Button(frame, text='Очистить', font=("Arial", 16), bg='#f44336', fg='black', width=15, height=2)
    btn_b.config(command=clear_fields)
    btn_b.pack(pady=5)

    # Поле для отображения результата
    result_label = tk.Label(frame, text="Результат: ", font=("Arial", 18, "bold"), bg='#e1f0e8', fg='#007ACC')
    result_label.pack(pady=20)

    # Поле для отображения статуса обновления курса
    status_label = tk.Label(frame, text="Курс обновляется...", font=("Arial", 12), bg='#e1f0e8', fg='#333')
    status_label.pack(pady=10)

    # Обновление курсов валют каждые 60 секунд
    update_rates()

    # Запуск основного цикла приложения
    root.mainloop()