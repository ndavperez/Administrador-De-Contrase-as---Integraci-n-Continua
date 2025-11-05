const Sidebar = () => {
  return (
    <aside className="w-64 bg-gray-900 text-white h-screen p-6 flex flex-col">
      <h2 className="text-2xl font-bold mb-10">Gestor de contraseñas</h2>
      <nav className="flex flex-col gap-4">
        <div className="mt-auto">
            
          <button className="text-left text-blue-400 hover:text-red-500">
            Cerrar sesión
          </button>
        </div>
      </nav>
    </aside>
  );
};

export default Sidebar;
