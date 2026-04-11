<details>
  <summary>🔽 Click to see the English translation. 🔽</summary>

<div align="center"><h1> 🛠 Quick Tools Edit Mode (2.1) 🛠 </h1>

![description](https://github.com/Constantyn6487/link/blob/main/preview%202.1%20eng.png?raw=true) 

</div>

**Quick Tools Edit Mode** is a compact toolbox for Blender that removes unnecessary clicks and pop‑up dialogs. All essential operations for weights, shading, and transforms are now reachable with a single click from the side panel or the context menu.

> **⚠️ [!IMPORTANT]**

> ***The addon works **exclusively in Edit Mode**. In Object Mode all UI elements are automatically hidden to keep the interface clean.***

## 🚀 Core Features

<div align="center">

| **Group** | **Functions** |
| :--------- | :---------- |
| **Selection Data**| Switches **Edges** и **Vertices**. They determine which elements of the mesh (edges/vertices) actions are applied to.|
| **Edge Crease** | Set crease weight (0.00 / 0.50 / 1.00) |
| **Edge Bevel Weight** | Set bevel weight (0.00 / 0.50 / 1.00) |
| **Shade Auto Smooth** | Quick auto‑smooth setup (compatible with Blender 4.2+) |
| **Shade Smooth / Flat** | Instantly switch shading type while staying in Edit Mode |
| **Apply Scale/Rotation** | Apply scale or rotation to geometry without leaving Edit Mode |

</div>

---

### 💡 Brief reference for each operator  

<div align="center">

| Operator | ID | Parameters | What it does |
|----------|----|------------|--------------|
| **QuickToolsSettings** | `scene.quick_tools_settings` | `affect_edges` (bool, default: True), `affect_vertices` (bool, default: False) | Settings that determine which elements of the mesh (edges/vertices) actions are applied to. |
| **BUTTON_OT_WeightSet** | `button.weight_set` | `value` (float), `mode` (`CREASE`/`BEVEL`) | Assigns crease‑weight or bevel‑weight to the selected elements. |
| **BUTTON_OT_QuickAction** | `button.quick_action` | `action` (`AUTO_SMOOTH`, `SMOOTH`, `FLAT`, `SCALE`, `ROTATION`) | Performs auto‑smooth, toggles shading, or “applies” scale/rotation to the mesh geometry. |

</div>

---
## 🔄 Support for multiple versions of Blender (Cross-version API)
The project implements a dynamic import system that ensures stable operation of the addon in both Blender 3.6 LTS and 4.0+ versions.

## 🔰 User Interface

### 1. Sidebar (N‑panel)
Tab `QuickToolsEditMode` (the name can be changed in the add‑on settings).

- **Selection Data:** Toggles `Edges` and `Vertices`. They determine which mesh elements (edges/vertices) the actions affect.  
- **Weights:** Buttons for instantly assigning values for `Crease` and `Bevel`.  
- **Shade Auto Smooth:** Quick auto‑smooth setting based on angle (works the same as in Object mode).  
- **Smooth & Transform:** Quick commands for shading and applying scale/rotation.

### 2. Context menu
Select a mesh, go to `Edit Mesh` mode, right‑click (**RMB**) in the 3D Viewport → open the **QuickToolsEditMode** entry.

- **Weights:** Buttons for instantly assigning values for `Crease` and `Bevel`.  
- **Shade Auto Smooth:** Quick auto‑smooth setting based on angle (works the same as in Object mode).  
- **Smooth & Transform:** Quick commands for shading and applying scale/rotation.

### 3. Blender Preferences Panel
1. *Changing the Add-on Tab Category on the N-panel*
	`Edit → Preferences → Add-ons → Quick Tools Edit Mode → expand settings → Tab Category field → enter category name and press Enter`.
2. *Supporting the Project*
	`Here you can financially support the developer` → *Support project on Boosty* → via the **Boosty** link.
3. *Using the Auto-Update Function*
	`Edit → Preferences → Add-ons → Quick Tools Edit Mode → expand settings → Updater settings → check the Auto-check box and select the check interval (Month and Day).`
	`You can also check for updates manually by clicking` → `Check now for update` → `select version to install` → `then restart Blender`.


<div align="center">

![description](https://github.com/Constantyn6487/link/blob/main/QTEM-Settings.png?raw=true)

</div>

---

## 🏗 Workflow Example
1. Enter **Edit Mode** (`Tab`).  
2. *Select the edges/vertices you want to assign weight to.*  
3. In the **Selection Data** panel, enable *Edges* (or *Vertices*).  
4. Click a weight button (e.g., `0.50`) → the same weight is instantly applied to all selected edges.  
5. To change **shading**, just click *Smooth* or *Flat*.  
6. If you forgot to apply **Scale/Rotation** while in Object mode, click *Apply Scale/Rotation* – the transformation is baked into the vertices and the object returns to *unit scale / zero rotation*.  
7. Example where the `Edges` and `Vertices` toggles are useful:

   🔧 **Example 1:** Precise `crease/bevel` control when refining a shape  
   You are working on an organic model (e.g., a character’s head) that already has a Subdivision Surface. You need to add a crease only on specific eye‑socket edges to keep sharp borders, but some vertices on the face surface are also accidentally selected.

   🔹**How the settings help:**  
   * Enable `edges`.  
   * Now when you press the `crease weight` button (e.g., 1.0)`, only the edges receive the value.  
   * Vertices are ignored – you won’t accidentally change their parameters.  

   ✅ **This prevents unwanted artifacts and gives precise control over which elements you modify.**

   🔧 **Example 2:** Working with vertex groups or shape‑key vertices  
   You are creating a deformation mechanic (e.g., an arm bend) where not only edges but also the positions of specific vertices matter. You want to set bevel weight on certain vertices to later use them in Geometry Nodes or to drive modifiers.

   🔹**How the settings help:**  
   * Disable `affect_edges` (set to **False**) and enable `affect_vertices` (set to **True**).  
   * Now when you use the tool, only vertices will be changed, even if edges are also selected.  

   ✅ **Thus you can precisely control where smoothing or deformation occurs, especially in complex setups.**

   🎯 **Summary:**  

   - The check‑boxes **affect_edges** and **affect_vertices** let you:  
     * Separate the influence areas of the tools.  
     * Avoid accidental changes to unselected elements.  
     * Speed up the workflow when modeling precisely.  

   - This is especially valuable when:  
     * Working with Subdivision Surface and creases.  
     * Using Geometry Nodes.  
     * Building complex setups with vertex data.

---

## 📦 Installation and System Requirements

* **✨ Blender version:** 3.6 or newer*

1. Download the `.zip` archive of the latest add‑on version from GitHub.  
2. Open Blender → `Edit → Preferences → Add‑ons → Install from Disk` (or `Edit` > `Preferences` > `Add‑ons` > `Install from Disk`).  
3. Select the downloaded file and click **Install Add‑on**.  
4. Tick the checkbox next to **Object: Quick Tools Edit Mode** → **Enable** if it was not automatically enabled.

---

## 🔧 Development and Contribution

**📜 License:** GNU General Public License v3.0.  

* 🐱‍💻 Questions and bug reports are welcome via the **Issues** section of this repository.*  
* 💰 If you like the add‑on and would like to support the developer financially, you can do so on [Boosty](https://boosty.to/constantiniy6487/single-payment/donation/791948/target?share=target_link).*

 

---  

</details>


<div align="center"><h1> 🛠 Quick Tools Edit Mode (2.1) 🛠 </h1>

![description](https://github.com/Constantyn6487/link/blob/main/preview%202.1%20rus.png?raw=true)
</div>

**Quick Tools Edit Mode** — это компактный набор инструментов для Blender, который избавляет от лишних кликов и всплывающих окон. Все ключевые операции по весам (weights), затенению (shading) и трансформациям теперь доступны в один клик прямо из боковой панели или контекстного меню.

> [!IMPORTANT]
> Аддон работает **исключительно в Edit Mode**. В объектном режиме элементы управления автоматически скрываются, чтобы не загромождать интерфейс.

## 🚀 Основные функции

<div align="center"> 

| **Группа** | **функций** |
| :--------- | :---------- |
| **Selection Data**| Переключатели **Edges** и **Vertices**. Определяют, к каким элементам меша (рёбра/вершины) применяются действия.|
| **Edge Crease** | Установка веса сгиба (0.00 / 0.50 / 1.00) |
| **Edge Bevel Weight** | Установка веса фаски (0.00 / 0.50 / 1.00) | 
| **Shade Auto Smooth** | Быстрая настройка автосглаживания (совместимо с Blender 4.2+) |
| **Shade Smooth / Flat** | Мгновенное переключение типа затенения из Edit Mode |
| **Apply Scale/Rotation** | Применение трансформаций к геометрии, не выходя из Edit Mode |

</div>

---

### 💡 Краткая справка по каждому оператору  

| Оператор | ID | Параметры | Что делает |
|----------|----|-----------|------------|
| **QuickToolsSettings** | `scene.quick_tools_settings` | `affect_edges` (bool, default: True), `affect_vertices` (bool, default: False) | Настройки, определяющие, к каким элементам меша (рёбра/вершины) применяются действия. |
| **BUTTON_OT_WeightSet** | `button.weight_set` | `value` (float), `mode` (`CREASE`/`BEVEL`) | Устанавливает crease‑weight или bevel‑weight выбранным элементам. |
| **BUTTON_OT_QuickAction** | `button.quick_action` | `action` (`AUTO_SMOOTH`, `SMOOTH`, `FLAT`, `SCALE`, `ROTATION`) | Выполняет авто‑сглаживание, переключает shading, либо «применяет» масштаб/вращение к геометрии. |

---
### 🔄 Поддержка нескольких версий Blender (Cross-version API)
В проекте реализована система динамического импорта, которая обеспечивает стабильную работу аддона как в Blender 3.6 LTS, так и в версиях 4.0+.

## 🔰 Пользовательский интерфейс

### 1. Боковая панель (N-panel)
Вкладка `QuickToolsEditMode` (название можно изменить в настройках).
* **Selection Data:** Переключатели `Edges` и `Vertices`. Определяют, к каким элементам меша (рёбра/вершины) применяются действия.
* **Weights:** Кнопки мгновенного назначения значений для `Crease` и `Bevel`.
* **Shade Auto Smooth**  Быстрая настройка автосглаживания по углу (работает аналогично как в режиме объекта)
* **Smooth & Transform:** Быстрые команды для шейдинга и фиксации масштаба/вращения.

### 2. Контекстное меню
Выберите меш перейдите в режим `Edit Mesh` нажмите **ПКМ** в 3D Viewport → откройте пункт **QuickToolsEditMode**.
* **Weights:** Кнопки мгновенного назначения значений для `Crease` и `Bevel`.
* **Shade Auto Smooth**  Быстрая настройка автосглаживания по углу (работает аналогично как в режиме объекта)
* **Smooth & Transform:** Быстрые команды для шейдинга и фиксации масштаба/вращения.

### 3. Панель настроек Blender Preferences
1. *Изменение категории вкладки Аддона на N - панели*
	`Edit → Preferences → Add‑ons → Quick Tools Edit Mode → раскройте настройки → поле Tab Category → введите название категории нажмите Enter`.
2. *Поддержка проекта*
	`Тут вы можете поддержать разработчика финансово` → *Support project on Boosty* → ссылка ведет на **boosty**.
3. *Использование функции автообновления*
	`Edit → Preferences → Add‑ons → Quick Tools Edit Mode → раскройте настройки → Updater settings → поставте галочку Auto-check и выберите интервал проверки день и месяц.`
	`А также можете проверить наличие обновлений нажав на кнопку` → `Check now for update` → `выбрать версию для установки` → `а затем перезагрузите Blender`.

<div align="center">

![description](https://github.com/Constantyn6487/link/blob/main/QTEM-Settings.png?raw)

</div>

---

## 🏗 Пример рабочего процесса
1. Зайдите в **Edit Mode** (`Tab`).
2. *Выберите ребра/вершины, которым хотите задать вес.*
3. В блоке **Selection Data** включите *Edges (или Vertices)*.
4. Нажмите кнопку веса (например, `0.50`) → мгновенно получаете одинаковый вес на всех выбранных ребрах.
5. Чтобы переключить **shading**, просто нажмите *Smooth или Flat*.
6. Если вы забыли применить **Scale/Rotation** когда были в режиме объекта, нажмите *ApplyScale/ApplyRotation* – трансформация «запишется» в вершины, а объект вернётся к *единичному масштабу/нулевому вращению*.
7. Пример где могут понадобится Переключатели `Edges` и `Vertices`:

	🔧 **Пример** 1: Точный контроль `crease/bevel` при доработке формы
	Вы работаете над органической моделью (например, голова персонажа), где уже есть *Subdivision Surface*. Вам нужно добавить crease только на определённые рёбра глазницы, чтобы сохранить чёткие границы, но случайно выделены также некоторые вершины на поверхности лица.

	🔹 Как помогают настройки:
	* Вы включаете `edges`.
	* Теперь при нажатии кнопки установки `crease/bevel (например, 1.0)`, только рёбра получат значение.
	* `Вершины игнорируются` — вы случайно не изменяете их параметры.
	
	✅ **Это предотвращает нежелательные артефакты и даёт точный контроль над тем, какие элементы вы хотите изменить.**
	
	🔧 **Пример** 2: Работа с вершинными группами или `shape key` вершинами
	Вы создаёте механику деформации (например, сгиб руки), где важны не только рёбра, но и положение конкретных вершин. Вы хотите установить bevel weight на некоторых вершинах, чтобы потом использовать их в Geometry Nodes или для управления поведением модификаторов.

	🔹 Как помогают настройки:
	* Выключите `vertices`.
	* Теперь при использовании инструмента будут изменены только вершины, даже если выделены и рёбра.
	
	✅ **Так вы можете точно контролировать, где именно будет происходить сглаживание или деформация, особенно в сложных сетапах.**
	
	🎯 Вывод:
	- Кнопки *edges* и *vertices* позволяют вам:
	 * Разделять области влияния инструментов.
	 * Избегать случайных изменений на невыбранных элементах.
	 * Ускорить рабочий процесс при точном моделировании.
	
	- Это особенно ценно при:
	 * Работе с Subsurf и crease.
	 * Использовании Geometry Nodes.
	 * Создании сложных сетапов с вершинными данными.
---

## 📦 Установка и системные требования

* **✨ Версия Blender:** 3.6 и выше*

1. Скачайте архив (`.zip`) с последней версией аддона с GitHub 
2. Откройте Blender → `Edit → Preferences → Add‑Ons → Install from disk` или `Edit` > `Preferences` > `Add‑Ons`  > `Install from disk`.
3. Выберите скачанный файл и нажмите **Install Add‑on**.
4. Поставьте галочку напротив **Object: Quick Tools Edit Mode** → **Enable** если сама не поставилась.

---

## 🔧 Разработка и вклад
**📜 Лицензия:** GNU General Public License v3.0.

* 🐱‍💻 Вопросы и сообщения об ошибках принимаются через раздел **Issues** в данном репозитории.*
* 💰 Если вам понравился Аддон и у вас появилось желание поддержать разработчика денюшкой, то это можно сделать на [boosty](https://boosty.to/constantiniy6487/single-payment/donation/791948/target?share=target_link). *
