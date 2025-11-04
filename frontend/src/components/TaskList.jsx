import { useEffect, useState } from "react";
import axios from "axios";
import { Card, Spin, message, Button, Modal, Input, Select } from "antd";
import { useNavigate } from "react-router-dom";
import { DeleteOutlined, EditOutlined } from "@ant-design/icons";

const { TextArea } = Input;
const { Option } = Select;

export default function TasksList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingTask, setEditingTask] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();

  // 🔹 Загрузка списка задач
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

  // 🔹 Удаление задачи
  const handleDelete = async (taskId) => {
    try {
      await axios.delete(`http://localhost:8000/api/v1/tasks/${taskId}`, {
        withCredentials: true,
      });
      message.success("Задача успешно удалена!");
      setTasks((prev) => prev.filter((t) => t.task_id !== taskId));
    } catch (error) {
      console.error("Ошибка при удалении задачи:", error);
      message.error("Не удалось удалить задачу");
    }
  };

  // 🔹 Открытие модального окна для редактирования
  const handleEdit = (task) => {
    setEditingTask({ ...task });
    setIsModalOpen(true);
  };

  // 🔹 Сохранение изменений (PUT)
  const handleSave = async () => {
    try {
      await axios.put(
        `http://localhost:8000/api/v1/tasks/${editingTask.task_id}`,
        {
          title: editingTask.title,
          description: editingTask.description,
          status: editingTask.status,
        },
        { withCredentials: true }
      );

      message.success("Задача успешно обновлена!");
      setTasks((prev) =>
        prev.map((t) => (t.task_id === editingTask.task_id ? editingTask : t))
      );
      setIsModalOpen(false);
    } catch (error) {
      console.error("Ошибка при обновлении задачи:", error);
      message.error("Не удалось обновить задачу");
    }
  };

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
          className="shadow-md relative"
          style={{
            backgroundColor: task.status === "pending" ? "#FFFFFF" : "#E5E7EB",
          }}
          extra={
            <div className="flex gap-2">
              <Button
                type="text"
                icon={<EditOutlined />}
                onClick={() => handleEdit(task)}
              />
              <Button
                type="text"
                danger
                icon={<DeleteOutlined />}
                onClick={() => handleDelete(task.task_id)}
              />
            </div>
          }
        >
          <p>{task.description}</p>
          <p>
            <strong>Статус:</strong>{" "}
            {task.status === "pending" ? "В работе" : "Выполнено"}
          </p>
          <p>
            <strong>Создано:</strong>{" "}
            {new Date(task.created_at).toLocaleString()}
          </p>
        </Card>
      ))}

      {/* Модалка для редактирования */}
      <Modal
        title="Редактирование задачи"
        open={isModalOpen}
        onOk={handleSave}
        onCancel={() => setIsModalOpen(false)}
        okText="Сохранить"
        cancelText="Отмена"
      >
        <Input
          className="mb-2"
          placeholder="Заголовок"
          value={editingTask?.title}
          onChange={(e) =>
            setEditingTask((prev) => ({ ...prev, title: e.target.value }))
          }
        />
        <TextArea
          rows={3}
          className="mb-2"
          placeholder="Описание"
          value={editingTask?.description}
          onChange={(e) =>
            setEditingTask((prev) => ({ ...prev, description: e.target.value }))
          }
        />
        <Select
          className="w-full"
          value={editingTask?.status}
          onChange={(value) =>
            setEditingTask((prev) => ({ ...prev, status: value }))
          }
        >
          <Option value="pending">В работе</Option>
          <Option value="completed">Выполнено</Option>
        </Select>
      </Modal>
    </div>
  );
}
