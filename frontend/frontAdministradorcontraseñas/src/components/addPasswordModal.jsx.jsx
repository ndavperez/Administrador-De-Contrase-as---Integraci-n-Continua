const AddPasswordModal = ({ isOpen, onClose, onSave }) => {
  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    const form = e.target;
    const newPassword = {
      service: form.service.value,
      username: form.username.value,
      password: form.password.value,
      note: form.note.value,
    };
    onSave(newPassword);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="bg-gray-900 p-6 rounded-xl w-96 text-white">
        <h2 className="text-xl font-bold mb-4">Agregar Contraseña</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <input
            type="text"
            name="service"
            placeholder="Servicio (Ej: Gmail)"
            className="p-2 rounded bg-gray-800 outline-none"
            required
          />
          <input
            type="text"
            name="username"
            placeholder="Usuario o Email"
            className="p-2 rounded bg-gray-800 outline-none"
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Contraseña"
            className="p-2 rounded bg-gray-800 outline-none"
            required
          />
          <textarea
            name="note"
            placeholder="Nota (opcional)"
            className="p-2 rounded bg-gray-800 outline-none"
          />
          <div className="flex justify-end gap-2 mt-4">
            <button type="button" onClick={onClose} className="text-gray-400">
              Cancelar
            </button>
            <button type="submit" className="bg-blue-500 px-4 py-2 rounded-lg hover:bg-blue-600">
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddPasswordModal;
