export const dashboardStats = [
  { label: 'Всего пользователей', value: '1,247', tone: 'blue', icon: 'user' },
  { label: 'Активных скидок', value: '33', tone: 'purple', icon: 'cube' },
  { label: 'Заявок компаний', value: '2', tone: 'orange', icon: 'doc' },
  { label: 'Партнерских компаний', value: '12', tone: 'green', icon: 'building' },
]

export const recentActivity = [
  { tone: 'orange', text: 'KFC отправила заявку на партнёрство', time: '15 мин назад' },
  { tone: 'blue', text: 'Иванов И.И. назначен менеджером Burger King', time: '1 ч назад' },
  { tone: 'green', text: 'Заявка Яндекс.Плюс одобрена', time: '2 ч назад' },
  { tone: 'blue', text: 'Spotify Premium создал новую скидку', time: '3 ч назад' },
]

export const pendingSidebar = [
  {
    company: 'KFC',
    contact: 'Иванова Мария',
    offer: '15% скидка на комбо-наборы для студентов по промокоду.',
    date: '2025-03-28',
  },
  {
    company: 'Wildberries',
    contact: 'Смирнова Екатерина',
    offer: 'Промокод на 500 ₽ для первого заказа со студенческой почтой.',
    date: '2025-03-27',
  },
]

export const topCompanies = [
  { company: 'Яндекс.Плюс', clicks: '2 340', unique: '1 890', ctr: '80.8%' },
  { company: 'Кинопоиск', clicks: '1 890', unique: '1 450', ctr: '76.7%' },
  { company: 'Spotify', clicks: '1 567', unique: '1 234', ctr: '78.7%' },
  { company: 'Burger King', clicks: '1 250', unique: '890', ctr: '71.2%' },
  { company: 'Okko', clicks: '1 234', unique: '980', ctr: '79.4%' },
]

export const quickNav = [
  { title: 'Заявки компаний', desc: 'Новые заявки', to: '/admin/applications', tone: 'purple' },
  { title: 'Менеджеры', desc: 'Команда', to: '/admin/managers', tone: 'blue' },
  { title: 'Статистика', desc: 'Аналитика', to: '/admin/statistics', tone: 'green' },
  { title: 'Категории', desc: 'Управление', to: '/catalog', tone: 'orange' },
]

export const applications = [
  {
    id: '1',
    company: 'KFC',
    status: 'pending',
    contact: 'Иванова Мария',
    position: 'Менеджер по маркетингу',
    email: 'maria@kfc.ru',
    phone: '+7 (499) 123-45-67',
    offer: '15% скидка на комбо-наборы для студентов при предъявлении студенческого.',
    submitted: '2025-03-28',
  },
  {
    id: '2',
    company: 'Яндекс.Плюс',
    status: 'approved',
    contact: 'Петров Алексей',
    position: 'Руководитель B2B',
    email: 'partner@yandex.ru',
    phone: '+7 (495) 000-11-22',
    offer: '3 месяца подписки по цене 1 месяца для студентов.',
    submitted: '2025-03-25',
    resolved: '2025-03-26',
  },
  {
    id: '3',
    company: 'Test Company',
    status: 'rejected',
    contact: 'Тестов Тест',
    position: 'Директор',
    email: 'test@example.com',
    phone: '+7 (900) 000-00-00',
    offer: 'Некорректное предложение.',
    submitted: '2025-03-20',
    resolved: '2025-03-21',
    reason: 'Не соответствует требованиям платформы',
  },
]

export const managers = [
  {
    id: 'm1',
    name: 'Иванов Иван Иванович',
    email: 'ivanov@studentpass.ru',
    phone: '+7 (916) 111-22-33',
    assigned: '2025-01-15',
    companies: [
      { name: 'Burger King', discounts: 4, clicks: 1250 },
      { name: 'Starbucks', discounts: 2, clicks: 890 },
    ],
  },
  {
    id: 'm2',
    name: 'Петрова Мария Сергеевна',
    email: 'petrova@studentpass.ru',
    phone: '+7 (917) 222-33-44',
    assigned: '2025-02-01',
    companies: [
      { name: 'Яндекс.Плюс', discounts: 6, clicks: 2340 },
      { name: 'Spotify', discounts: 3, clicks: 1567 },
    ],
  },
  {
    id: 'm3',
    name: 'Сидоров Алексей Петрович',
    email: 'sidorov@studentpass.ru',
    phone: '+7 (918) 333-44-55',
    assigned: '2024-11-20',
    companies: [{ name: 'World Class', discounts: 2, clicks: 456 }],
  },
]

export const partnerCompaniesTable = [
  {
    company: 'Burger King',
    email: 'partner@burgerking.ru',
    manager: 'Иванов И.И.',
    discounts: 4,
    clicks: 1250,
  },
  {
    company: 'Яндекс.Плюс',
    email: 'partner@yandex.ru',
    manager: 'Петрова М.С.',
    discounts: 6,
    clicks: 2340,
  },
  {
    company: 'Spotify',
    email: 'ru@spotify.com',
    manager: 'Петрова М.С.',
    discounts: 3,
    clicks: 1567,
  },
  {
    company: 'World Class',
    email: 'b2b@worldclass.ru',
    manager: 'Сидоров А.П.',
    discounts: 2,
    clicks: 456,
  },
]

export const statisticsSummary = [
  { label: 'Всего кликов', value: '10 407', tone: 'purple', icon: 'eye' },
  { label: 'Уникальных пользователей', value: '8 014', tone: 'green', icon: 'graph' },
  { label: 'Средний CTR', value: '77.0%', tone: 'blue', icon: 'chart' },
]

export const statisticsTable = [
  { company: 'Яндекс.Плюс', clicks: '2 340', unique: '1 890', ctr: '80.8%', period: '2025-03' },
  { company: 'Кинопоиск', clicks: '1 890', unique: '1 450', ctr: '76.7%', period: '2025-03' },
  { company: 'Spotify', clicks: '1 567', unique: '1 234', ctr: '78.7%', period: '2025-03' },
  { company: 'Burger King', clicks: '1 250', unique: '890', ctr: '71.2%', period: '2025-03' },
  { company: 'Okko', clicks: '1 234', unique: '980', ctr: '79.4%', period: '2025-03' },
  { company: 'Starbucks', clicks: '890', unique: '670', ctr: '75.3%', period: '2025-03' },
  { company: 'Subway', clicks: '780', unique: '560', ctr: '71.8%', period: '2025-03' },
  { company: 'World Class', clicks: '456', unique: '340', ctr: '74.6%', period: '2025-03' },
]
