import { useState } from "react";
import Sidebar from "../components/Sidebar";
import AddPasswordModal from "../components/addPasswordModal.jsx";
import PasswordCard from "../components/passwordCard.jsx";

const Dashboard = () => {
  const [passwords, setPasswords] = useState([
    { service: "Gmail", username: "user@gmail.com" },
    { service: "Instagram", username: "@usuario" },
  ]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleAddPassword = (newPassword) => {
    setPasswords([...passwords, newPassword]);
  };

  return (
    <div className="flex bg-gray-950 text-white min-h-screen">
      <Sidebar />

      <main className="flex-1 p-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Mis Contraseñas</h1>
          <button
            onClick={() => setIsModalOpen(true)}
            className="bg-blue-500 px-4 py-2 rounded-lg hover:bg-blue-600"
          >
            + Nueva contraseña
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {passwords.map((p, i) => (
            <PasswordCard
              key={i}
              service={p.service}
              username={p.username}
              onView={() => alert("Mostrar contraseña")}
              onEdit={() => alert("Editar")}
              onDelete={() => alert("Eliminar")}
            />
          ))}
        </div>
      </main>

      <AddPasswordModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleAddPassword}
      />
    </div>
  );
};

export default Dashboard;
