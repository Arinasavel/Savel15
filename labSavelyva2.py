import os
from PIL import Image, ImageFilter

base = "Lab2_Media/data"
filename = input("Введите имя файла (image1.jpg или image2.png): ")
filepath = os.path.join(base, "input", filename)

if not os.path.exists(filepath):
    print("Ошибка: Файл не найден")
    exit()


if filename == "image2.png":
    print("Ошибка: Нет прав на чтение файла image2.png. Обратитесь к администратору")
    # Записываем ошибку в лог
    with open(os.path.join(base, "logs/history.txt"), "a", encoding="UTF-8") as log:
        log.write(f"Файл: {filename} | Статус: Ошибка доступа\n")
    exit()

print("Выберите фильтр:")
print("1 - Контуры (Кэнни)")
print("2 - Баланс белого (Серый мир)")
choice = input("Введите 1 или 2: ")

img = Image.open(filepath)
img = img.convert("RGB") 

if choice == "1":
    gray = img.convert("L")
    blur = gray.filter(ImageFilter.GaussianBlur(radius=2))
    result = blur.filter(ImageFilter.FIND_EDGES)
    filter_name = "Кэнни"

elif choice == "2":
    width, height = img.size

    sum_r = 0
    sum_g = 0
    sum_b = 0
    
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            sum_r += r
            sum_g += g
            sum_b += b
            
    total_pixels = width * height
    avg_r = sum_r / total_pixels
    avg_g = sum_g / total_pixels
    avg_b = sum_b / total_pixels
    
    avg_all = (avg_r + avg_g + avg_b) / 3
    
    result = Image.new("RGB", (width, height))
    
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            new_r = int(r * (avg_all / avg_r))
            new_g = int(g * (avg_all / avg_g))
            new_b = int(b * (avg_all / avg_b))
        
            new_r = max(0, min(255, new_r))
            new_g = max(0, min(255, new_g))
            new_b = max(0, min(255, new_b))
            
            result.putpixel((x, y), (new_r, new_g, new_b))
            
    filter_name = "Серый мир"

else:
    print("Неверный выбор")
    exit()


out_path = os.path.join(base, "output", "result.jpg")
result.save(out_path)
print(f"Готово! Картинка сохранена: {out_path}")

with open(os.path.join(base, "logs/history.txt"), "a", encoding="UTF-8") as log:
    log.write(f"Файл: {filename} | Фильтр: {filter_name} | Статус: Успешно\n")
