# Руководство по тестированию FastAPI Shop в Postman

## Содержание
1. [Начальная настройка](#начальная-настройка)
2. [Тестирование эндпоинтов](#тестирование-эндпоинтов)
3. [Автоматические тесты](#автоматические-тесты)
4. [Переменные окружения](#переменные-окружения)

---

## Начальная настройка

### 1. Создание коллекции
1. Откройте Postman
2. Нажмите "New" → "Collection"
3. Назовите коллекцию "FastAPI Shop"
4. В описании укажите: `Base URL: http://localhost:8000`

### 2. Настройка переменных окружения
1. Нажмите "Environments" → "Create Environment"
2. Назовите окружение "FastAPI Shop Local"
3. Добавьте переменные:

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| baseUrl | http://localhost:8000 | http://localhost:8000 |
| productId | 1 | 1 |
| categoryId | 1 | 1 |

---

## Тестирование эндпоинтов

### 📌 1. Health Check & Root

#### 1.1 GET Root
- **URL:** `{{baseUrl}}/`
- **Method:** GET
- **Описание:** Проверка работоспособности API

**Ожидаемый ответ (200 OK):**
```json
{
  "message": "Welcome to FastAPI Shop",
  "docs": "/api/docs"
}
```

**Тесты (Tests tab):**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has message", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('message');
    pm.expect(jsonData.message).to.include('FastAPI Shop');
});
```

#### 1.2 GET Health Check
- **URL:** `{{baseUrl}}/health`
- **Method:** GET

**Ожидаемый ответ (200 OK):**
```json
{
  "status": "healthy"
}
```

---

### 📁 2. Categories

#### 2.1 GET All Categories
- **URL:** `{{baseUrl}}/api/categories`
- **Method:** GET
- **Описание:** Получить список всех категорий

**Ожидаемый ответ (200 OK):**
```json
[
  {
    "name": "Electronics",
    "slug": "electronics",
    "id": 1
  },
  {
    "name": "Clothing",
    "slug": "clothing",
    "id": 2
  }
]
```

**Тесты:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response is array", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('array');
});

pm.test("Categories have required fields", function () {
    var jsonData = pm.response.json();
    if (jsonData.length > 0) {
        pm.expect(jsonData[0]).to.have.property('id');
        pm.expect(jsonData[0]).to.have.property('name');
        pm.expect(jsonData[0]).to.have.property('slug');
        
        // Сохраняем первый categoryId для других тестов
        pm.environment.set("categoryId", jsonData[0].id);
    }
});
```

#### 2.2 GET Category by ID
- **URL:** `{{baseUrl}}/api/categories/{{categoryId}}`
- **Method:** GET
- **Описание:** Получить категорию по ID

**Ожидаемый ответ (200 OK):**
```json
{
  "name": "Electronics",
  "slug": "electronics",
  "id": 1
}
```

**Тесты:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Category has correct structure", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
    pm.expect(jsonData).to.have.property('name');
    pm.expect(jsonData).to.have.property('slug');
    pm.expect(jsonData.id).to.eql(parseInt(pm.environment.get("categoryId")));
});
```

#### 2.3 GET Category by Invalid ID (Error Case)
- **URL:** `{{baseUrl}}/api/categories/9999`
- **Method:** GET

**Ожидаемый ответ (404 Not Found):**
```json
{
  "detail": "Category with id 9999 not found"
}
```

**Тесты:**
```javascript
pm.test("Status code is 404", function () {
    pm.response.to.have.status(404);
});

pm.test("Error message is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.detail).to.include("not found");
});
```

---

### 📦 3. Products

#### 3.1 GET All Products
- **URL:** `{{baseUrl}}/api/products`
- **Method:** GET
- **Описание:** Получить список всех товаров

**Ожидаемый ответ (200 OK):**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Wireless Headphones",
      "description": "High-quality wireless headphones...",
      "price": 299.99,
      "category_id": 1,
      "image_url": "https://images.unsplash.com/...",
      "created_at": "2024-01-17T10:30:00",
      "category": {
        "name": "Electronics",
        "slug": "electronics",
        "id": 1
      }
    }
  ],
  "total": 13
}
```

**Тесты:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has products array and total", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('products');
    pm.expect(jsonData).to.have.property('total');
    pm.expect(jsonData.products).to.be.an('array');
});

pm.test("Products have correct structure", function () {
    var jsonData = pm.response.json();
    if (jsonData.products.length > 0) {
        var product = jsonData.products[0];
        pm.expect(product).to.have.property('id');
        pm.expect(product).to.have.property('name');
        pm.expect(product).to.have.property('price');
        pm.expect(product).to.have.property('category');
        pm.expect(product.category).to.have.property('name');
        
        // Сохраняем productId для других тестов
        pm.environment.set("productId", product.id);
    }
});

pm.test("Total matches products count", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.total).to.eql(jsonData.products.length);
});
```

#### 3.2 GET Product by ID
- **URL:** `{{baseUrl}}/api/products/{{productId}}`
- **Method:** GET

**Ожидаемый ответ (200 OK):**
```json
{
  "id": 1,
  "name": "Wireless Headphones",
  "description": "High-quality wireless headphones...",
  "price": 299.99,
  "category_id": 1,
  "image_url": "https://images.unsplash.com/...",
  "created_at": "2024-01-17T10:30:00",
  "category": {
    "name": "Electronics",
    "slug": "electronics",
    "id": 1
  }
}
```

**Тесты:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Product has correct ID", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.id).to.eql(parseInt(pm.environment.get("productId")));
});

pm.test("Product has category details", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('category');
    pm.expect(jsonData.category).to.have.property('id');
    pm.expect(jsonData.category).to.have.property('name');
});
```

#### 3.3 GET Products by Category
- **URL:** `{{baseUrl}}/api/products/category/{{categoryId}}`
- **Method:** GET

**Ожидаемый ответ (200 OK):**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Wireless Headphones",
      "category_id": 1,
      ...
    }
  ],
  "total": 5
}
```

**Тесты:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("All products belong to the category", function () {
    var jsonData = pm.response.json();
    var categoryId = parseInt(pm.environment.get("categoryId"));
    
    jsonData.products.forEach(function(product) {
        pm.expect(product.category_id).to.eql(categoryId);
    });
});
```

---

### 🛒 4. Cart

#### 4.1 POST Add to Cart
- **URL:** `{{baseUrl}}/api/cart/add`
- **Method:** POST
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "product_id": 1,
  "quantity": 2,
  "cart": {}
}
```

**Ожидаемый ответ (200 OK):**
```json
{
  "cart": {
    "1": 2
  }
}
```

**Тесты:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Cart updated successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('cart');
    pm.expect(jsonData.cart).to.have.property('1');
    pm.expect(jsonData.cart['1']).to.eql(2);
});

// Сохраняем корзину для следующих тестов
pm.environment.set("currentCart", JSON.stringify(pm.response.json().cart));
```

#### 4.2 POST Add More Quantity to Existing Item
- **URL:** `{{baseUrl}}/api/cart/add`
- **Method:** POST
- **Body:**
```json
{
  "product_id": 1,
  "quantity": 3,
  "cart": {"1": 2}
}
```

**Ожидаемый ответ (200 OK):**
```json
{
  "cart": {
    "1": 5
  }
}
```

**Тесты:**
```javascript
pm.test("Quantity increased correctly", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.cart['1']).to.eql(5);
});
```

#### 4.3 POST Get Cart Details
- **URL:** `{{baseUrl}}/api/cart`
- **Method:** POST
- **Body:**
```json
{
  "1": 2,
  "2": 1
}
```

**Ожидаемый ответ (200 OK):**
```json
{
  "items": [
    {
      "product_id": 1,
      "name": "Wireless Headphones",
      "price": 299.99,
      "quantity": 2,
      "subtotal": 599.98,
      "image_url": "https://images.unsplash.com/..."
    }
  ],
  "total": 599.98,
  "items_count": 2
}
```

**Тесты:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Cart details have correct structure", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('items');
    pm.expect(jsonData).to.have.property('total');
    pm.expect(jsonData).to.have.property('items_count');
});

pm.test("Cart calculations are correct", function () {
    var jsonData = pm.response.json();
    var calculatedTotal = 0;
    var calculatedCount = 0;
    
    jsonData.items.forEach(function(item) {
        pm.expect(item.subtotal).to.eql(item.price * item.quantity);
        calculatedTotal += item.subtotal;
        calculatedCount += item.quantity;
    });
    
    pm.expect(Math.round(jsonData.total)).to.eql(Math.round(calculatedTotal));
    pm.expect(jsonData.items_count).to.eql(calculatedCount);
});
```

#### 4.4 PUT Update Cart Item
- **URL:** `{{baseUrl}}/api/cart/update`
- **Method:** PUT
- **Body:**
```json
{
  "product_id": 1,
  "quantity": 5,
  "cart": {"1": 2}
}
```

**Ожидаемый ответ (200 OK):**
```json
{
  "cart": {
    "1": 5
  }
}
```

**Тесты:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Quantity updated correctly", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.cart['1']).to.eql(5);
});
```

#### 4.5 DELETE Remove from Cart
- **URL:** `{{baseUrl}}/api/cart/remove/1`
- **Method:** DELETE
- **Body:**
```json
{
  "cart": {"1": 2, "2": 3}
}
```

**Ожидаемый ответ (200 OK):**
```json
{
  "cart": {
    "2": 3
  }
}
```

**Тесты:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Product removed from cart", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.cart).to.not.have.property('1');
    pm.expect(jsonData.cart).to.have.property('2');
});
```

#### 4.6 POST Empty Cart
- **URL:** `{{baseUrl}}/api/cart`
- **Method:** POST
- **Body:**
```json
{}
```

**Ожидаемый ответ (200 OK):**
```json
{
  "items": [],
  "total": 0.0,
  "items_count": 0
}
```

---

## Автоматические тесты

### Создание Test Suite

Вы можете создать папки в коллекции для организации тестов:

```
FastAPI Shop
├── 1. Health & Root
│   ├── GET Root
│   └── GET Health
├── 2. Categories
│   ├── GET All Categories
│   ├── GET Category by ID
│   └── GET Invalid Category (404)
├── 3. Products
│   ├── GET All Products
│   ├── GET Product by ID
│   └── GET Products by Category
└── 4. Cart
    ├── POST Add to Cart
    ├── POST Get Cart Details
    ├── PUT Update Cart
    └── DELETE Remove from Cart
```

### Запуск Collection Runner

1. Нажмите на коллекцию "FastAPI Shop"
2. Нажмите "Run"
3. Выберите все запросы или конкретные папки
4. Нажмите "Run FastAPI Shop"
5. Просмотрите результаты тестов

---

## Сценарии тестирования

### Сценарий 1: Полный цикл покупки

Последовательность запросов:
1. `GET /api/categories` - просмотр категорий
2. `GET /api/products/category/1` - выбор товаров из категории
3. `POST /api/cart/add` - добавление первого товара
4. `POST /api/cart/add` - добавление второго товара
5. `POST /api/cart` - просмотр корзины
6. `PUT /api/cart/update` - изменение количества
7. `POST /api/cart` - финальная проверка корзины

### Сценарий 2: Обработка ошибок

1. `GET /api/products/9999` - несуществующий товар (404)
2. `GET /api/categories/9999` - несуществующая категория (404)
3. `POST /api/cart/add` с product_id=9999 - добавление несуществующего товара
4. `PUT /api/cart/update` для товара не в корзине (404)

---

## Экспорт/Импорт коллекции

### Экспорт
1. Нажмите на коллекцию
2. Три точки → "Export"
3. Выберите "Collection v2.1"
4. Сохраните JSON файл

### Импорт
1. File → Import
2. Выберите сохраненный JSON файл
3. Импортируйте окружение отдельно

---

## Дополнительные советы

1. **Используйте Pre-request Scripts** для автоматической настройки данных
2. **Создайте Mock Server** для тестирования без запущенного backend
3. **Интегрируйте с Newman** для CI/CD pipeline
4. **Используйте Postman Monitors** для регулярной проверки API

### Пример Pre-request Script для генерации случайных данных:
```javascript
pm.environment.set("randomProductId", Math.floor(Math.random() * 10) + 1);
pm.environment.set("randomQuantity", Math.floor(Math.random() * 5) + 1);
```

---

## Ожидаемые коды ответов

| Endpoint | Method | Success | Error |
|----------|--------|---------|-------|
| `/` | GET | 200 | - |
| `/health` | GET | 200 | - |
| `/api/categories` | GET | 200 | - |
| `/api/categories/{id}` | GET | 200 | 404 |
| `/api/products` | GET | 200 | - |
| `/api/products/{id}` | GET | 200 | 404 |
| `/api/products/category/{id}` | GET | 200 | 404 |
| `/api/cart/add` | POST | 200 | 404 |
| `/api/cart` | POST | 200 | - |
| `/api/cart/update` | PUT | 200 | 404 |
| `/api/cart/remove/{id}` | DELETE | 200 | 404 |

---

**Готово!** Теперь у вас есть полное руководство по тестированию вашего API в Postman.