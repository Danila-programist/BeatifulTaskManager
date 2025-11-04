import { useEffect, useState } from "react";
import { Card, Row, Col, Spin, message } from "antd";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { getUserAnalytics } from "../api/analytics.js"; // ✅ импорт функции

export default function UserProfile() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserAnalytics = async () => {
      try {
        const response = await getUserAnalytics();
        setData(response.data);
      } catch (error) {
        console.error("Ошибка при загрузке аналитики:", error);
        message.error("Не удалось загрузить информацию о пользователе");
      } finally {
        setLoading(false);
      }
    };

    fetchUserAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spin size="large" />
      </div>
    );
  }

  if (!data) {
    return <div className="text-center text-grayish">Нет данных для отображения</div>;
  }

  const { user_info, tasks_overview, productivity_metrics, recent_activity, tasks_created_by_weekday } = data;
  const chartData = Object.entries(tasks_created_by_weekday || {}).map(([day, count]) => ({
    day: day.charAt(0).toUpperCase() + day.slice(1),
    count,
  }));

  return (
    <div className="p-4">
      <Row gutter={[16, 16]}>
        <Col xs={24} md={12}>
          <Card title="Профиль пользователя" bordered={false}>
            <p><strong>Имя пользователя:</strong> {user_info.username}</p>
            <p><strong>Email:</strong> {user_info.email}</p>
            <p><strong>Имя:</strong> {user_info.first_name}</p>
            <p><strong>Фамилия:</strong> {user_info.last_name}</p>
          </Card>
        </Col>

        <Col xs={24} md={12}>
          <Card title="Обзор задач" bordered={false}>
            <p><strong>Всего задач:</strong> {tasks_overview.total_tasks}</p>
            <p><strong>Активных:</strong> {tasks_overview.active_tasks}</p>
            <p><strong>Выполнено:</strong> {tasks_overview.completed_tasks}</p>
            <p><strong>Процент выполнения:</strong> {tasks_overview.completion_rate}%</p>
          </Card>
        </Col>

        <Col xs={24} md={12}>
          <Card title="Продуктивность" bordered={false}>
            <p><strong>Создано сегодня:</strong> {productivity_metrics.tasks_created_today}</p>
            <p><strong>Выполнено сегодня:</strong> {productivity_metrics.tasks_completed_today}</p>
            <p><strong>Создано за неделю:</strong> {productivity_metrics.tasks_created_this_week}</p>
            <p><strong>Выполнено за неделю:</strong> {productivity_metrics.tasks_completed_this_week}</p>
          </Card>
        </Col>

        <Col xs={24} md={12}>
          <Card title="Недавняя активность" bordered={false}>
            <p><strong>Последняя созданная задача:</strong> {recent_activity.last_task_created || "—"}</p>
            <p><strong>Последняя выполненная задача:</strong> {recent_activity.last_task_completed || "—"}</p>
            <p><strong>Самый активный день:</strong> {recent_activity.most_active_day}</p>
          </Card>
        </Col>

        <Col span={24}>
          <Card title="Активность по дням недели" bordered={false}>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#7C3AED" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>
    </div>
  );
}
