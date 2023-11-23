**Цель практической работы**

Освоить функционал Sentry, применить навыки по работе с Prometheus и Grafana

**Что входит в работу**

- Развернуть локально Sentry и настроить интеграцию с репозиторием Gitlab
- Добавить собственные метрики Prometheus и построить dashboard в Grafana

**Задание 1. Sentry**

1. Развернуть Sentry локально
2. Настроить систему оповещений на почту
3. Настроить интеграцию с Gitlab/Github

**Советы и рекомендации**

[Local sentry](https://develop.sentry.dev/self-hosted/)

[Alerts](https://docs.sentry.io/product/alerts/) 

[Git integrations](https://docs.sentry.io/product/integrations/source-code-mgmt/)

**Что оценивается**

Оценивается умение работы с Sentry, развертывание локально, с помощью docker, настройка оповещений об ошибках и интеграция с системой контроля версий


**Задание 2. Prometheus + Grafana**

1. Развернуть Prometheus, Flask app, Grafana с помощью docker
2. Во flask-приложение необходимо создать эндпоинт (контекст не важен) и подключить пакет prometheus_flask_exporter
3. На эндпоинт необходимо добавить декоратор метрики @metrics.counter(), которая будет хранить счетчик запросов с кодом ответа 200
4. Построить график в Grafana, используя метрику из п.3


**Советы и рекомендации**

[Настройка конфигурации Grafana](https://grafana.com/docs/grafana/latest/administration/configuration/)
 
[Подключение Grafana к Prometheus](https://grafana.com/docs/grafana/latest/datasources/prometheus/)

**Что оценивается**

Оценивается умение работать с Prometheus и Grafana: развертывание инструментов локально, создание метрики, визуализация метрики на дашборде в Grafana

**Как отправить задание на проверку**

Выполните домашнее задание в GitLab, в форме ниже напишите «Сделано» и нажмите кнопку «Отправить».


