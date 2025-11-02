import { useEffect, useState } from "react";
import axios from "axios";
import { Card, Spin, message } from "antd";
import { useNavigate } from "react-router-dom";

export default function TasksList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/v1/tasks", {
          withCredentials: true, 
        });

        setTasks(response.data);
      } catch (error) {
        console.error("Failed to fetch tasks:", error);
        message.error("Не удалось загрузить задачи. Пожалуйста, авторизуйтесь.");
        navigate("/"); 
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [navigate]);

  if (loading)
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Spin tip="Загрузка..." size="large" />
      </div>
    );

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
      {tasks.map((task) => (
        <Card
          key={task.task_id}
          title={task.title}
          bordered={false}
          className="shadow-md"
          style={{
            backgroundColor: task.status === "pending" ? "#FFFFFF" : "#E5E7EB",
          }}
        >
          <p>{task.description}</p>
          <p>Статус: {task.status === "pending" ? "В работе" : "Выполнено"}</p>
          <p>Создано: {new Date(task.created_at).toLocaleString()}</p>
        </Card>
      ))}
    </div>
  );
}
