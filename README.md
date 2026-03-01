<div align="center">

<details>
  <summary>🔽 Click to see the English translation. 🔽</summary>

<div align="center"><h1> 🛠 Quick Tools Edit Mode 🛠 </h1>

![description](https://github.com/Constantyn6487/link/blob/main/preview184eng.png?raw)

</div>

**Quick Tools Edit Mode** is a compact toolbox for Blender that removes unnecessary clicks and pop‑up dialogs. All essential operations for weights, shading, and transforms are now reachable with a single click from the side panel or the context menu.

> [!IMPORTANT]  
> The addon works **exclusively in Edit Mode**. In Object Mode all UI elements are automatically hidden to keep the interface clean.

## 🚀 Core Features

<div align="center">

| **Group** | **Functions** |
| :--------- | :---------- |
| **Edge Crease** | Set crease weight (0.00 / 0.50 / 1.00) |
| **Edge Bevel Weight** | Set bevel weight (0.00 / 0.50 / 1.00) |
| **Shade Auto Smooth** | Quick auto‑smooth setup (compatible with Blender 4.2+) |
| **Shade Smooth / Flat** | Instantly switch shading type while staying in Edit Mode |
| **Apply Scale/Rotation** | Apply scale or rotation to geometry without leaving Edit Mode |

</div>

---

### 💡 Brief reference for each operator  

| Operator | ID | Parameters | What it does |
|----------|----|------------|--------------|
| **BUTTON_OT_WeightSet** | `button.weight_set` | `value` (float), `mode` (`CREASE`/`BEVEL`) | Assigns crease‑weight or bevel‑weight to the selected elements. |
| **BUTTON_OT_QuickAction** | `button.quick_action` | `action` (`AUTO_SMOOTH`, `SMOOTH`, `FLAT`, `SCALE`, `ROTATION`) | Performs auto‑smooth, toggles shading, or “applies” scale/rotation to the mesh geometry. |

---

## 🔰 User Interface

### 1. Side panel (N‑panel)  
Tab name: **QuickToolsEditMode** (the tab name can be changed in the addon preferences).  
* **Selection Data:** toggles `Edges` and `Vertices`. They decide which data the weight operators will affect.  
* **Weights:** quick‑set buttons for Crease and Bevel values.  
* **Shade Auto Smooth:** one‑click auto‑smooth activation (works the same way as the object‑mode operator).  
* **Smooth & Transform:** fast shading commands and tools to bake scale/rotation into the mesh.  

### 2. Context menu  
While in **Edit Mesh** mode, right‑click in the 3D Viewport → open **QuickToolsEditMode** submenu.

### 3. Changing the N‑panel tab category  
`Edit → Preferences → Add‑ons → Quick Tools Edit Mode → expand → Tab Category field → type the new name → press Enter`.

<div align="center">

![description](https://github.com/Constantyn6487/link/blob/main/QTEM-Settings.png?raw)

</div>

---

## 🏗 Typical workflow  
1. Enter **Edit Mode** (`Tab`).  
2. *Select the edges/vertices you want to modify.*  
3. In the **Selection Data** block enable **Edges** (or **Vertices**) as needed.  
4. Click a weight button (e.g., `0.50`) → the same weight is instantly applied to all selected elements.  
5. To change **shading**, press **Smooth** or **Flat**.  
6. If you forgot to apply **Scale/Rotation** while you were in Object Mode, press **ApplyScale** or **ApplyRotation** – the transform is baked into the vertices and the object returns to a unit scale / zero rotation.

---

## 📦 Installation & System Requirements  

* **✨ Blender version:** 4.2+ (tested up to the latest 5.x).  
* **📜 License:** GNU General Public License v3.0.  

1. Download the latest `.zip` release from the repository.  
2. In Blender go to `Edit → Preferences → Add‑Ons → Install…` (or `Edit → Preferences → Get Extensions → Install from disk`).  
3. Choose the downloaded file and click **Install Add‑on**.  
4. Tick the box next to **Object: Quick Tools Edit Mode** to enable it (if it isn’t already checked).  

---

## 🔧 Development & Contributions  
Bug reports, feature requests, and pull requests are welcome via the **Issues** section of this repository.  

---  

</details>

</div>

<div align="center"><h1> 🛠 Quick Tools Edit Mode 🛠 </h1>

![description](https://github.com/Constantyn6487/link/blob/main/preview184rus.png?raw)
</div>

**Quick Tools Edit Mode** — это компактный набор инструментов для Blender, который избавляет от лишних кликов и всплывающих окон. Все ключевые операции по весам (weights), затенению (shading) и трансформациям теперь доступны в один клик прямо из боковой панели или контекстного меню.

> [!IMPORTANT]
> Аддон работает исключительно в **Edit Mode**. В объектном режиме элементы управления автоматически скрываются, чтобы не загромождать интерфейс.

## 🚀 Основные функции

<div align="center">

| **Группа** | **функций** |
| :--------- | :---------- |
| **Edge Crease** | Установка веса сгиба (0.00 / 0.50 / 1.00) |
| **Edge Bevel Weight** | Установка веса фаски (0.00 / 0.50 / 1.00) | 
| **Shade Auto Smooth** | Быстрая настройка автосглаживания (совместимо с Blender 4.2+) |
| **Shade Smooth / Flat** | Мгновенное переключение типа затенения из Edit Mode
| **Apply Scale/Rotation** | Применение трансформаций к геометрии, не выходя из Edit Mode |

</div>

---

### 💡 Краткая справка по каждому оператору  

| Оператор | ID | Параметры | Что делает |
|----------|----|-----------|------------|
| **BUTTON_OT_WeightSet** | `button.weight_set` | `value` (float), `mode` (`CREASE`/`BEVEL`) | Устанавливает crease‑weight или bevel‑weight выбранным элементам. |
| **BUTTON_OT_QuickAction** | `button.quick_action` | `action` (`AUTO_SMOOTH`, `SMOOTH`, `FLAT`, `SCALE`, `ROTATION`) | Выполняет авто‑сглаживание, переключает shading, либо «применяет» масштаб/вращение к геометрии. |

---

## 🔰 Пользовательский интерфейс

### 1. Боковая панель (N-panel)
Вкладка `QuickToolsEditMode` (название можно изменить в настройках).
* **Selection Data:** Переключатели `Edges` и `Vertices`. Определяют, на что именно будет влиять установка весов.
* **Weights:** Кнопки мгновенного назначения значений для `Crease` и `Bevel`.
* **Shade Auto Smooth**  Быстрая настройка автосглаживания по углу (работает аналогично как в режиме объекта)
* **Smooth & Transform:** Быстрые команды для шейдинга и фиксации масштаба/вращения.

### 2. Контекстное меню
Выберите меш перейдите в режим `Edit Mesh` нажмите **ПКМ** в 3D Viewport → откройте пункт **QuickToolsEditMode**.

### 3. Изменение категории вкладки Аддона на N - панели
`Edit → Preferences → Add‑ons → Quick Tools Edit Mode → раскройте настройки → поле Tab Category → введите название категории нажмите Enter`.

<div align="center">

![description](https://github.com/Constantyn6487/Tutor_readme_outsidefile/blob/main/QTEM-Settings.png)

</div>

---

## 🏗 Пример рабочего процесса
1. Зайдите в **Edit Mode** (`Tab`).
2. *Выберите ребра/вершины, которым хотите задать вес.*
3. В блоке **Selection Data** включите *Edges (или Vertices)*.
4. Нажмите кнопку веса (например, `0.50`) → мгновенно получаете одинаковый вес на всех выбранных ребрах.
5. Чтобы переключить **shading**, просто нажмите *Smooth или Flat*.
6. Если вы забыли применить **Scale/Rotation** когда были в режиме объекта, нажмите *ApplyScale/ApplyRotation* – трансформация «запишется» в вершины, а объект вернётся к *единичному масштабу/нулевому вращению*.

---

## 📦 Установка и системные требования

* **✨ Версия Blender:** 4.2.+ и выше.
* **📜 Лицензия:** GNU General Public License v3.0.

1. Скачайте архив (`.zip`) с последней версией аддона с GitHub 
2. Откройте Blender → `Edit → Preferences → Add‑Ons → Install from disk` или `Edit` > `Preferences` > `Get Extensions`  > `Install from disk`.
3. Выберите скачанный файл и нажмите Install Add‑on.
4. Поставьте галочку напротив Object: Quick Tools Edit Mode → Enable если сама не поствилась.

---

## 🔧 Разработка и вклад
Вопросы и сообщения об ошибках принимаются через раздел **Issues** в данном репозитории.
