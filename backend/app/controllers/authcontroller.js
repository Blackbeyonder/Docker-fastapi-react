// Mock de usuarios
const users = [
  { username: 'admin', password: '1234', token: 'abcd1234' },
];

exports.login = (req, res) => {
  const { username, password } = req.body;

  // Validar credenciales
  const user = users.find((u) => u.username === username && u.password === password);

  if (user) {
    res.json({ success: true, token: user.token });
  } else {
    res.status(401).json({ success: false, message: 'Credenciales inválidas' });
  }
};
