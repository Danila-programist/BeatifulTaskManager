import { useState } from "react";
import { Button, Modal, Input, Select, message } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import axios from "axios";

const { TextArea } = Input;
const { Option } = Select;

export default function AddTaskButton({ onTaskAdded }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [task, setTask] = useState({
    title: "",
    description: "",
    status: "pending",
  });
  const [loading, setLoading] = useState(false);

  const handleOpen = () => setIsModalOpen(true);
  const handleClose = () => {
    setIsModalOpen(false);
    setTask({ title: "", description: "", status: "pending" });
  };

  const handleSubmit = async () => {
    if (!task.title || !task.description) {
      message.warning("Пожалуйста, заполните все поля");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        "/api/v1/tasks",
        task,
        { withCredentials: true }
      );
      message.success("Задача успешно создана!");
      if (onTaskAdded) onTaskAdded(response.data);
      handleClose();
    } catch (error) {
      console.error("Ошибка при создании задачи:", error);
      message.error("Не удалось создать задачу");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Плавающая кнопка + */}
      <Button
        type="primary"
        shape="circle"
        size="large"
        icon={<PlusOutlined />}
        style={{
          position: "fixed",
          bottom: 40,
          right: 40,
          zIndex: 1000,
          backgroundColor: "#7C3AED",
          borderColor: "#7C3AED",
          transition: "all 0.2s ease-in-out",
        }}
        onMouseEnter={(e) => (e.currentTarget.style.transform = "translateY(-2px)")}
        onMouseLeave={(e) => (e.currentTarget.style.transform = "translateY(0)")}
        onClick={handleOpen}
      />

      {/* Модалка */}
      <Modal
        title="Создать новую задачу"
        open={isModalOpen}
        onOk={handleSubmit}
        onCancel={handleClose}
        okText="Создать"
        cancelText="Отмена"
        confirmLoading={loading}
        okButtonProps={{
          style: {
            backgroundColor: "#7C3AED",
            borderColor: "#7C3AED",
            color: "#fff",
            transition: "all 0.2s ease-in-out",
          },
          onMouseDown: (e) => {
            e.currentTarget.style.backgroundColor = "#000000";
          },
          onMouseUp: (e) => {
            e.currentTarget.style.backgroundColor = "#7C3AED";
          },
        }}
        cancelButtonProps={{
          style: {
            backgroundColor: "#fff",
            color: "#000",
            borderColor: "#000",
            transition: "all 0.2s ease-in-out",
          },
        }}
      >
        <Input
          placeholder="Заголовок"
          className="mb-2"
          value={task.title}
          onChange={(e) => setTask({ ...task, title: e.target.value })}
        />
        <TextArea
          placeholder="Описание"
          className="mb-2"
          rows={4}
          value={task.description}
          onChange={(e) => setTask({ ...task, description: e.target.value })}
        />
        <Select
          value={task.status}
          onChange={(value) => setTask({ ...task, status: value })}
          className="w-full"
        >
          <Option value="pending">В работе</Option>
          <Option value="completed">Выполнено</Option>
        </Select>
      </Modal>
    </>
  );
}
