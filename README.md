# fastapi_sqlalchemy<h1>Асинхронный Backend на FastAPI для биржи труда</h1>
<hr>
<p>Идейным вдохновителем стал видеоурок: <a href="https://www.youtube.com/watch?v=PVebRy0_K0s">https://www.youtube.com/watch?v=PVebRy0_K0s</a></p>
<p><br></p>
<h2>Краткое описание</h2>
<p>Сервис занимающийся регистрацией пользователей, их изменением. А также &nbsp;созданием вакансий, их редактирование и удаление.&nbsp;</p>
<h2>Особенности</h2>
<ul>
    <li>БД - PostgreSQL</li>
    <li>engine - asyncpg</li>
    <li>ОРМ - SqlAlchemy</li>
    <li>Secuirity - JWT</li>
</ul>
<h2>Использование</h2>
<p><code>python3 -m pytest</code> - запуск тестов</p>
<p><code>python3 main.py</code> - запуск сервиса</p>
<p>Установите настройки в core/config.py либо создайте .env файл</p>
<p><br></p>
