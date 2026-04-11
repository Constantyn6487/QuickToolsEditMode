<details>
  <summary><div align="center"><h1> 🔰Нумерация версий (Versioning)🔰 🔽Click English lang.🔽</h1></div></summary>

We use a hybrid scheme `MAJOR.MINOR.PATCH+YYYYMMDD+nup` or `MAJOR.MINOR.PATCH+YYYYMMDD+up`.

#### How the parts change  

| Part | When it is incremented | Example |
|------|-----------------------|---------|
| **MAJOR** | When we break backward compatibility, a data migration is required, or the add‑on’s API changes. | `v1.0.0+20260217 → v2.0.0+20260305` |
| **MINOR** | When we add new functionality that users can ignore if they wish. | `v1.2.0+20260301 → v1.3.0+20260315` |
| **PATCH** | When we fix bugs without changing functionality. | `v1.2.3+20260310 → v1.2.4+20260312` |
| **+YYYYMMDD** | Publication date (UTC). | `v1.2.4+20260312` |
| **NUP** | “No‑Update” – a version **without** automatic‑update support. | `v1.0.0+20260217nup` |
| **UP** | “Update” – a version **with** automatic‑update support. | `v2-0-20260217up` |

#### Where it is used  

* `bl_info["version"]` in the add‑on’s source file stores only the `MAJOR.MINOR.PATCH` part.  
* The Git tag and the release title are generated as `vMAJOR.MINOR.PATCH+YYYYMMDD+nup` **or** `vMAJOR.MINOR.PATCH+YYYYMMDD+up`.  
* `CHANGELOG.md` lists the changes under these tags.  

</details>

Мы используем гибридную схему `MAJOR.MINOR.PATCH+YYYYMMDD+nup or up`.

### Как меняются части

| Часть | Когда увеличиваем | Пример |
|-------|------------------|--------|
| **MAJOR** | Нарушаем обратную совместимость, требуется миграция данных, изменяется API аддона. | `v1.0.0+20260217 → v2.0.0+20260305` |
| **MINOR** | Добавляем новые функции, которые пользователь может игнорировать. | `v1.2.0+20260301 → v1.3.0+20260315` |
| **PATCH** | Исправляем баги, не меняем функциональность. | `v1.2.3+20260310 → v1.2.4+20260312` |
| **+YYYYMMDD** | Дата публикации (UTC). | `v1.2.4+20260312` |
| **NUP** | Обозначает no update версия без функции авто обновления | `v1.0.0+20260217nup` |
| **UP** | Обозначает update версия с функцией авто обновления | `v2-0-20260217up` |

### Где используется

* `bl_info["version"]` в файле аддона хранит только `MAJOR.MINOR.PATCH`.  
* Тег в Git и заголовок релиза формируются как `vMAJOR.MINOR.PATCH+YYYYMMDD+nup or up`.  
* В `CHANGELOG.md` перечисляем изменения по этим тегам.
