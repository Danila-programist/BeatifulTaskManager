### Фронтенд

Документация по папкам, файлам и функциональности проекта: \

Папки и файлы: 
- `src` - папка с приложением на React
- `Dockefile` - докер-файл для создания контейнера фронтенда
- `eslint.config.js` - линтер JavaScript
- `index.html` - единственная страничка html для подключения React
- `package-lock.json` - зависимости для React
- `package.json` - зависимости для React
- `tailwind.config.js` - настройки Tailwind
- `vite.config.js` - настройки сборщика проекта Vite

Пройдемся по внутренним пакетам приложения `src`:

- `api` - взаимодействие с API бэкенда с помощью axios
- `components` - компоненты для развертывания их на pages
- `pages` - страницы приложения 
- `routes` - навигация по страницам
- `App.jsx` - основное приложение React
- `index.css` - стили App.jsx
- `main.jsx` - интеграция к index.html страничке


### Схематичное представление реализации фронтенда

![alt text](/frontend/img/image.png)